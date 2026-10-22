# Copyright 2025 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Escodoo Helpdesk Mgmt Custom",
    "summary": """Escodoo Helpdesk Custom""",
    "version": "16.0.1.1.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/escodoo-addons",
    "depends": [
        "helpdesk_mgmt",
        "helpdesk_ticket_related",
        "portal",
        "sales_team",
    ],
    "data": [
        "security/helpdesk_security.xml",
        "security/ir.model.access.csv",
        "wizard/environment_change_views.xml",
        "views/helpdesk_ticket.xml",
        "views/helpdesk_ticket_templates.xml",
        "views/res_partner.xml",
        "views/res_config_settings_views.xml",
    ],
}
