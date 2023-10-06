from odoo import models, fields


class MyModel(models.Model):
    _name = 'test.module'
    _description = '1. denemeee'

    name = fields.Char(string='Name', required=True)
