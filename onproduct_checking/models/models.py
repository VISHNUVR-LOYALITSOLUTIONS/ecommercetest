# -*- coding: utf-8 -*-

from odoo import models, fields, api


class onproduct_checking(models.Model):
    _inherit='product.template'


    own_product = fields.Boolean(string="Own Product",default=False)
