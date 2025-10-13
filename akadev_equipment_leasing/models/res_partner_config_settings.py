# models/res_partner_rental_config.py
from odoo import models, fields

class PartnerRentalConfig(models.Model):
    _name = 'res.partner.rental.config'
    _description = "Partner Rental Configuration"

    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True
    )
    rental_location_id = fields.Many2one(
        'stock.location',
        string='Emplacement par Défaut'
    )
    rental_duration = fields.Integer(
        string='Durée par Défaut (jours)',
        default=7
    )
    late_notification_email = fields.Char(
        string='Email Notifications Retard'
    )
