# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class Branch_limit(models.Model):
    _name = 'branch.excess.limit'


    reference_no = fields.Char(string="Reference")
    excess_amount = fields.Float(string="Excess Amount")
    picking_date = fields.Datetime(string="Date")
    source_location = fields.Many2one('stock.location',string="Source Location")
    destination_location = fields.Many2one('stock.location',string="Destination Location")


class confirm_wizard(models.TransientModel):
    _name = 'approval.message'


    text= fields.Char()




    def btn_approve(self):
        current_id = self.env.context.get('current_id', False)
        picking = self.env['stock.picking'].browse(current_id)
        for order in picking:
            order.write({'state': 'send_to_manager_approval'})
        return

