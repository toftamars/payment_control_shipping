# -*- coding: utf-8 -*-
from odoo import fields, models


class PaymentControlDecisionWizard(models.TransientModel):
    _name = 'payment.control.decision.wizard'
    _description = 'Ödeme Onay Kararı'

    order_id = fields.Many2one(
        'sale.order', string='Sipariş', required=True, readonly=True)
    note = fields.Text(string='Açıklama', required=True)

    def action_approve(self):
        self.ensure_one()
        self.order_id._apply_payment_decision('approve', self.note)
        return {'type': 'ir.actions.act_window_close'}

    def action_reject(self):
        self.ensure_one()
        self.order_id._apply_payment_decision('reject', self.note)
        return {'type': 'ir.actions.act_window_close'}
