
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    rentable = fields.Boolean(
        related='product_tmpl_id.rentable',
        string='Louable',
        help='Ce produit peut être loué'
    )

    rental_category_id = fields.Many2one(
        related='product_tmpl_id.rental_category_id',
        string='Catégorie Location'
    )

    rental_tag_ids = fields.Many2many(
        related='product_tmpl_id.rental_tag_ids',
        string='Étiquettes Location'
    )

    daily_rental_price = fields.Monetary(
        related='product_tmpl_id.daily_rental_price',

        string='Prix Location/Jour',
        currency_field='currency_id'
    )