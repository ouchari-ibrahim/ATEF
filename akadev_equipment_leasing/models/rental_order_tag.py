# models/rental_order.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)
# models/rental_product_tag.py
class RentalTag(models.Model):
    _name = 'rental.order.tag'
    _description = 'Étiquette d\'Équipement'
    _order = 'name'

    name = fields.Char(string='Nom', required=True)
    color = fields.Integer(string='Couleur')
    company_id = fields.Many2one('res.company', string='Société',
                               default=lambda self: self.env.company)
