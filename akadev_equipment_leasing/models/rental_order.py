# models/rental_order.py
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class RentalOrder(models.Model):
    _name = 'rental.order'
    _description = 'Commande de Location'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'


    name = fields.Char(
        string='Référence',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: '/'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        domain=[('is_client_location', '=', True)],
        tracking=True
    )
    picking_id = fields.Many2one('stock.picking', string='Bon de livraison')
    rental_category_id = fields.Many2one(
        'rental.order.category',
        string='Catégorie de Location',
        help="Catégorie principale de la commande"
    )

    rental_order_tag_id = fields.Many2one(
        'rental.order.tag',  # the model for your tags
        string="Étiquette de Location",
        help="Étiquette principale de la commande"
    )

    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('rented', 'Loué'),
        ('partial_returned', 'Partiellement Retourné'),
        ('returned', 'Retourné'),
        ('cancelled', 'Annulé')
    ], string='État', default='draft', tracking=True)

    company_id = fields.Many2one(
        'res.company',
        string='Société',
        required=True,
        default=lambda self: self.env.company
    )

    order_date = fields.Datetime(
        string='Date de Commande',
        default=fields.Datetime.now,
        required=True,
        tracking=True
    )

    rental_line_ids = fields.One2many(
        'rental.order.line',
        'order_id',
        string='Lignes de Location'
    )

    notes = fields.Text(string='Notes')

    # Champs calculés
    total_amount = fields.Monetary(
        string='Montant Total',
        compute='_compute_total_amount',
        store=True,
        currency_field='currency_id'
    )

    currency_id = fields.Many2one(
        'res.currency',
        string='Devise',
        default=lambda self: self.env.company.currency_id
    )

    late_lines_count = fields.Integer(
        string='Lignes en Retard',
        compute='_compute_late_lines',
        store=True
    )

    has_late_lines = fields.Boolean(
        string='A des Retards',
        compute='_compute_late_lines',
        store=True
    )

    @api.model
    def create(self, vals):
        if isinstance(vals, list):
            # Multiple records creation
            for v in vals:
                if v.get('name', '/') == '/':
                    v['name'] = self.env['ir.sequence'].next_by_code('rental.order') or '/'
        else:
            # Single record creation
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('rental.order') or '/'
        return super(RentalOrder, self).create(vals)

    @api.depends('rental_line_ids.rental_price', 'rental_line_ids.extra_charge')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(line.rental_price + line.extra_charge
                                     for line in order.rental_line_ids)

    @api.depends('rental_line_ids.is_late')
    def _compute_late_lines(self):
        for order in self:
            late_lines = order.rental_line_ids.filtered('is_late')
            order.late_lines_count = len(late_lines)
            order.has_late_lines = bool(late_lines)

    def action_confirm(self):
        """Confirmer la commande de location"""
        for order in self:
            if not order.rental_line_ids:
                raise UserError(_('Vous devez ajouter au moins une ligne de location.'))

            for line in order.rental_line_ids:
                if not line.rental_start_date:
                    raise UserError(_('La date de début est obligatoire pour toutes les lignes.'))

            order.state = 'confirmed'
            order.message_post(body=_('Commande de location confirmée.'))

    def action_deliver(self):
        """Livrer les équipements (Pickup)"""
        StockPicking = self.env['stock.picking']
        StockMove = self.env['stock.move']

        for order in self:
            if not order.state != 'draft':
                raise UserError(_('Seules les commandes confirmées peuvent être livrées.'))

            if order.picking_id:
                raise UserError(_('Un bon de livraison existe déjà pour cette commande.'))

            picking_type = self.env.ref('stock.picking_type_out', raise_if_not_found=False)
            if not picking_type:
                raise UserError(_('Le type de transfert sortant (Livraison) est introuvable.'))

            picking_vals = {
                'partner_id': order.partner_id.id,
                'picking_type_id': picking_type.id,
                'origin': order.name,
                'rental_id': order.id,  # link picking -> rental
                'location_id': picking_type.default_location_src_id.id,
                'location_dest_id': order.partner_id.property_stock_customer.id,
            }
            picking = StockPicking.create(picking_vals)

            for line in order.rental_line_ids:
                StockMove.create({
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'product_uom': line.product_id.uom_id.id,
                    'picking_id': picking.id,
                    'location_id': picking.location_id.id,
                    'location_dest_id': picking.location_dest_id.id,
                })

            order.picking_id = picking.id
            order.state = 'rented'
            order.message_post(body=_('Équipements livrés au client. Bon de livraison : %s') % picking.name)

    def action_return_partial(self):
        """Retour partiel d'équipements"""
        self.state = 'partial_returned'
        self.message_post(body=_('Retour partiel d\'équipements effectué.'))

    def action_return_complete(self):
        """Retour complet de tous les équipements"""
        for order in self:
            # Vérifier que tous les équipements sont retournés
            unreturned_lines = order.rental_line_ids.filtered(lambda l: not l.returned)
            if unreturned_lines:
                raise UserError(_('Tous les équipements doivent être retournés avant de clôturer la commande.'))

            order.state = 'returned'
            order.message_post(body=_('Tous les équipements ont été retournés.'))

    def action_cancel(self):
        """Annuler la commande"""
        self.state = 'cancelled'
        self.message_post(body=_('Commande de location annulée.'))

    @api.model
    def check_late_rentals(self):
        """Méthode CRON pour vérifier les retards"""
        late_lines = self.env['rental.order.line'].search([
            ('rental_end_date', '<', fields.Datetime.now()),
            ('returned', '=', False),
            ('order_id.state', 'in', ['rented', 'partial_returned'])
        ])

        for line in late_lines:
            if not line.is_late:
                line._send_late_notification()
