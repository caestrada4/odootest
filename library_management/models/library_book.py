from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    isbn = fields.Char(string='ISBN')
    published_date = fields.Date(string='Published Date')
    pages = fields.Integer(string='Number of Pages')
    description = fields.Text(string='Description')
    available=fields.Boolean(string='Disponible', default=True)