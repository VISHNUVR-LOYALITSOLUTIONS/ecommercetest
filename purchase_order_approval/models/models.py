# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


# class REsuser_security(models.Model):
#     _inherit = 'res.users'
#
#
#     financial_security = fields.Boolean(string="Financial Approval",default=False)
#     ceo_security = fields.Boolean(string="CEO Approval", default=False)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[('waiting_for_financial_approval', 'Financial Approval'),('waiting_for_manager_approval', 'Manager Approval')])

    # @api.model
    # def create(self, values):
    #
    #     rec = super(PurchaseOrder, self).create(values)
    #
    #     if 'partner_id' in values:
    #
    #         team = self.env['res.users'].sudo().search([
    #             ("groups_id", "=",self.env.ref("purchase_order_approval.group_financial_approval").id),
    #            ])
    #
    #
    #
    #         partners = [i.id for i in team.partner_id]
    #
    #         if partners:
    #
    #             rec.message_subscribe(partner_ids=partners)
    #
    #     return rec
    #
    #


    #
    # @api.model
    # def create(self, vals):
    #     lead_res = super(PurchaseOrder, self).create(vals)
    #     for rec in lead_res:
    #         if rec.estimation_ids:
    #             partner_ids = []
    #             for est_rec in rec.estimation_ids:
    #                 if est_rec.partner_id and est_rec.partner_id.email:
    #                     partner_ids.append(est_rec.partner_id.id)
    #             if partner_ids:
    #                 rec.message_subscribe(partner_ids, None)
    #     return lead_res

    def button_confirm(self):
        for order in self:
            order._add_supplier_to_product()
            order.write({'state': 'waiting_for_financial_approval'})

            if order.partner_id:

                team = self.env['res.users'].sudo().search([
                    ("groups_id", "=", self.env.ref("purchase_order_approval.group_financial_approval").id),
                ])

                partners = [i.id for i in team.partner_id]

                if partners:
                    order.message_subscribe(partner_ids=partners)



    def button_release(self):
        for order in self:
            order.state = 'waiting_for_manager_approval'
            if order.partner_id:

                team = self.env['res.users'].sudo().search([("groups_id", "=", self.env.ref( "purchase_order_approval.group_ceo_approval" ).id),])



                partners = [i.id for i in team.partner_id]

                if partners:

                    order.message_subscribe(partner_ids=partners)



        # super(PurchaseOrder, self).button_approve()

    # def button_approve(self, force=False):
    #     for order in self:
    #     # approve_purchases = self.filtered(
    #     #     lambda p: p.user_id.financial_security)
    #         order.write({'state': 'waiting_for_manager_approval'})


        # return super(PurchaseOrder, self).button_approve(
        #     force=force)

    def button_ceo(self):
        for order in self:
            # self._create_picking()
            order.write({'state': 'to approve'})
            # order.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
            if order.partner_id:

                team = self.env['res.users'].sudo().search([("groups_id", "=",self.env.ref("purchase_order_approval.group_ceo_approval_approval").id)])

                partners = [i.id for i in team.partner_id]

                if partners:
                    order.message_subscribe(partner_ids=partners)





    # @api.multi
    # def action_sales_approvals(self):
    #     for order in self:
    #         order.state = 'waiting_for_md_approval'
    #
    # @api.multi
    # def md_approval(self):
    #     for order in self:
    #         order.state = 'md_approved'
    #
    # @api.multi
    # def md_refused(self):
    #     for order in self:
    #         order.state = 'md_refused'
    #
    # @api.multi
    # def print_quotation(self):
    #     self.filtered(lambda s: s.state == 'md_approved').write({'state': 'sent'})
    #     return self.env['report'].get_action(self, 'sale.report_saleorder')
    #
    # @api.multi
    # def action_draft(self):
    #     orders = self.filtered(lambda s: s.state in ['cancel', 'sent','md_refused'])
    #     orders.write({
    #         'state': 'draft',
    #         'procurement_group_id': False,
    #     })
    #     return orders.mapped('order_line').mapped('procurement_ids').write({'sale_line_id': False})
