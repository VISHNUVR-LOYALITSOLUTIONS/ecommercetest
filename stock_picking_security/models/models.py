# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stock_picking_security(models.Model):
    _inherit = 'res.users'




    operating_unit_security = fields.Many2many(comodel_name="operating.unit",
        string="Stock Operating Units")



    # @api.onchange('allowed_operating_unit')
    # def allow_stock_picking(self):
    #
    #     for user in self:
    #         if user.allowed_operating_unit:
    #             stock = self.env['stock.picking'].search(
    #                 [('location_dest_id.operating_unit_id', 'in', user.operating_unit_ids.ids),
    #                  ('picking_type_code', '=', 'internal')])








                #
    #
    #
    # def stock_operating_unit(self):
    #
    #     stocks = self.env['stock.picking'].search([])
    #
    #     user_id = self.env.user.id
    #
    #     stock_user = self.env['res.users'].browse(user_id)
    #     a=[]
    #     for i in self:
    #         if i.operating_unit_id:
    #             a.append(i.operating_unit_id.id)
    #


