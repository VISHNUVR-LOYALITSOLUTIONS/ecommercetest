# -*- coding: utf-8 -*-
# from odoo import http


# class PhygiPurchaseOrderPrint(http.Controller):
#     @http.route('/phygi_purchase_order_print/phygi_purchase_order_print/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/phygi_purchase_order_print/phygi_purchase_order_print/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('phygi_purchase_order_print.listing', {
#             'root': '/phygi_purchase_order_print/phygi_purchase_order_print',
#             'objects': http.request.env['phygi_purchase_order_print.phygi_purchase_order_print'].search([]),
#         })

#     @http.route('/phygi_purchase_order_print/phygi_purchase_order_print/objects/<model("phygi_purchase_order_print.phygi_purchase_order_print"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('phygi_purchase_order_print.object', {
#             'object': obj
#         })
