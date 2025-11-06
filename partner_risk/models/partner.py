from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    tipo_deudor = fields.Selection(
        [
            ('alto', 'Alto riesgo'),
            ('medio', 'Riesgo medio'),
            ('bajo', 'Bajo Riesgo'),
        ],
        string='Tipo deudor',
        required=True,
        help='Registre el tipo de riesgo que tiene este contacto en cuanto a su nivel de endeudamiento'
    )

    es_residente = fields.Boolean(
        string='Es residente',
        help='Marque si el contacto es residente de su país'
    )
