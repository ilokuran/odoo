from odoo import models, fields, api, exceptions
from datetime import date


class Patient(models.Model):
    _name = 'patient.module'
    _description = 'Patient'
    _rec_name = 'full_name'
    patient_id = fields.Char(string='Patient ID', required=True, copy=False, readonly=True,
                             default=lambda self: self.env['ir.sequence'].next_by_code('patient.module.id') or 'New')
    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    full_name = fields.Char(string='Full Name', compute='_compute_full_name')
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', readonly=True, compute='_compute_age')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    national_id_no = fields.Char(string='National ID No')

    @api.model
    def create(self, vals):
        if vals.get('patient_id', 'New') == 'New':
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('patient.module.id') or 'New'
        return super(Patient, self).create(vals)

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for patient in self:
            patient.full_name = f"{patient.first_name} {patient.last_name}"

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for record in self:
            if record.date_of_birth:
                delta = today - record.date_of_birth
                record.age = delta.days // 365
            else:
                record.age = 0

    @api.model
    def create(self, vals):
        if vals.get('patient_id', ('New')) == ('New'):
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('patient.sequence') or ('New')
        result = super(Patient, self).create(vals)
        return result

    @api.constrains('national_id_no')
    def _check_national_id_no_unique(self):
        for patient in self:
            if self.search_count([('national_id_no', '=', patient.national_id_no)]) > 1:
                raise exceptions.ValidationError('The National ID must be unique.')
