# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BudgetMixin(models.AbstractModel):
    """Mixin for budget template and simulation models.

    This mixin provides common fields and methods for budget models.
    It centralizes the shared logic between budget templates and simulations,
    including complexity factors, user and company quantities, and total hours
    calculation.

    Subclasses should define:
    - module_line_ids (One2many to budget.template.module or budget.simulation.module)
    - integration_line_ids (One2many to budget.template.integration or
      budget.simulation.integration)
    - line_ids (One2many to budget.template.line or budget.simulation.line)
    """

    _name = "budget.mixin"
    _description = "Budget Mixin"

    # Fields
    description = fields.Html(
        help="Detailed description of the budget template or simulation. "
        "This field supports HTML formatting for rich text content.",
    )
    active = fields.Boolean(
        default=True,
        help="If unchecked, this record will be hidden and cannot be used "
        "in new budget simulations or templates.",
    )
    users_qty = fields.Integer(
        string="Number of Users",
        default=5,
        help="Total number of users for this budget. This value is used to "
        "calculate the users factor: 1% per user above 5, with a maximum "
        "increase of 40%. For example, 10 users = +5%, 25 users = +20%, "
        "50 users = +40% (maximum).",
    )
    company_qty = fields.Integer(
        string="Number of Companies",
        default=1,
        help="Total number of companies for this budget. This value is used "
        "to calculate the companies factor: 15% per company above 1, with "
        "no maximum limit. For example, 2 companies = +15%, 3 companies = +30%, "
        "4 companies = +45%, etc.",
    )
    complexity = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        default="medium",
        help="Complexity level for this budget. This affects the complexity "
        "factor applied to all lines: Low = 1.00x, Medium = 1.15x, High = 1.30x. "
        "The complexity factor is multiplied with the base hours of each line.",
    )
    excluded_module_ids = fields.Many2many(
        "budget.module",
        compute="_compute_excluded_ids",
        string="Excluded Modules",
        help="List of modules that are already added to this budget. "
        "These modules are automatically excluded from the selection dropdown "
        "to prevent duplicates.",
    )
    excluded_integration_ids = fields.Many2many(
        "budget.integration",
        compute="_compute_excluded_ids",
        string="Excluded Integrations",
        help="List of integrations that are already added to this budget. "
        "These integrations are automatically excluded from the selection "
        "dropdown to prevent duplicates.",
    )
    total_hours = fields.Float(
        compute="_compute_totals",
        store=True,
        digits=(16, 2),
        help="Total calculated hours for this budget. This is the sum of all "
        "final hours from modules, integrations, and general activities. Each "
        "line's final hours already includes all factors (complexity, users, "
        "and companies).",
    )

    # Methods
    @api.depends("module_line_ids.module_id", "integration_line_ids.integration_id")
    def _compute_excluded_ids(self):
        """Compute excluded module and integration IDs.

        This method collects all modules and integrations that are already
        added to the budget, so they can be excluded from selection dropdowns
        to prevent duplicates.

        Returns:
            None: Updates excluded_module_ids and excluded_integration_ids fields.
        """
        for rec in self:
            rec.excluded_module_ids = rec.module_line_ids.mapped("module_id")
            rec.excluded_integration_ids = rec.integration_line_ids.mapped(
                "integration_id"
            )

    @api.depends(
        "line_ids.final_hours",
        "integration_line_ids.final_hours",
        "module_line_ids.final_hours",
    )
    def _compute_totals(self):
        """Compute total hours from all lines.

        This method sums the final hours from all three types of lines:
        - General activities (line_ids)
        - Integration lines (integration_line_ids)
        - Module lines (module_line_ids)

        Note that each line's final_hours already includes all factors
        (complexity, users, and companies), so we simply sum them.

        Returns:
            None: Updates total_hours field.
        """
        for rec in self:
            # Sum final hours (already includes all factors:
            # complexity, users, companies)
            base_hours = sum(rec.line_ids.mapped("final_hours"))
            integration_hours = sum(rec.integration_line_ids.mapped("final_hours"))
            module_hours = sum(rec.module_line_ids.mapped("final_hours"))

            # Total hours is simply the sum of all final_hours
            # (each final_hours already includes complexity,
            # users, and companies factors)
            rec.total_hours = base_hours + integration_hours + module_hours
