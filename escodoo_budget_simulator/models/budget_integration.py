# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BudgetIntegration(models.Model):
    """Budget Integration Catalog.

    This model stores the catalog of integrations that can be used in budget
    templates and simulations. Each integration has a default number of hours
    that represents the typical implementation time for that integration.

    Integrations from this catalog can be added to budget templates and
    simulations, and the default hours can be adjusted per template or
    simulation as needed.
    """

    _name = "budget.integration"
    _description = "Budget Integration Catalog"
    _order = "name"

    # Fields
    name = fields.Char(
        required=True,
        help="Display name of the integration (e.g., 'NFe', 'NFS-e', "
        "'CNAB Receivables'). This is the name that will appear in selection "
        "dropdowns and reports.",
    )
    code = fields.Char(
        required=True,
        help="Unique code for this integration (e.g., 'nfe', 'nfse', "
        "'cnab_receivable'). This code is used internally to identify the "
        "integration and must be unique across all integrations.",
    )
    default_hours = fields.Float(
        default=0.0,
        digits=(16, 2),
        help="Default number of implementation hours for this integration. "
        "This value represents the typical time required to implement and "
        "configure this integration. It can be adjusted per template or "
        "simulation as needed. Final line hours use the complexity factor on "
        "this base, or a Python hours formula when defined below.",
    )
    hours_formula = fields.Text(
        string="Hours formula (Python)",
        help="Optional Python expression evaluated to obtain final hours for "
        "this catalog item on a budget line. If empty, hours are "
        "base_hours × complexity_factor. If set, the expression must evaluate "
        "to a number (the line's final hours). Available names: base_hours, "
        "complexity, complexity_factor, default_hours (base × complexity), "
        "users_qty, company_qty, users_factor, company_factor, min, max, int, "
        "float, round.",
    )
    active = fields.Boolean(
        default=True,
        help="If unchecked, this integration will be hidden and cannot be "
        "selected in new budget templates or simulations.",
    )
    sequence = fields.Integer(
        default=10,
        help="Sequence number for ordering integrations. Lower numbers appear "
        "first in selection dropdowns and lists.",
    )
    description = fields.Text(
        help="Detailed description of this integration. Use this field to "
        "document what the integration does, its main features, or any special "
        "considerations for implementation.",
    )

    # Constraints
    _sql_constraints = [
        (
            "code_unique",
            "UNIQUE(code)",
            "Integration code must be unique!",
        ),
    ]
