# -*- coding: utf-8 -*-
{
    'name': 'sale_order_test',
    'version': '1.0.0',
    'summary': 'Módulo de prueba: estructura básica para extender sale.order',
    'description': """
Módulo de ejemplo para Odoo 19 Community.

Proporciona la estructura mínima (manifiesto, seguridad, vistas y datos de ejemplo)
para que puedas comenzar a desarrollar extensiones sobre sale.order.
""",
    'author': 'Carlos Andrés Estrada',
    'category': 'Sales',
    'sequence': 10,
    'depends': [
        'sale',
    ],
    'license': 'AGPL-3',
    'data': [
        'views/sale_order_views.xml',

    ],
    'installable': True,
    'application': False,

}
