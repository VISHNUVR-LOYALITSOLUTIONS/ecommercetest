# -*- coding: utf-8 -*-
# from odoo import http


# class BranchwiseEditingPopup(http.Controller):
#     @http.route('/branchwise_editing_popup/branchwise_editing_popup/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/branchwise_editing_popup/branchwise_editing_popup/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('branchwise_editing_popup.listing', {
#             'root': '/branchwise_editing_popup/branchwise_editing_popup',
#             'objects': http.request.env['branchwise_editing_popup.branchwise_editing_popup'].search([]),
#         })

#     @http.route('/branchwise_editing_popup/branchwise_editing_popup/objects/<model("branchwise_editing_popup.branchwise_editing_popup"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('branchwise_editing_popup.object', {
#             'object': obj
#         })
