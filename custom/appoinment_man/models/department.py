from odoo import models, fields, api, exceptions
from odoo.exceptions import ValidationError


class Department(models.Model):
    _name = 'department.module'
    _description = 'Department'
    _rec_name = 'name'

    name = fields.Char(string='Name')
    code = fields.Char(string='Code', required=True, index=True)

    @api.constrains('code')
    def _check_code_unique(self):
        for record in self:
            if self.env['department.module'].search_count([('code', '=', record.code)]) > 1:
                raise exceptions.ValidationError('The Code must be unique.')
