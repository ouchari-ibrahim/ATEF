# models/rental_order.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


# models/res_config_settings.py
class RentalConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    default_rental_location = fields.Many2one(
        'stock.location',
        string='Emplacement par Défaut'
    )

    default_rental_duration = fields.Integer(
        string='Durée par Défaut (jours)',
        default=7
    )

    late_notification_email = fields.Char(
        string='Email Notifications Retard')