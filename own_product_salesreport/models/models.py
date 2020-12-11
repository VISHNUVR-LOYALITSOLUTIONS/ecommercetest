# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Own_productsales(models.TransientModel):
    _name = "own.product.sales.report"
    _description = "Own Product Sales Report"


    operating_unit= fields.Many2one('operating.unit', string='Branch',
                                 default=lambda self: self.env.user.default_operating_unit_id)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date(string='End Date')
    target_move = fields.Boolean(default=False)


    def check_report(self):

        # self.ensure_one()
        # data = {'ids': self.env.context.get('active_ids', [])}
        # res = self.read()
        # res = res and res[0] or {}
        # data.update({'form': res})
        self.ensure_one()
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'sale.order'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('own_product_salesreport.action_report_own_product').report_action(self, data=datas)


    def export_xls(self):

        # self.ensure_one()
        #
        # active_record = self._context['active_id']
        # record = self.env['sale.order'].browse(active_record)
        #
        # datas = {
        #     'ids': self.ids,
        #     'model': self._name,
        #     'record': record.id,
        # }
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'sale.order'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]

        return self.env.ref('own_product_salesreport.action_own_product_xls').report_action(self, data=datas)
