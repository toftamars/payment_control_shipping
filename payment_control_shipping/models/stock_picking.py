# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

APPROVER_GROUP = 'payment_control_shipping.group_shipping_approver'


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    payment_control_approval_state = fields.Selection(
        related='sale_id.payment_control_approval_state',
        string='Ödeme Onay Durumu', readonly=True)
    payment_control_is_approver = fields.Boolean(
        string='Onaycı mı?', compute='_compute_payment_control_is_approver')

    @api.depends_context('uid')
    def _compute_payment_control_is_approver(self):
        is_approver = self.env.user.has_group(APPROVER_GROUP)
        for picking in self:
            picking.payment_control_is_approver = is_approver

    def button_validate(self):
        self._check_payment_before_delivery()
        try:
            return super().button_validate()
        except Exception:
            # TEŞHİS: gizlenen gerçek hatayı tam traceback ile log'a düşür.
            _logger.exception(
                "payment_control_shipping TEŞHİS: super().button_validate() "
                "içinde hata (pickings=%s)", self.ids)
            raise

    def _check_payment_before_delivery(self):
        is_approver = self.env.user.has_group(APPROVER_GROUP)
        for picking in self:
            if picking.picking_type_id.code != 'outgoing':
                continue
            sale_order = picking.sale_id
            if not sale_order:
                continue
            # Sevkiyat Onaycısı grubundaki kullanıcı ödeme kontrolünü
            # doğrudan geçebilir; onay istemesine gerek yoktur.
            if is_approver:
                continue
            if sale_order.payment_control_approval_state == 'approved':
                continue
            invoices = sale_order.invoice_ids.filtered(
                lambda m: m.move_type == 'out_invoice' and m.state == 'posted'
            )
            if not invoices:
                raise UserError(_(
                    "%s siparişi için henüz fatura kesilmemiş / ödeme "
                    "alınmamış. Ödeme alınmadan sevkiyat doğrulanamaz.\n\n"
                    "Onay gerekiyorsa 'Ödeme Onayı İste' butonunu kullanın."
                ) % sale_order.name)
            unpaid = invoices.filtered(
                lambda m: m.payment_state not in ('paid', 'in_payment')
            )
            if unpaid:
                raise UserError(_(
                    "%s siparişinin ödemesi tam olarak tamamlanmamış. "
                    "Sevkiyat doğrulanamaz.\n\nBekleyen fatura(lar): %s\n\n"
                    "Onay gerekiyorsa 'Ödeme Onayı İste' butonunu kullanın."
                ) % (sale_order.name, ', '.join(unpaid.mapped('name'))))

    def action_request_payment_approval(self):
        orders = self.mapped('sale_id')
        if orders:
            orders.action_request_payment_approval()
        return True

    def action_approve_payment_control(self):
        orders = self.mapped('sale_id')
        if orders:
            orders.action_approve_payment_control()
        return True
