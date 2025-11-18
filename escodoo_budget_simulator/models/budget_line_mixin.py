# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BudgetLineMixin(models.AbstractModel):
    """Mixin for budget line models (modules, integrations, and lines).

    This mixin provides common fields and methods for budget line models.
    It centralizes the calculation logic for final hours, including complexity,
    users, and companies factors.

    Subclasses should define:
    - parent_id field (template_id or simulation_id)
    - catalog_id field (module_id, integration_id, or line_id)
    - related fields (name, code, default_hours) pointing to catalog_id
      OR manual fields (name, category, suggested_hours/base_hours)
    - _compute_final_hours method
    - _get_base_hours method (if different from default)
    """

    _name = "budget.line.mixin"
    _description = "Budget Line Mixin"

    # Fields
    sequence = fields.Integer(
        default=10,
        help="Sequence number for ordering lines. Lower numbers appear first. "
        "Used to control the display order of lines in lists and reports.",
    )
    adjusted_hours = fields.Float(
        default=0.0,
        digits=(16, 2),
        help="Manual adjustment of hours for this line. If set to a value "
        "greater than 0, this value will be used instead of the default hours "
        "from the catalog. Leave as 0 to use the default hours from the catalog. "
        "The adjusted hours are used as the base for calculating final hours "
        "with all factors applied.",
    )
    final_hours = fields.Float(
        compute="_compute_final_hours",
        store=True,
        digits=(16, 2),
        help="Final calculated hours for this line after applying all factors: "
        "complexity, users, and companies. This is calculated as: "
        "base_hours × complexity_factor × users_factor × company_factor. "
        "The base hours are either the adjusted hours (if > 0) or the default "
        "hours from the catalog.",
    )

    # Methods
    def _get_base_hours(self):
        """Get base hours (adjusted or default).

        This method returns the adjusted hours if set (value > 0), otherwise
        returns the default hours from the catalog. Subclasses should define
        the default_hours field.

        Returns:
            float: Base hours to use for calculations.
        """
        return self.adjusted_hours if self.adjusted_hours > 0 else self.default_hours

    @staticmethod
    def _get_complexity_factor(complexity):
        """Get complexity factor based on complexity level.

        Args:
            complexity (str): Complexity level ('low', 'medium', or 'high').

        Returns:
            float: Complexity factor multiplier.
                - Low: 1.00x (no increase)
                - Medium: 1.15x (+15%)
                - High: 1.30x (+30%)
        """
        complexity_factors = {"low": 1.00, "medium": 1.15, "high": 1.30}
        return complexity_factors.get(complexity, 1.00)

    @staticmethod
    def _get_users_factor(users_qty):
        """Get users factor: 1% per user above 5, max +40%.

        The factor increases by 1% for each user above 5, with a maximum
        increase of 40%. For example:
        - 5 users or less: 1.00x (no increase)
        - 10 users: 1.05x (+5%)
        - 25 users: 1.20x (+20%)
        - 50 users or more: 1.40x (+40%, maximum)

        Args:
            users_qty (int): Total number of users.

        Returns:
            float: Users factor multiplier.
        """
        users_factor = 1.0
        if users_qty > 5:
            additional_users = users_qty - 5
            users_factor = 1.0 + min(additional_users * 0.01, 0.40)
        return users_factor

    @staticmethod
    def _get_company_factor(company_qty):
        """Get company factor: 15% per company above 1, no maximum.

        The factor increases by 15% for each company above 1, with no
        maximum limit. For example:
        - 1 company: 1.00x (no increase)
        - 2 companies: 1.15x (+15%)
        - 3 companies: 1.30x (+30%)
        - 4 companies: 1.45x (+45%)
        - And so on...

        Args:
            company_qty (int): Total number of companies.

        Returns:
            float: Company factor multiplier.
        """
        company_factor = 1.0
        if company_qty > 1:
            additional_companies = company_qty - 1
            company_factor = 1.0 + (additional_companies * 0.15)
        return company_factor
