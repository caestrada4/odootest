{
    'name': 'Library Management',
    'version': '1.0', 
    'summary': 'Manage library books and members',
    'description': 'A module to manage library books, members, and borrowing activities.',  
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
    ],
    'installable': True,
    'application': True,
}