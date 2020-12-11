# -*- coding: utf-8 -*-
# from odoo import http


# class StockPickingSecurity(http.Controller):
#     @http.route('/stock_picking_security/stock_picking_security/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_security/stock_picking_security/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_security.listing', {
#             'root': '/stock_picking_security/stock_picking_security',
#             'objects': http.request.env['stock_picking_security.stock_picking_security'].search([]),
#         })

#     @http.route('/stock_picking_security/stock_picking_security/objects/<model("stock_picking_security.stock_picking_security"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_security.object', {
#             'object': obj
#         })
