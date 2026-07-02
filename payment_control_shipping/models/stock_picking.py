# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

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
        return super().button_validate()

    @api.model
    def _payment_control_enabled(self):
        """Kriz modu: Ayarlar'dan kapatılırsa kontrol tamamen devre dışı."""
        param = self.env['ir.config_parameter'].sudo().get_param(
            'payment_control_shipping.enabled')
        if not param:
            return True
        return str(param).strip().lower() not in ('false', '0')

    def _payment_control_block_reason(self, sale_order):
        """Sevkiyatın engellenme sebebini döndürür; engel yoksa boş döner."""
        invoices = sale_order.invoice_ids.filtered(
            lambda m: m.move_type == 'out_invoice' and m.state == 'posted'
        )
        if not invoices:
            return _(
                "%s siparişi için henüz fatura kesilmemiş / ödeme alınmamış. "
                "Ödeme alınmadan sevkiyat doğrulanamaz.\n\n"
                "Onay gerekiyorsa 'Ödeme Onayı İste' butonunu kullanın."
            ) % sale_order.name
        unpaid = invoices.filtered(
            lambda m: m.payment_state not in ('paid', 'in_payment')
        )
        if unpaid:
            return _(
                "%s siparişinin ödemesi tam olarak tamamlanmamış. "
                "Sevkiyat doğrulanamaz.\n\nBekleyen fatura(lar): %s\n\n"
                "Onay gerekiyorsa 'Ödeme Onayı İste' butonunu kullanın."
            ) % (sale_order.name, ', '.join(unpaid.mapped('name')))
        return False

    def _check_payment_before_delivery(self):
        if not self._payment_control_enabled():
            return
        is_approver = self.env.user.has_group(APPROVER_GROUP)
        for picking in self:
            if picking.picking_type_id.code != 'outgoing':
                continue
            sale_order = picking.sale_id
            if not sale_order:
                continue
            if sale_order.payment_control_approval_state == 'approved':
                continue
            reason = picking._payment_control_block_reason(sale_order)
            if not reason:
                continue
            if is_approver:
                # Onaycı doğrudan geçebilir; ama denetim için iz bırakılır.
                picking.message_post(body=_(
                    "Ödeme/fatura tamamlanmadan, onaycı yetkisiyle sevkiyat "
                    "doğrulandı. Doğrulayan: %s"
                ) % self.env.user.name)
                continue
            raise UserError(reason)

    def action_request_payment_approval(self):
        self.ensure_one()
        if not self.sale_id:
            raise UserError(_("Bu transfere bağlı bir satış siparişi yok."))
        return self.sale_id.action_request_payment_approval()

    def action_open_payment_decision(self):
        self.ensure_one()
        if not self.sale_id:
            raise UserError(_("Bu transfere bağlı bir satış siparişi yok."))
        return self.sale_id.action_open_payment_decision()
