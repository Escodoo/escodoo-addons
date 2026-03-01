# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Escodoo Budget Simulator CRM",
    "summary": """
        Integration between Budget Simulator and CRM Opportunities""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/escodoo-addons",
    "depends": [
        "escodoo_budget_simulator",
        "crm",
        "sale_crm",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/crm_lead_to_simulation_views.xml",
        "views/crm_lead_views.xml",
        "views/budget_simulation_views.xml",
    ],
    "test": [
        "tests/test_crm_lead_budget_simulation.py",
    ],
    "installable": True,
    "auto_install": False,
}
