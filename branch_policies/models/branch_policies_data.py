# -*- coding: utf-8 -*-

from odoo import models, fields, api

class branch_policies(models.Model):
    _name = 'branch_policies.branch_policies'

    name = fields.Char(string="Based On")
    short_code = fields.Char(string="Short Code")
