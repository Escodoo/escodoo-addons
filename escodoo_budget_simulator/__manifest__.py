# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Escodoo Budget Simulator",
    "summary": """
        Simulate Odoo implementation budgets with templates, hours and cost estimation""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/escodoo-addons",
    "depends": [
        "base",
        "contacts",
        "mail",
        "sales_team",
        "sale",
    ],
    "data": [
        "security/budget_security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/res_config_settings_views.xml",
        "views/budget_template_views.xml",
        "views/budget_integration_views.xml",
        "views/budget_module_views.xml",
        "views/budget_line_views.xml",
        "views/budget_simulation_views.xml",
        "views/budget_simulation_create_template_wizard_views.xml",
        "views/budget_menu.xml",
        "report/budget_simulation_report.xml",
    ],
    "demo": [
        "demo/demo_data.xml",
    ],
    "test": [
        "tests/test_budget_simulation.py",
    ],
    "installable": True,
    "application": True,
}
