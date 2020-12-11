# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError,AccessError


class Stockpicking(models.Model):
    _inherit = 'stock.picking'




    popup_bool = fields.Boolean("Editing",compute='_compute_restrict_branch',domain="[('picking_type_id.code','=','internal')]")

    def _compute_restrict_branch(self):

        company = self.env.user.operating_unit_ids

        branch = [branches.id for branches in company]

        all = self.env['stock.picking'].search([])



        for i in self:

            if i.picking_type_id.code != 'internal':
                i.popup_bool = False

            elif i.picking_type_id.code == 'internal':
                if i.virtual_loaction:
                    if i.virtual_loaction.operating_unit_id:
                        if i.virtual_loaction.operating_unit_id.id not in branch:
                            i.popup_bool = True
                        else:
                            i.popup_bool = False
                if i.tmp_source_loaction:
                    if i.tmp_source_loaction.operating_unit_id:
                        if i.tmp_source_loaction.operating_unit_id.id not in branch:
                            i.popup_bool = True
                        else:
                            i.popup_bool = False
                if i.location_id:
                    if i.location_id.operating_unit_id:
                        if i.location_id.operating_unit_id.id not in branch:
                            i.popup_bool = True
                        else:
                            i.popup_bool = False
            else:
                pass





                        # if i.virtual_loaction.operating_unit_id:
                        #     if i.virtual_loaction.operating_unit_id.id not in branch:
                        #         i.popup_bool = True
                        # if i.tmp_source_loaction.operating_unit_id:
                        #     if i.tmp_source_loaction.operating_unit_id.id not in branch:
                        #         i.popup_bool = True

                        # def write(self, vals):
    #
    #     # record = super(Stockpicking, self).write(vals)
    #     company = self.env.user.operating_unit_ids
    #
    #     branch = [branches.id for branches in company]
    #
    #     if self.picking_type_id.code=='internal':
    #         if self.virtual_loaction.operating_unit_id:
    #             if self.virtual_loaction.operating_unit_id.id not in branch:
    #                 raise ValidationError(
    #                     _("""The requested operation can not be completed due to security restrictions."""))
    #         if self.tmp_source_loaction.operating_unit_id:
    #             if self.tmp_source_loaction.operating_unit_id.id not in branch:
    #                 raise ValidationError(
    #                     _("""The requested operation can not be completed due to security restrictions."""))
    #         if self.location_id.operating_unit_id:
    #             if self.location_id.operating_unit_id.id not in branch:
    #
    #                 raise ValidationError(
    #                     _("""The requested operation can not be completed due to security restrictions."""))
    #
    #
    #                 # raise UserError(_('Your Transaction Limit Is') )
    #
    #     return super(Stockpicking, self).write(vals)