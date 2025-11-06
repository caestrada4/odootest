{
    'name': 'Partner Risk Fields',
    'version': '1.0.0',
    'summary': 'Añade campos Tipo deudor y Es residente a res.partner',
    'category': 'Custom',
    'author': 'Taller',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
}
