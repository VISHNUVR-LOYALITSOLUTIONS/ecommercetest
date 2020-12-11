# -*- coding: utf-8 -*-
# from odoo import http


# class InternalTransferApproval(http.Controller):
#     @http.route('/internal_transfer_approval/internal_transfer_approval/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/internal_transfer_approval/internal_transfer_approval/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('internal_transfer_approval.listing', {
#             'root': '/internal_transfer_approval/internal_transfer_approval',
#             'objects': http.request.env['internal_transfer_approval.internal_transfer_approval'].search([]),
#         })

#     @http.route('/internal_transfer_approval/internal_transfer_approval/objects/<model("internal_transfer_approval.internal_transfer_approval"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('internal_transfer_approval.object', {
#             'object': obj
#         })
