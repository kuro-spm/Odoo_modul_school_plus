from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_ids = fields.One2many('school.student', 'customer_id', string='Students')

  
