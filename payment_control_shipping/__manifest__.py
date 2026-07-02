# -*- coding: utf-8 -*-
{
    'name': 'Ödeme Kontrollü Sevkiyat',
    'version': '15.0.2.9.0',
    'category': 'Inventory/Delivery',
    'summary': 'Ödemesi tamamlanmamış müşteri siparişlerinin sevkiyatını engeller',
    'author': 'Zuhal Müzik',
    'depends': ['stock', 'sale_stock', 'account', 'mail', 'sms'],
    'data': [
        'security/payment_control_groups.xml',
        'security/ir.model.access.csv',
        'data/mail_template_payment_approval.xml',
        'wizards/payment_control_approval_wizard_views.xml',
        'wizards/payment_control_decision_wizard_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
