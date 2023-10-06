from odoo import models, fields, api, exceptions
from odoo.exceptions import UserError


class Appointment(models.Model):
    _name = 'appointment.module'
    _description = 'Appointment'
    _rec_name = 'code'

    code = fields.Char(string='Code', required=True, index=True)
    appointment_datetime = fields.Datetime(string='Appointment Date and Time')
    doctor_ids = fields.Many2many('doctor.module', string='Doctors')
    patient_id = fields.Many2one('patient.module', string='Patient')
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancel')],
        string='Stage', default='draft', statusbar_clickable=True)
    name = fields.Char(string="Name")
    treatment_ids = fields.One2many('treatment.module', 'appointment_id', string='Treatments')

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['appointment.module'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The Code must be unique.')

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('appointment.module') or 'New'
        result = super(Appointment, self).create(vals)
        return result

    def in_progress(self):
        self.write({'stage': 'in_progress'})

    def done(self):
        self.write({'stage': 'done'})

    def draft(self):
        self.write({'stage': 'draft'})

    def cancel(self):
        self.write({'stage': 'cancel'})

    def unlink(self):
        for appointment in self:
            if appointment.stage == 'done':
                raise UserError("You cannot delete an appointment that is in 'Done' stage.")
        return super(Appointment, self).unlink()
