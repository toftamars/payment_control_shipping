# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

APPROVER_GROUP = 'payment_control_shipping.group_shipping_approver'


class PaymentControlApprovalWizard(models.TransientModel):
    _name = 'payment.control.approval.wizard'
    _description = 'Ödeme Onayı İste'

    order_id = fields.Many2one(
        'sale.order', string='Sipariş', required=True, readonly=True)
    available_approver_ids = fields.Many2many(
        'res.users', string='Uygun Onaycılar',
        compute='_compute_available_approver_ids')
    approver_ids = fields.Many2many(
        'res.users', string='Onay İstenecek Kişiler',
        help="Onay talebinin (mail + SMS + bildirim) gönderileceği "
             "Sevkiyat Onaycısı kullanıcıları seçin.")

    @api.depends('order_id')
    def _compute_available_approver_ids(self):
        group = self.env.ref(APPROVER_GROUP, raise_if_not_found=False)
        members = group.users if group else self.env['res.users']
        for wizard in self:
            wizard.available_approver_ids = members

    def action_send_request(self):
        self.ensure_one()
        if not self.approver_ids:
            raise UserError(_("En az bir onaycı seçmelisiniz."))
        self.order_id._process_approval_request(self.approver_ids)
        return {'type': 'ir.actions.act_window_close'}
