# -*- coding: utf-8 -*-
# from odoo import http


# class SaleProductPack(http.Controller):
#     @http.route('/sale_product_pack/sale_product_pack/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_product_pack/sale_product_pack/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_product_pack.listing', {
#             'root': '/sale_product_pack/sale_product_pack',
#             'objects': http.request.env['sale_product_pack.sale_product_pack'].search([]),
#         })

#     @http.route('/sale_product_pack/sale_product_pack/objects/<model("sale_product_pack.sale_product_pack"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_product_pack.object', {
#             'object': obj
#         })
