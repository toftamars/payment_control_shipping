# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    payment_control_enabled = fields.Boolean(
        string='Ödeme Kontrollü Sevkiyat Aktif',
        default=True,
        config_parameter='payment_control_shipping.enabled',
        help="Kapatılırsa ödeme/fatura kontrolü tüm sevkiyatlarda geçici "
             "olarak devre dışı kalır (kriz modu).")
