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
    edition_course_id = fields.Many2one(string='Course', related='edition_id.course_id')

    #related fields de l'alumne:
    student_phone=fields.Char('Phone', related='student_id.phone', readonly=True)
    student_email=fields.Char('email', related='student_id.email', readonly=True)

    @api.constrains('qualification')
    def _check_qualification(self):
        for obj in self:
            # S'avalua directament la condició matemàtica.
            # Es recomana posar els decimals (10.0 i 0.0) per mantenir la coherència de tipus Float.
            if obj.qualification > 10.0 or obj.qualification < 0.0:
                raise ValidationError(_('Qualification must be between 0.0 and 10.0'))
    

    @api.model_create_multi
    def create(self, values):
        # 1. Primer creem les matrícules utilitzant el super()
        r = super().create(values)

        # 2. Ara processem cada matrícula inserida per afegir-li les assignatures
        for matricula in r:
            # Obtenim el curs a través de l'edició
            curs = matricula.edition_id.course_id
            
            if curs:
                # Busquem les assignatures vinculades a aquest curs
                assignatures_curs = self.env['school.course.subject'].search([
                    ('course_id', '=', curs.id)
                ])

                # Per cada assignatura del curs, creem un registre a 'school.enrollment.subject'
                for linia in assignatures_curs:
                    nota_inicial = {}
                    nota_inicial['enrollment_id'] = matricula.id
                    nota_inicial['subject_id'] = linia.id  
                    nota_inicial['qualification'] = 0.0
                    
                    # Creem el registre de la nota utilitzant el diccionari preparat
                    self.env['school.enrollment.subject'].create(nota_inicial)

        # 3. Retornem el recordset de matrícules
        return r    
                            
                            
                            





    