{
    "name": "Kiosk API Integration",
    "summary": "Module to integrate Kiosk API with Odoo",
    "version": "1.0.0",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/kiosk_views.xml",
    ],
    "installable": True, 
    "application": False,
}