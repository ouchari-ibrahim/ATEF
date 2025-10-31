from odoo import models, fields, api




class InheritSaleOrder(models.Model):
    _inherit = 'sale.order'

    def print_report(self):
        # Assurez-vous qu'il y a un seul enregistrement pour générer le rapport
        self.ensure_one()

        # Récupérez le rapport depuis l'identifiant
        report = self.env.ref('nn_custom_report.action_devis_template')

        # Générez le rapport pour l'enregistrement actuel
        return report.report_action(self)
