# models/rental_order.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


# models/rental_order_line.py
class RentalOrderLine(models.Model):
    _name = 'rental.order.line'
    _description = 'Ligne de Commande de Location'
    _order = 'order_id, id'

    order_id = fields.Many2one(
        'rental.order',
        string='Commande',
        required=True,
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        'product.template',
        string='Équipement',
        required=True,
        domain=[('rentable', '=', True)]
    )

    rental_start_date = fields.Datetime(
        string='Date de Début',
        required=True,
        tracking=True
    )

    rental_end_date = fields.Datetime(
        string='Date de Fin Prévue',
        tracking=True
    )

    return_date = fields.Datetime(
        string='Date de Retour Réelle',
        tracking=True
    )

    returned = fields.Boolean(
        string='Retourné',
        default=False,
        tracking=True
    )

    rental_price = fields.Monetary(
        string='Prix Location',
        currency_field='currency_id'
    )

    extra_charge = fields.Monetary(
        string='Frais Supplémentaires',
        currency_field='currency_id',
        default=0.0
    )

    currency_id = fields.Many2one(
        related='order_id.currency_id',
        string='Devise'
    )

    # Champs de calcul de durée
    rental_duration_days = fields.Integer(
        string='Durée (jours)',
        compute='_compute_rental_duration',
        store=True
    )

    rental_duration_full = fields.Char(
        string='Durée Complète',
        compute='_compute_rental_duration',
        store=True
    )

    # Gestion des retards
    is_late = fields.Boolean(
        string='En Retard',
        compute='_compute_late_status',
        store=True
    )

    late_days = fields.Integer(
        string='Jours de Retard',
        compute='_compute_late_status',
        store=True
    )

    late_hours = fields.Float(
        string='Heures de Retard',
        compute='_compute_late_status',
        store=True
    )

    # Champs techniques
    on_return_date = fields.Datetime(
        string='Horodatage Retour',
        help='Horodatage technique du retour'
    )

    @api.depends('rental_start_date', 'return_date')
    def _compute_rental_duration(self):
        for line in self:
            if line.rental_start_date:
                end_date = line.return_date or fields.Datetime.now()
                delta = end_date - line.rental_start_date

                line.rental_duration_days = delta.days

                # Format complet : Xj Yh Zm
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                line.rental_duration_full = f"{delta.days}j {hours}h {minutes}m"
            else:
                line.rental_duration_days = 0
                line.rental_duration_full = "0j 0h 0m"

    @api.depends('rental_end_date', 'return_date', 'returned')
    def _compute_late_status(self):
        for line in self:
            if line.rental_end_date and not line.returned:
                now = fields.Datetime.now()
                if now > line.rental_end_date:
                    line.is_late = True
                    delta = now - line.rental_end_date
                    line.late_days = delta.days
                    line.late_hours = delta.total_seconds() / 3600
                else:
                    line.is_late = False
                    line.late_days = 0
                    line.late_hours = 0
            else:
                line.is_late = False
                line.late_days = 0
                line.late_hours = 0

    def action_return_equipment(self):
        """Marquer l'équipement comme retourné"""
        for line in self:
            line.returned = True
            line.return_date = fields.Datetime.now()
            line.on_return_date = fields.Datetime.now()

            # Créer le mouvement de stock entrant
            line._create_stock_move_in()

            # Vérifier l'état de la commande
            line.order_id._check_return_status()

            line.order_id.message_post(
                body=_('Équipement %s retourné.') % line.product_id.name
            )

    def _create_stock_move_out(self):
        """Créer mouvement de stock sortant (livraison)"""
        # Logique pour créer les mouvements de stock
        pass

    def _create_stock_move_in(self):
        """Créer mouvement de stock entrant (retour)"""
        # Logique pour créer les mouvements de stock
        pass

    def _send_late_notification(self):
        """Envoyer notification de retard"""
        template = self.env.ref('rental_equipment.email_template_late_rental',
                                raise_if_not_found=False)
        if template:
            template.send_mail(self.id, force_send=True)

        self.order_id.message_post(
            body=_('⚠️ Équipement en retard : %s (retard de %d jours)') %
                 (self.product_id.name, self.late_days)
        )