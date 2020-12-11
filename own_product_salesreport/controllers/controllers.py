# -*- coding: utf-8 -*-
# from odoo import http


# class OwnProductSalesreport(http.Controller):
#     @http.route('/own_product_salesreport/own_product_salesreport/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/own_product_salesreport/own_product_salesreport/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('own_product_salesreport.listing', {
#             'root': '/own_product_salesreport/own_product_salesreport',
#             'objects': http.request.env['own_product_salesreport.own_product_salesreport'].search([]),
#         })

#     @http.route('/own_product_salesreport/own_product_salesreport/objects/<model("own_product_salesreport.own_product_salesreport"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('own_product_salesreport.object', {
#             'object': obj
#         })
