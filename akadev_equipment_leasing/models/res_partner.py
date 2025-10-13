# models/rental_order.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_client_location = fields.Boolean(
        string='Client Location',
        help='Ce partenaire peut louer des équipements',store=True
    )
    testing = fields.Boolean(
        string='Client Location',
        help='Ce partenaire peut louer des équipements',store=True
    )

    is_supplier = fields.Boolean(
        string='Fournisseur',
        help='Ce partenaire est un fournisseur',store=True
    )

    rental_count = fields.Integer(
        string='Nombre de Locations',
        compute='_compute_rental_count',store=True
    )
    rental_config_ids = fields.One2many(
        'res.partner.rental.config',
        'partner_id',
        string='Rental Configurations'
    )
    def _compute_rental_count(self):
        for partner in self:
            partner.rental_count = self.env['rental.order'].search_count([
                ('partner_id', '=', partner.id)
            ])

    def action_view_rentals(self):
        """Voir les locations du client"""
        return {
            'name': _('Locations'),
            'type': 'ir.actions.act_window',
            'res_model': 'rental.order',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id}
        }