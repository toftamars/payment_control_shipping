# -*- coding: utf-8 -*-
from odoo import api, fields, models

PARAM = 'payment_control_shipping.enabled'


class PaymentControlToggleWizard(models.TransientModel):
    _name = 'payment.control.toggle.wizard'
    _description = 'Ödeme Kontrolü (Aç/Kapat)'

    enabled = fields.Boolean(string='Ödeme Kontrollü Sevkiyat Aktif')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        param = self.env['ir.config_parameter'].sudo().get_param(PARAM)
        res['enabled'] = (not param) or \
            str(param).strip().lower() not in ('false', '0')
        return res

    def action_apply(self):
        self.ensure_one()
        self.env['ir.config_parameter'].sudo().set_param(
            PARAM, 'True' if self.enabled else 'False')
        return {'type': 'ir.actions.act_window_close'}
