# -*- coding: utf-8 -*-
# from odoo import http


# class OnproductChecking(http.Controller):
#     @http.route('/onproduct_checking/onproduct_checking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/onproduct_checking/onproduct_checking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('onproduct_checking.listing', {
#             'root': '/onproduct_checking/onproduct_checking',
#             'objects': http.request.env['onproduct_checking.onproduct_checking'].search([]),
#         })

#     @http.route('/onproduct_checking/onproduct_checking/objects/<model("onproduct_checking.onproduct_checking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('onproduct_checking.object', {
#             'object': obj
#         })
