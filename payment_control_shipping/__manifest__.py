# -*- coding: utf-8 -*-
{
    'name': 'Ödeme Kontrollü Sevkiyat',
    'version': '15.0.2.4.0',
    'category': 'Inventory/Delivery',
    'summary': 'Ödemesi tamamlanmamış müşteri siparişlerinin sevkiyatını engeller',
    'author': 'Zuhal Müzik',
    'depends': ['stock', 'sale_stock', 'account', 'mail'],
    'data': [
        'security/payment_control_groups.xml',
        'data/mail_template_payment_approval.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
