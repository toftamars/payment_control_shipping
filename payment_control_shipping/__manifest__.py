# -*- coding: utf-8 -*-
{
    'name': 'Ödeme Kontrollü Sevkiyat',
    'version': '15.0.1.0.0',
    'category': 'Inventory/Delivery',
    'summary': 'Ödemesi tamamlanmamış müşteri siparişlerinin sevkiyatını engeller',
    'author': 'Zuhal Müzik',
    'depends': ['stock', 'sale_stock', 'account'],
    'data': [
        'security/payment_control_groups.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
