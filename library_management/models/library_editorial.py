from odoo import models, fields


class LibraryEditorial(models.Model):
    _name = 'library.editorial'
    _description = 'Editorial'

    name = fields.Char(string='Nombre de la editorial', required=True)
    country = fields.Char(string='País')
    phone = fields.Char(string='Número telefónico')