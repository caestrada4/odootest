from odoo import models, fields,api

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

    price = fields.Float(string='Precio', compute='_compute_price', store=True)

    editorial_id = fields.Many2one('library.editorial',string='Editorial',help='Editorial del libro')

    @api.depends('published_date')
    def _compute_price(self):
        today = fields.Date.today()
        for record in self:
            if record.published_date:
                years=today.year - record.published_date.year
                if (today.month, today.day) < (record.published_date.month, record.published_date.day):
                    years -= 1
                record.price = max(years,0)
            else:
                record.price = 0.0
