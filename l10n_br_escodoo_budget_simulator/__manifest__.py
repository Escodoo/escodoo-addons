# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Brazilian Localization Escodoo Budget Simulator",
    "summary": "Fill fiscal operation on quotations created from budget simulations",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/escodoo-addons",
    "depends": [
        "escodoo_budget_simulator",
        "l10n_br_fiscal",
        "l10n_br_sale",
    ],
    "data": [
        "views/res_company_views.xml",
    ],
    "test": [
        "tests/test_budget_simulation_quotation_fiscal.py",
    ],
    "installable": True,
    "application": False,
}
