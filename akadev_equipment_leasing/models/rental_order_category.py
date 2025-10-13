# models/rental_order.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)

# models/rental_product_category.py
class RentalCategory(models.Model):
    _name = 'rental.order.category'
    _description = 'Catégorie d\'Équipements'
    _order = 'name'

    name = fields.Char(string='Nom', required=True)
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Société',
                               default=lambda self: self.env.company)
