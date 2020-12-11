# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round



# class REsuser_security(models.Model):
#     _inherit = 'res.users'
#
#
#     financial_security = fields.Boolean(string="Financial Approval",default=False)
#     ceo_security = fields.Boolean(string="CEO Approval", default=False)

class Stockpicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection(selection_add=[('send_to_logistic_approval', 'Send to logistic Approval'),('send_to_manager_approval', 'Send to Manager Approval'),
                                            ('ready_to_transfer', 'Ready To Transfer'),('stock_in_transist', 'Stock in Transist'),
                                            ('validate_confirm', 'Proceed To validate')])

    virtual_loaction = fields.Many2one('stock.location',string="Virtual Location",default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,)
    tmp_source_loaction = fields.Many2one('stock.location', string="Temporary Source Location")

    tmp_destination_loaction = fields.Many2one('stock.location', string="Destination Location",default=lambda self: self.env['stock.picking.type'].browse(self._context.get('default_picking_type_id')).default_location_dest_id,)

    branch_excess_amount = fields.Float("Excess Amount")
    security_confirm = fields.Boolean("Security For Confirm",default=False,compute='security_for_confirm',store=True)
    security_validate = fields.Boolean("Security For validate",default=False,compute='security_for_validate',store=True)

    @api.depends('picking_type_code','state')
    def security_for_validate(self):
        for order in self:
            s=[]
            if order.picking_type_code == 'internal':
                if order.state in ['draft','send_to_logistic_approval','send_to_manager_approval','ready_to_transfer','stock_in_transist']:
                    order.security_validate = True
            else:
                order.security_validate = False

    @api.depends('picking_type_code')
    def security_for_confirm(self):
        for order in self:
            if order.picking_type_code=='internal':
                order.security_confirm=True
            else:
                order.security_confirm = False


    def confirm_button(self):
        for order in self:
            order.write({'state': 'send_to_logistic_approval',
                         'tmp_destination_loaction':order.location_dest_id.id})


    def confirm_logistic_approval(self):
        for i in self:
            lines = []
            if i.location_dest_id:
                branch_rule = i.location_dest_id.operating_unit_id.select_rule.short_code
                branch_amount = i.location_dest_id.operating_unit_id.branch_limit
            else:
                branch_rule = i.operating_unit_id.select_rule.short_code
                branch_amount = i.operating_unit_id.branch_limit
            product = self.env['product.product'].search([])
            current_stock = 0
            # current_st=0
            if branch_rule == 'BSP':

                query = '''

                                                           (select product_id as id,location_id as location_id,round(sum(name),4) as opening_stock from
                                              (select i.id , l.id as location_id,product_id,i.name as description,
                                                  case when state ='done' then product_qty else 0 end as name,
                                                  case when state !='done' then product_qty else 0 end as product_qty_pending,date,picking_id,l.company_id
                                              from stock_location l,
                                                  stock_move i
                                              where l.usage='internal'
                                                  and i.location_dest_id = l.id
                                                  and state != 'cancel'
                                                  and i.company_id = l.company_id
                                                  and l.operating_unit_id =%s

                                              union all

                                              select -o.id ,l.id as location_id ,product_id,o.name as description,
                                                  case when state ='done' then -product_qty else 0 end as name,
                                                  case when state !='done' then -product_qty else 0 end as product_qty_pending,date, picking_id,l.company_id
                                              from stock_location l,
                                                  stock_move o
                                              where l.usage='internal'
                                                  and o.location_id = l.id
                                                  and state != 'cancel'
                                                  and o.company_id = l.company_id
                                                  and l.operating_unit_id=%s
                                                  )s where location_id=%s group by product_id,location_id)
                                          '''

                self.env.cr.execute(query, (
                    i.location_dest_id.operating_unit_id.id, i.location_dest_id.operating_unit_id.id,
                    i.location_dest_id.id))

                for row in self.env.cr.dictfetchall():

                    product_id = row['id'] if row['id'] else 0
                    opening_stock = row['opening_stock'] if row['opening_stock'] else 0

                    query3 = """

                                    select pt.list_price as sale_price from product_product as p 
                        	left join product_template as pt on pt.id=p.product_tmpl_id 	
                                                             where p.id=%s 

                                                                  """

                    self.env.cr.execute(query3, (row['id'],))

                    closingstock_cost = 0
                    for ans1 in self.env.cr.dictfetchall():
                        closingstock_cost = ans1['sale_price'] if ans1['sale_price'] else 0

                    res = {
                        'id': row['id'],

                        'opening_stock': round(opening_stock, 2),
                        'current_stock': round((opening_stock * closingstock_cost), 2),
                    }
                    lines.append(res)

                current_stock = sum([item['current_stock'] for item in lines])
                # current_stock = sum([amount.qty_available * amount.lst_price for amount in product])
                current_product_stock = sum(
                    [am.qty_available * am.lst_price for ams in i.move_ids_without_package for am in
                     ams.product_id])
                stock_form_product_stock = sum(
                    [am.product_uom_qty * am.product_id.lst_price for ams in i.move_ids_without_package for am in
                     ams])

                if (branch_amount - current_stock) < stock_form_product_stock:
                    i.branch_excess_amount = stock_form_product_stock-((branch_amount - current_stock))

                    return {
                        'name': 'Are you sure?',
                        'type': 'ir.actions.act_window',
                        'res_model': 'approval.message',
                        'view_mode': 'form',
                        'view_type': 'form',
                        'target': 'new',
                        'context': {'current_id': i.id}
                    }
                    # i.write({'state': 'send_to_manager_approval'})
                    # raise UserError(_('Your Transaction Limit Is %s') % (branch_amount - current_stock))
                else:
                    i.write({'state': 'ready_to_transfer'})


            elif branch_rule == 'BCP':

                query = '''

                                                (select product_id as id,location_id as location_id,round(sum(name),4) as opening_stock from
                                              (select i.id , l.id as location_id,product_id,i.name as description,
                                                  case when state ='done' then product_qty else 0 end as name,
                                                  case when state !='done' then product_qty else 0 end as product_qty_pending,date,picking_id,l.company_id
                                              from stock_location l,
                                                  stock_move i
                                              where l.usage='internal'
                                                  and i.location_dest_id = l.id
                                                  and state != 'cancel'
                                                  and i.company_id = l.company_id
                                                  and l.operating_unit_id =%s

                                              union all

                                              select -o.id ,l.id as location_id ,product_id,o.name as description,
                                                  case when state ='done' then -product_qty else 0 end as name,
                                                  case when state !='done' then -product_qty else 0 end as product_qty_pending,date, picking_id,l.company_id
                                              from stock_location l,
                                                  stock_move o
                                              where l.usage='internal'
                                                  and o.location_id = l.id
                                                  and state != 'cancel'
                                                  and o.company_id = l.company_id
                                                  and l.operating_unit_id=%s
                                                  )s where location_id=%s group by product_id,location_id)
                                '''

                self.env.cr.execute(query, (
                    i.location_dest_id.operating_unit_id.id, i.location_dest_id.operating_unit_id.id,
                    i.location_dest_id.id))

                for row in self.env.cr.dictfetchall():
                    product_id = row['id'] if row['id'] else 0
                    opening_stock = row['opening_stock'] if row['opening_stock'] else 0
                    closingstock_cost = self.env['product.product'].browse(row['id']).standard_price,
                    # closingstock_cost = float(closingstock)

                    #                     query3 = """
                    #
                    #
                    #                     select ph.unit_cost as cost from stock_valuation_layer as ph
                    # left join res_users as r on r.id = ph.write_uid where ph.product_id=%s and r.default_operating_unit_id=%s
                    # order by ph.id DESC LIMIT 1
                    #
                    #                                         """
                    #
                    #                     self.env.cr.execute(query3, (row['id'], i.location_dest_id.operating_unit_id.id))
                    #
                    #                     closingstock_cost = 0
                    #                     for ans1 in self.env.cr.dictfetchall():
                    #                         closingstock_cost = ans1['cost'] if ans1['cost'] else 0

                    res = {
                        'id': row['id'],

                        'opening_stock': round(opening_stock, 2) if opening_stock != 0 else 0,
                        'current_stock': round((opening_stock * closingstock_cost[0]), 2) if opening_stock != 0 and
                                                                                             closingstock_cost[
                                                                                                 0] != 0 else 0,
                    }
                    lines.append(res)

                current_stock = sum([item['current_stock'] for item in lines])
                # current_stock = sum([item['current_stock'] for item in lines])

                # current_stock = sum([amount.qty_available * amount.standard_price for amount in product])
                current_product_stock = sum(
                    [am.qty_available * am.standard_price for ams in i.move_ids_without_package for am in
                     ams.product_id])
                stock_form_product_stock = sum(
                    [am.product_uom_qty * am.product_id.standard_price for ams in i.move_ids_without_package for am
                     in ams])

                if (branch_amount - current_stock) < stock_form_product_stock:
                    i.branch_excess_amount = stock_form_product_stock-((branch_amount - current_stock))

                    # i.write({'state': 'send_to_manager_approval'})
                    # raise UserError(_('Your Transaction Limit Is %s') % (branch_amount - current_stock))
                    return {
                        'name': 'Are you sure?',
                        'type': 'ir.actions.act_window',
                        'res_model': 'approval.message',
                        'view_mode': 'form',
                        'view_type': 'form',
                        'target': 'new',
                        'context': {'current_id': self.id}
                    }

                    # return {
                    #     'name': 'My Window',
                    #     'domain': [],
                    #     'res_model': 'stock.picking',
                    #     'type': 'ir.actions.act_window',
                    #     'view_mode': 'form',
                    #     'view_type': 'form',
                    #     'context': {},
                    #     'target': 'new',
                    # }

                else:
                    i.write({'state': 'ready_to_transfer'})




    def confirm_manager_approval(self):
        for order in self:

            so_order = {
                'reference_no': order.name,
                'excess_amount': order.branch_excess_amount,
                'picking_date': order.scheduled_date,
                'source_location': order.location_id.id,
                'destination_location': order.location_dest_id.id,

            }

            so = self.env['branch.excess.limit'].create(so_order)

            order.state = 'ready_to_transfer'
        return

    def stock_transfer(self):

        for i in self.move_line_ids:
            i.location_dest_id = self.virtual_loaction.id
        self.ensure_one()
        if not self.move_lines and not self.move_line_ids:
            raise UserError(_('Please add some items to move.'))

        # Clean-up the context key at validation to avoid forcing the creation of immediate
        # transfers.

        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # add user as a follower
        self.message_subscribe([self.env.user.partner_id.id])

        # If no lots when needed, raise error
        picking_type = self.picking_type_id
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in
                                 self.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        no_reserved_quantities = all(
            float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in
            self.move_line_ids)
        if no_reserved_quantities and no_quantities_done:
            raise UserError(_(
                'You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

        if picking_type.use_create_lots or picking_type.use_existing_lots:
            lines_to_check = self.move_line_ids
            if not no_quantities_done:
                lines_to_check = lines_to_check.filtered(
                    lambda line: float_compare(line.qty_done, 0,
                                               precision_rounding=line.product_uom_id.rounding)
                )

            for line in lines_to_check:
                product = line.product_id
                if product and product.tracking != 'none':
                    if not line.lot_name and not line.lot_id:
                        raise UserError(
                            _('You need to supply a Lot/Serial number for product %s.') % product.display_name)

        # Propose to use the sms mechanism the first time a delivery
        # picking is validated. Whatever the user's decision (use it or not),
        # the method button_validate is called again (except if it's cancel),
        # so the checks are made twice in that case, but the flow is not broken
        sms_confirmation = self._check_sms_confirmation_popup()
        if sms_confirmation:
            return sms_confirmation

        if no_quantities_done:
            view = self.env.ref('stock.view_immediate_transfer')
            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, self.id)]})
            return {
                'name': _('Immediate Transfer?'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.immediate.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        if self._get_overprocessed_stock_moves() and not self._context.get('skip_overprocessed_check'):
            view = self.env.ref('stock.view_overprocessed_transfer')
            wiz = self.env['stock.overprocessed.transfer'].create({'picking_id': self.id})
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'stock.overprocessed.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        # Check backorder should check for other barcodes
        if self._check_backorder():
            return self.action_generate_backorder_wizard()
        self._check_company()

        todo_moves = self.mapped('move_lines').filtered(
            lambda self: self.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed'])
        # Check if there are ops not linked to moves yet
        for pick in self:
            if pick.owner_id:
                pick.move_lines.write({'restrict_partner_id': pick.owner_id.id})
                pick.move_line_ids.write({'owner_id': pick.owner_id.id})

            # # Explode manually added packages
            # for ops in pick.move_line_ids.filtered(lambda x: not x.move_id and not x.product_id):
            #     for quant in ops.package_id.quant_ids: #Or use get_content for multiple levels
            #         self.move_line_ids.create({'product_id': quant.product_id.id,
            #                                    'package_id': quant.package_id.id,
            #                                    'result_package_id': ops.result_package_id,
            #                                    'lot_id': quant.lot_id.id,
            #                                    'owner_id': quant.owner_id.id,
            #                                    'product_uom_id': quant.product_id.uom_id.id,
            #                                    'product_qty': quant.qty,
            #                                    'qty_done': quant.qty,
            #                                    'location_id': quant.location_id.id, # Could be ops too
            #                                    'location_dest_id': ops.location_dest_id.id,
            #                                    'picking_id': pick.id
            #                                    }) # Might change first element
            # # Link existing moves or add moves when no one is related
            for ops in pick.move_line_ids.filtered(lambda x: not x.move_id):
                # Search move with this product
                moves = pick.move_lines.filtered(lambda x: x.product_id == ops.product_id)
                moves = sorted(moves, key=lambda m: m.quantity_done < m.product_qty, reverse=True)
                if moves:
                    ops.move_id = moves[0].id
                else:
                    new_move = self.env['stock.move'].create({
                        'name': _('New Move:') + ops.product_id.display_name,
                        'product_id': ops.product_id.id,
                        'product_uom_qty': ops.qty_done,
                        'product_uom': ops.product_uom_id.id,
                        'description_picking': ops.description_picking,
                        'location_id': pick.location_id.id,
                        'location_dest_id': pick.virtual_loaction.id,
                        'picking_id': pick.id,
                        'picking_type_id': pick.picking_type_id.id,
                        'restrict_partner_id': pick.owner_id.id,
                        'company_id': pick.company_id.id,
                    })
                    ops.move_id = new_move.id
                    new_move._action_confirm()
                    todo_moves |= new_move
                    # 'qty_done': ops.qty_done})
        todo_moves._action_done(cancel_backorder=self.env.context.get('cancel_backorder'))
        todo_moves.write({'state': 'assigned', 'date': fields.Datetime.now()})
        # self.write({'date_done': fields.Datetime.now()})
        self._send_confirmation_email()
        self.state = 'stock_in_transist'
        # for order in self:


            # if order.location_id and order.location_dest_id:
            #     picking_vals = {
            #         'partner_id': order.partner_id.id,
            #         'company_id': order.company_id.id,
            #         'picking_type_id': order.picking_type_id.id,
            #         'location_id': order.location_id,
            #         'location_dest_id': order.virtual_loaction,
            #         'origin': order.name
            #     }
            #     picking_id = self.env['stock.picking'].sudo().create(picking_vals)
            # else:
            #     raise UserError(_('Please configure appropriate locations on Operation type/Partner'))
            #
            # for move in self.move_lines:
            #     lines = self.move_line_ids.filtered(lambda x: x.product_id == move.product_id)
            #     done_qty = sum(lines.mapped('qty_done'))
            #     if not done_qty:
            #         done_qty = sum(lines.mapped('product_uom_qty'))
            #     move_vals = {
            #         'picking_id': picking_id.id,
            #         'picking_type_id': order.picking_type_id.id,
            #         'name': move.name,
            #         'product_id': move.product_id.id,
            #         'product_uom': move.product_uom.id,
            #         'product_uom_qty': done_qty,
            #         'location_id': order.location_id,
            #         'location_dest_id': order.virtual_loaction,
            #         'company_id': order.company_id.id
            #     }
            #     self.env['stock.move'].sudo().create(move_vals)
            # if picking_id:
            #     picking_id.sudo().action_confirm()
            #     picking_id.sudo().action_assign()




    def confirm_validation(self):
        if self.location_dest_id:
            for i in self.move_line_ids:
                i.location_id = self.virtual_loaction.id
                i.location_dest_id = self.location_dest_id.id

        for order in self:
            order.write({
                'tmp_source_loaction': order.location_id,
                'location_id': order.virtual_loaction,
                'state': 'validate_confirm'
            })



            # order.tmp_source_loaction = order.location_id
            #
            # order.location_id = order.virtual_loaction
            #
            #
            # order.state = 'validate_confirm'



