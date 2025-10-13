
from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    rental_id = fields.Many2one('rental.order', string='Commande de location')
