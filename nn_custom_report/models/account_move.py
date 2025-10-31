from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    def action_invoice_print(self):
        """Print the invoice and mark it as sent, so that we can see more
        easily the next step of the workflow.
        """
        if any(not move.is_invoice(include_receipts=True) for move in self):
            raise UserError(_("Only invoices can be printed."))

        self.filtered(lambda inv: not inv.is_move_sent).write({'is_move_sent': True})

        if self.user_has_groups('account.group_account_invoice'):
            return self.env.ref('nn_custom_report.account_invoices').report_action(self)
        else:
            return self.env.ref('nn_custom_report.account_invoices_without_payment').report_action(self)
