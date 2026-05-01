# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

#omod per crear una classe automaticament!
#oof per crear un camp automàticament!

#Forma part de school_plus
class SchoolEnrollment(models.Model):
    _name = 'school.enrollment'
    _description = 'School Enrollment Management'

    qualification = fields.Float(digits=(3,1), string="Qualification", default=0.0, required=True)
    student_id = fields.Many2one('school.student', string='Student', required=True)
    subject_ids = fields.One2many('school.enrollment.subject', 'enrollment_id', string='Subjects')
    edition_id = fields.Many2one('school.course.edition', string='Course edition', required=True) 
    
    #Related fields
    #Necessitem start_date i stop_date del course edition
    # Related fields
    #El primer parametre ha de ser string='' o dona error!
    course_edition_date_start = fields.Date(string='Start Date', related='edition_id.date_start', readonly=True)
    course_edition_date_stop = fields.Date(string='Stop Date', related='edition_id.date_stop', readonly=True)

    #related fields de l'alumne:
    student_phone=fields.Char('Phone', related='student_id.phone' readonly=True)
    student_email=fields.Char('email', related='student_id.email' readonly=True)

    @api.constrains('qualification')
    def _check_qualification(self):
        for obj in self:
            if not obj.qualification:
                obj.qualification=0
            # S'avalua directament la condició matemàtica.
            # Es recomana posar els decimals (10.0 i 0.0) per mantenir la coherència de tipus Float.
            if obj.qualification > 10.0 or obj.qualification < 0.0:
                raise ValidationError(_('Qualification must be between 0.0 and 10.0'))
    

    @api.model_create_multi
    def create(self, vals_list):
        # 1. Primer creem les matrícules (enrollments) cridant al super.
        # 'registres' serà un recordset amb les matrícules ja creades (i amb ID!).
        registres = super(SchoolEnrollment, self).create(vals_list)

        # 2. Iterem sobre cada matrícula acabada de crear
        for matricula in registres:
            # 3. Obtenim el curs a través de l'edició
            # Recorda: l'edició sap a quin curs pertany (edition_id.course_id)
            curs = matricula.edition_id.course_id

            if curs:
                # 4. Busquem les assignatures que formen part d'aquest curs
                # Anem a la taula 'school.course.subject'
                assignatures_del_curs = self.env['school.course.subject'].search([
                    ('course_id', '=', curs.id)
                ])

                # 5. Per cada assignatura trobada, creem el registre a la taula de notes
                for line in assignatures_del_curs:
                    self.env['school.enrollment.subject'].create({
                        'enrollment_id': matricula.id,  # Lliguem a la matrícula actual
                        'subject_id': line.subject_id.id, # L'assignatura concreta
                        'qualification': 0.0             # Nota inicial per defecte
                    })
        
        # 6. Finalment, retornem el recordset original com marca el protocol d'Odoo
        return registres

                            
                            
                            





    