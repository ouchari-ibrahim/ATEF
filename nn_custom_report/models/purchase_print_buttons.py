from odoo import models, fields, api



class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def print_report(self):
        # Assurez-vous qu'il y a un seul enregistrement pour générer le rapport
        self.ensure_one()

        # Récupérez le rapport depuis l'identifiant
        report = self.env.ref('nn_custom_report.action_report_purchase_order')

        # Générez le rapport pour l'enregistrement actuel
        return report.report_action(self)
