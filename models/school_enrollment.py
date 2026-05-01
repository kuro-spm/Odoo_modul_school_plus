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
    edition_id = fields.Many2one('school.course.edition', string='Course edition', required=True) 
    
    #Related fields
    #Necessitem start_date i stop_date del course edition
    # Related fields
    #El primer parametre ha de ser string='' o dona error!
    course_edition_date_start = fields.Date(string='Start Date', related='edition_id.date_start')
    course_edition_date_stop = fields.Date(string='Stop Date', related='edition_id.date_stop')

    #related fields de l'alumne:
    student_phone=fields.Char('Phone', related='student_id.phone')
    student_email=fields.Char('email', related='student_id.email')

    @api.constrains('qualification')
    def _check_qualification(self):
        for obj in self:
            # S'avalua directament la condició matemàtica.
            # Es recomana posar els decimals (10.0 i 0.0) per mantenir la coherència de tipus Float.
            if obj.qualification > 10.0 or obj.qualification < 0.0:
                raise ValidationError(_('Qualification must be between 0.0 and 10.0'))
    
    @api.model_create_multi
    def create(self,values):
        # values és una llista de diccionaris amb els valors dels camps dels registres a inserir
        r= super().create(values) #llista de registres ja creats (ja tenen ID)
        
        for d in r:
            enrollment_id= '???'
            #per cada valor edition_id al diccionari de valors...
            if 'enrollment_id' in d and d['enrollment_id']!=False:
                #hem de crear enrollment_subject...
                #anem a buscar les assignatures a school.course.subject...
                enroll_subj={}
                enroll_subj[self.edition_id] = d['enrollment_id']
                enroll_subj[self.qualification]=0
                subjects = self.env['school.course.subject'].search([('course_id', '=', d[''])])
                for sbj in subjects:
                    enroll_subj[subject_id] = sbj
                    self.env['school.enrollment.subject'].create(enroll_subj)



                            
                            
                            





    