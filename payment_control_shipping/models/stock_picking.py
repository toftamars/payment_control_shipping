# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        self._check_payment_before_delivery()
        return super().button_validate()

    def _check_payment_before_delivery(self):
        bypass_group = 'payment_control_shipping.group_bypass_payment_check'

        for picking in self:
            if self.env.user.has_group(bypass_group):
                continue
            if picking.picking_type_id.code != 'outgoing':
                continue
            sale_order = picking.sale_id
            if not sale_order:
                continue
            invoices = sale_order.invoice_ids.filtered(
                lambda m: m.move_type == 'out_invoice' and m.state == 'posted'
            )
            if not invoices:
                raise UserError(_(
                    "%s siparişi için henüz fatura kesilmemiş / ödeme "
                    "alınmamış. Ödeme alınmadan sevkiyat doğrulanamaz."
                ) % sale_order.name)
            unpaid = invoices.filtered(
                lambda m: m.payment_state not in ('paid', 'in_payment')
            )
            if unpaid:
                raise UserError(_(
                    "%s siparişinin ödemesi tam olarak tamamlanmamış. "
                    "Sevkiyat doğrulanamaz.\n\nBekleyen fatura(lar): %s"
                ) % (sale_order.name, ', '.join(unpaid.mapped('name'))))
