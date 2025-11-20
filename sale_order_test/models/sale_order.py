from odoo import models, fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    x_validez=fields.Selection([
        ('7_dias', '7 días'),
        ('15_dias', '15 días'),
        ('30_dias', '30 días'),
        ('45_dias', '45 días'),
        ('60_dias', '60 días'),
    ],string='Validez',help='Período de validez de la cotización',default='15_dias')

    x_metodo_pago=fields.Selection([
        ('credito', 'Crédito'),
        ('debito', 'Débito'),
        ('efectivo', 'Efectivo'),
    ],string='Método de Pago',default='credito',help='Método de pago acordado con el cliente')

    x_nota_cotizacion=fields.Char(string='Nota de Cotización',help='Notas adicionales para la cotización')

    x_tabla_amortizacion=fields.Html(string='Tabla de Amortización',help='Detalles de la tabla de amortización para pagos a crédito',compute='_compute_tabla_amortizacion',store=False)

    @api.depends('x_validez')
    def _compute_tabla_amortizacion(self):
        for record in self:
            dias = 0

            if record.x_validez == '7_dias':
                dias = 7
            elif record.x_validez == '15_dias':
                dias = 15
            elif record.x_validez == '30_dias':
                dias = 30
            elif record.x_validez == '45_dias':
                dias = 45
            elif record.x_validez == '60_dias':
                dias = 60
            
            if dias==0:
                record.x_tabla_amortizacion = ""
                continue

            tabla=""""
            <table style="width: 50%; border-collapse: collapse;" border="1">
                <tr style="background-color: #f2f2f2;">
                    <th>Día</th>
                    <th>Saldo</th>
                </tr>
            """

            saldo= record.amount_total or 0.0
            pago_diario = saldo / dias if dias > 0 else 0.0

            for x in range(1, dias + 1):
                saldo_restante = saldo - (pago_diario*x)
                tabla += f"""
                <tr>
                    <td style="padding: 5px;">{x}</td>
                    <td style="padding: 5px;">{saldo_restante:.2f}</td>
                </tr>
                """

            tabla += "</table>"
            record.x_tabla_amortizacion = tabla