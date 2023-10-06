from odoo import models, fields


class Treatment(models.Model):
    _name = 'treatment.module'
    _description = 'Treatment'
    _inherit = ['mail.thread', 'mail.activity.mixin'] #enables tracking

    name = fields.Char(string='Name')
    is_done = fields.Boolean(string='Is Done')
    appointment_id = fields.Many2one('appointment.module', string='Appointment', tracking=True)
