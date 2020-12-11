# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime
from datetime import datetime as dt
from datetime import datetime as dir
from datetime import datetime as cal


class AccountTax(models.Model):
    _inherit = "account.tax"

    igst = fields.Boolean(string='IGST',default=False)



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_creation = fields.Many2one('res.users', string="created_by")

    purchase_creation_date = fields.Datetime(string='Purchase Creation Date')


    financial_representative = fields.Many2one('res.users',string="Financial Representative")

    financial_creation_date = fields.Datetime(string='Financial Approval Date')


    manager_representative = fields.Many2one('res.users',string="Manager Representative")

    manager_creation_date = fields.Datetime(string='Manager Approval Date')


    authorised_by = fields.Many2one('res.users',string="Authorised By")

    authorisation_date = fields.Datetime(string='Authorisation Date')

    @api.model
    def create(self, vals):
        vals['purchase_creation'] = self.env.uid if 'purchase_creation' in vals else ""
        vals['purchase_creation_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if 'purchase_creation_date' in vals else ""
        # for i in self:
        #     i.purchase_creation = self.env.uid
        #     i.purchase_creation_date = datetime.now()
        return super(PurchaseOrder, self).create(vals)



    def button_release(self):
        picking_vals = super(PurchaseOrder, self).button_release()
        for i in self:
            i.financial_representative = self.env.uid
            i.financial_creation_date = dt.now().strftime("%Y-%m-%d %H:%M:%S")

        return picking_vals



    def button_ceo(self):
        picking_vals = super(PurchaseOrder, self).button_ceo()
        for i in self:
            i.manager_representative= self.env.uid
            i.manager_creation_date = dir.now().strftime("%Y-%m-%d %H:%M:%S")

        return picking_vals

    def button_approve(self, force=False):
        for order in self:

            order.write({'authorised_by': self.env.uid,
                         'authorisation_date':cal.now().strftime("%Y-%m-%d %H:%M:%S")

                         })


        return super(PurchaseOrder, self).button_approve(
            force=force)
