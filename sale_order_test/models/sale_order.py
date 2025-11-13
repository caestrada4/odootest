from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    x_validez=fields.Selection([
        ('7_dias', '7 días'),
        ('15_dias', '15 días'),
        ('30_dias', '30 días'),
    ],string='Validez',help='Período de validez de la cotización',default='15_dias')

    x_metodo_pago=fields.Selection([
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('efectivo', 'Efectivo'),
    ],string='Método de Pago',default='credito',help='Método de pago acordado con el cliente')

    x_nota_cotizacion=fields.Char(string='Nota de Cotización',help='Notas adicionales para la cotización')