# -*- coding: utf-8 -*-
# from odoo import http


# class StockProductPack(http.Controller):
#     @http.route('/stock_product_pack/stock_product_pack/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_product_pack/stock_product_pack/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_product_pack.listing', {
#             'root': '/stock_product_pack/stock_product_pack',
#             'objects': http.request.env['stock_product_pack.stock_product_pack'].search([]),
#         })

#     @http.route('/stock_product_pack/stock_product_pack/objects/<model("stock_product_pack.stock_product_pack"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_product_pack.object', {
#             'object': obj
#         })
