from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DoctorModel(models.Model):
    _name = 'doctor.module'
    _description = 'Doctors'
    _rec_name = 'full_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name')
    date_of_birth = fields.Date(string='Date of Birth',required=True)
    age = fields.Integer(string='Age', store=True, compute='_compute_age', readonly=True)
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email', required=True, copy=False)
    department_id = fields.Many2one('department.module', string='Department')
    shift_start = fields.Float(string='Shift Start', required=True)
    shift_end = fields.Float(string='Shift End', required=True)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for record in self:
            record.full_name = f"{record.first_name} {record.last_name}"

    @api.constrains('email')
    def _check_email_unique(self):
        for doctor in self:
            if self.env['doctor.module'].search_count([('email', '=', doctor.email)]) > 1:
                raise ValidationError('Email address must be unique.')

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                delta = today - record.date_of_birth
                record.age = delta.days // 365
            else:
                record.age = 0
