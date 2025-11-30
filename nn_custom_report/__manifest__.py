{
    "name": "nn_custom_report",
    "version": "19.0.1.0.0",
    "summary": "Personalized Devis/Sales Quotation Report",
    "description": """
This module provides a custom 'Devis' report by extending sale.order (sale.devis) and sale.order.line (devis_line).
It matches the client's PDF template with a tailored header, footer, and field layout.
""",
    "category": "Sales",
    "author": "Your Company",
    "website": "http://www.yourcompany.com",
    "license": "LGPL-3",
    "depends": [
        "sale_management",
        "web","sale",
        "base",
        "purchase",
        "account",
    ],
    "data": [
        # Templates ready
        "reports/header_footer.xml",
        "reports/sale_order_template.xml",
        "reports/purchase_order_template.xml",
        "reports/account_move_template.xml",

        # Report Actions replace or updated
        "reports/sale_order_report_action.xml",
        "reports/sale_order_without_price_template.xml",
        "reports/purchase_order_report_action_replace.xml",
        "reports/purchase_order_without_price_template.xml",

        # Views: Print report button for each model
        # "views/sale_print_buttons.xml",
        # "views/purchase_print_buttons.xml",
    ],
    "assets": {},
    "installable": True,
    "application": True,
    "auto_install": False,
}
