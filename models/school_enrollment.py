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

    qualification = fields.Float(digits=(3,1), string="Qualification", required=True)
    student_id = fields.Many2one('school.student', string='Student', required=True)
    subject_ids = fields.One2many('school.enrollment.subject', 'enrollment_id', string='Subjects')
    edition_id = fields.Many2one('school.course.edition', string='edition', required=True) 
    
    #Necessitem start_date i stop_date del course edition

    @api.constrains('qualification')
    def _check_qualification(self):
        for obj in self:
            # S'avalua directament la condició matemàtica.
            # Es recomana posar els decimals (10.0 i 0.0) per mantenir la coherència de tipus Float.
            if obj.qualification > 10.0 or obj.qualification < 0.0:
                raise ValidationError(_('Qualification must be between 0.0 and 10.0'))
    

    