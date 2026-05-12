# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 

#Forma part de school_plus
class SchoolEnrollmentSubject(models.Model):
    _name = 'school.enrollment.subject'
    _description = 'School Enrollment Subject Management'

    qualification = fields.Float(digits=(3,1), string="Qualification", required=True, default=0.0)
    enrollment_id = fields.Many2one('school.enrollment', string='Enrollment', required=True, ondelete='cascade') #si dónes de baixa una matrícula sencera, s'esborraran automàticament totes les assignatures que hi havia penjant d'ella i no et quedaran dades escombraries a la base de dades.
    subject_id = fields.Many2one('school.course.subject', string='Subject', required=True)

    @api.constrains('qualification')
    def _check_qualification(self):
        for obj in self:
            # S'avalua directament la condició matemàtica.
            # Es recomana posar els decimals (10.0 i 0.0) per mantenir la coherència de tipus Float.
            if obj.qualification > 10.0 or obj.qualification < 0.0:
                raise ValidationError(_('Qualification must be between 0.0 and 10.0'))
    
