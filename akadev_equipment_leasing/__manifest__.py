# __manifest__.py
{
    'name': 'Location d\'Équipements',
    'version': '19.0.1.0.0',
    'category': 'Sales/Location',
    'summary': 'Module de gestion de location de machines et équipements',
    'description': """
Module Location d'Équipements
=============================

Ce module permet de gérer la location de machines et équipements :
- Gestion complète des commandes de location
- Suivi des étapes : création, confirmation, livraison, retour
- Intégration avec la gestion des stocks
- Suivi automatique des durées et retards
- Notifications et alertes automatiques
- Rapports PDF personnalisés
    """,
    'author': 'Votre Société',
    'website': 'https://www.votresite.com',
    'depends': ['base', 'stock', 'mail'],
    'data': [
        'security/rental_security.xml',
        'security/ir.model.access.csv',
        'data/rental_sequence.xml',
        'data/rental_data.xml',
        'views/rental_order_views.xml',
        'views/rental_order_line_views.xml',
        'views/rental_equipment_views.xml',
        'views/rental_category_views.xml',
        'views/rental_tag_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/rental_config_views.xml',
        'views/rental_menus.xml',
        'reports/rental_reports.xml',
        'reports/rental_delivery_report.xml',
        'reports/rental_return_report.xml',
    ],
    'demo': [
        'demo/rental_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'rental_equipment/static/src/css/rental_style.css',
            'rental_equipment/static/src/js/rental_widget.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}