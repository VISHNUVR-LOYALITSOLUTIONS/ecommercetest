# -*- coding: utf-8 -*-
# from odoo import http


# class ProductPack(http.Controller):
#     @http.route('/product_pack/product_pack/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_pack/product_pack/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_pack.listing', {
#             'root': '/product_pack/product_pack',
#             'objects': http.request.env['product_pack.product_pack'].search([]),
#         })

#     @http.route('/product_pack/product_pack/objects/<model("product_pack.product_pack"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_pack.object', {
#             'object': obj
#         })
