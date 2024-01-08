# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    escodoo_primary_interest = fields.Selection(
        [
            ("seeking_erp", "My company is seeking an ERP"),
            ("using_odoo", "My company uses Odoo and needs services or improvements"),
            (
                "external_consultant",
                "I am an external consultant and want to recommend Odoo",
            ),
            ("partnership_opportunity", "Partnership Opportunity"),
        ],
        string="Primary Interest",
    )
    escodoo_has_management_system = fields.Boolean(string="Has Management System?")
    escodoo_management_system_name = fields.Char(string="Management System Name")
    escodoo_company_size = fields.Selection(
        [
            ("micro", "Less than 5 Employees"),
            ("small", "5-20 Employees"),
            ("medium_small", "20-50 Employees"),
            ("medium", "50-100 Employees"),
            ("medium_large", "100-250 Employees"),
            ("large", "More than 250 Employees"),
        ],
        string="Company Size",
    )
    field_name = fields.Selection([("key", "value")], string="field_name")
    escodoo_annual_revenue = fields.Monetary(
        "Annual Revenue", currency_field="company_currency", track_visibility="always"
    )
    escodoo_average_ticket = fields.Monetary(
        "Average Ticket", currency_field="company_currency", track_visibility="always"
    )
    escodoo_technological_maturity = fields.Selection(
        string="Technological Maturity",
        selection=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
    )
    escodoo_has_dedicate_team = fields.Boolean(string="Has Dedicated Team")
    escodoo_project_budget = fields.Monetary(
        "Budget", currency_field="company_currency", track_visibility="always"
    )
    escodoo_project_release_date = fields.Date("Release Date")
    escodoo_project_description = fields.Html(string="General Description")
    escodoo_project_primary_pain = fields.Html(string="Primary Pains")
    escodoo_project_integration = fields.Html(string="Integrations")
