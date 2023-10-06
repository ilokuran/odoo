from odoo import api, fields, models


class AppointmentWizard(models.TransientModel):
    _name = 'appointment.wizard'
    _description = 'Create Appointment Wizard'

    patient_id = fields.Many2one('patient.module', string='Patient', required=True)
    doctor_ids = fields.Many2many('doctor.module', string='Doctors', required=True)
    #code = fields.Char(string='Code', required=True, default='_default_code')
    code = fields.Char(string='Code', required=True, default=lambda self: self._default_code() or 'New')

    def button_create_appointment(self):
        self.ensure_one()
        vals = {
            'patient_id': self.patient_id.id,
            'doctor_ids': [(6, 0, self.doctor_ids.ids)],
            'code': self.code,
            'stage': 'draft',
        }
        self.env['appointment.module'].create(vals)
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def _default_code(self):
        return self.env['ir.sequence'].next_by_code('appointment.wizard.code' or 'New')

