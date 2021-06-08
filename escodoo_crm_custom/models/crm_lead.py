# Copyright 2021 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class CrmLead(models.Model):

    _inherit = 'crm.lead'

    escodoo_company_size = fields.Integer(
        string='Company Size')
    escodoo_annual_revenue = fields.Monetary(
        'Annual Revenue',
        currency_field='company_currency',
        track_visibility='always')
    escodoo_average_ticket = fields.Monetary(
        'Average Ticket',
        currency_field='company_currency',
        track_visibility='always')
    escodoo_technological_maturity = fields.Selection(
        string='Technological Maturity',
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High')
        ],)
    escodoo_has_dedicate_team = fields.Boolean(
        string="Has Dedicated Team")
    escodoo_project_budget = fields.Monetary(
        'Budget',
        currency_field='company_currency',
        track_visibility='always')
    escodoo_project_release_date = fields.Date(
        'Release Date')
    escodoo_project_description = fields.Html(
        string='General Description')
    escodoo_project_pain_primary = fields.Html(
        string='Primary Pains')
    escodoo_project_integration = fields.Html(
        string='Integrations')
