# -*- coding: utf-8 -*- 
from odoo import models, fields, api, _ 
from odoo.exceptions import ValidationError 
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from ..utils.utils import is_valid_email

 #Forma part de school_plus
class SchoolStudent(models.Model): 
    _name = 'school.student' 
    _description = 'Student Management' 
    _rec_name = 'display_name' #Per defecte és Name, però no tenim aquest camp
    _order = 'last_name,first_name'

    #Dades obligatòries:
    first_name = fields.Char('First Name', size=30, required=True)
    last_name = fields.Char('Last Name', size=40, required=True)
    birthdate = fields.Date('Birthdate', required=True)
    phone = fields.Char('Phone', required=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other','Other')],'Gender', required=True)
    #adress
    address1 = fields.Char('Adress 1', required=True)
    address2 = fields.Char('Adress 2') #no obligatoria
    zip_code = fields.Char('Zip Code', required=True)
    city = fields.Char('City', required=True)
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country','Citizenship', required=True)

    #Dades optatives:
    email = fields.Char('eMail', size=60, required=False)
    #Camps calculats
    age =fields.Integer('Age', compute='_compute_age', store=False)
    #Dades obligatòries segons condició:
    tin = fields.Char('Tax ID', size=14)
    guardian_info = fields.Text('Guardian information')
    #Altres relacions
    enrollment_ids = fields.One2many('school.enrollment', 'student_id', string='Enrollment')

    # El Tutor/Pagador (res.partner)
    customer_id = fields.Many2one('res.partner', string="Guardian", required=True)   

    # Related fields: És vital afegir readonly=True i, preferiblement, store=False 
    # per no omplir la base de dades amb informació duplicada.
    customer_phone = fields.Char(related='customer_id.phone', string='Phone', readonly=True)
    customer_street = fields.Char(related='customer_id.street', string='Street', readonly=True)
    customer_street2 = fields.Char(related='customer_id.street2', string='Street 2', readonly=True)
    customer_zip = fields.Char(related='customer_id.zip', string='Zip', readonly=True)
    customer_city = fields.Char(related='customer_id.city', string='City', readonly=True)

    # CORRECCIÓ CLAU: 
    # Per als camps Many2one, assegura't que el co-model ('res.country.state') 
    # sigui exactament el mateix que el camp original al que apuntes.
    customer_state_id = fields.Many2one(
        comodel_name='res.country.state', 
        related='customer_id.state_id', 
        string='State', 
        readonly=True
    )
    customer_country_id = fields.Many2one(
        comodel_name='res.country', 
        related='customer_id.country_id', 
        string='Country', 
        readonly=True
    )

    @api.depends('first_name', 'last_name')
    def _compute_display_name(self):
        #self és equivalent a this.
        #és el conjunt de registres (recordset) sobre el que es necessita executar el mètode.
        for obj in self:
            if obj.first_name and obj.last_name:
                obj.display_name = obj.last_name + ", " + obj.first_name
            else:
                obj.display_name = ''

    @api.constrains('email')
    def check_email(self):
        for obj in self:
            if obj.email and not is_valid_email(obj.email):
                raise ValidationError(_("Email is invalid."))

    @api.constrains('phone')
    def check_phone(self):
        for obj in self:
            if obj.phone and not obj.phone.isdigit():
                raise ValidationError(_("Phone number can only contain digits."))

    @api.depends('birthdate')
    def _compute_age(self):
        avui = date.today()
        for obj in self:
            if obj.birthdate: 
                obj.age = relativedelta(avui, obj.birthdate).years
            else:
                obj.age=0


    @api.onchange('tin')
    def _onchange_tin(self):
        if(self.tin):
            self.tin = self.tin.upper()

   
   
    #campo_id = fields.Many2one('modelo.destino', string='Etiqueta', required=True) 
    #campos_ids = fields.One2many('modelo.destino', 'campo_many2one_inverso', string='Etiqueta') 
    #campos_ids = fields.Many2many('modelo.destino', string='Etiqueta') 
