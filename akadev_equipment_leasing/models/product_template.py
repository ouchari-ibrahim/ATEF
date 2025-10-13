from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    rentable = fields.Boolean(
        string='Louable',
        help='Ce produit peut être loué'
    )

    rental_category_id = fields.Many2one(
        'rental.product.category',
        string='Catégorie Location'
    )

    rental_tag_ids = fields.Many2many(
        'rental.product.tag',
        string='Étiquettes Location'
    )

    daily_rental_price = fields.Monetary(
        string='Prix Location/Jour',
        currency_field='currency_id'
    )