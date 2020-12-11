# -*- coding: utf-8 -*-

from odoo import models, fields, api

class company_privilege_policies(models.Model):
    _inherit = 'operating.unit'

    select_rule = fields.Many2one('branch_policies.branch_policies')
    branch_limit = fields.Float()

