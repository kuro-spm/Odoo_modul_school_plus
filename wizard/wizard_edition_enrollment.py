# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class EditionEnrollmentWizard(models.TransientModel):
    _name = 'school.edition.enrollment.wizard'
    _description = 'EditionEnrollment'

    course_edition_id = fields.Many2one('school.course.edition', string='Course Edition')

    n_enrolled_students = fields.Integer(string='Number of enrolled students', readonly=True)
    n_succesfull_students =fields.Integer(string='Number of succesfull students', readonly=True)
    n_failed_students =fields.Integer(string='Number of failed students', readonly=True)

    state = fields.Selection([('init', 'Init'), ('done', 'Done')], 'State', default='init')

    def count_students(self):
        all_enrollments = self.env['school.enrollment']
        
        total = all_enrollments.search_count([
            ('edition_id', '=', self.course_edition_id.id)
        ])

        success =all_enrollments.search_count([
            ('edition_id', '=', self.course_edition_id.id),
            ('qualification', '>=', 5)
        ])

        failed =all_enrollments.search_count([
            ('edition_id', '=', self.course_edition_id.id),
            ('qualification', '<', 5)
        ])

        self.write(
            {
            'n_enrolled_students':total, 
            'n_succesfull_students':success, 
            'n_failed_students':failed, 
            'state': 'done'
            }
        )

        return {
            'name': 'Wizard to count editions before dates',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
            'res_model': 'school.edition.enrollment.wizard',
            'type': 'ir.actions.act_window',
        }
