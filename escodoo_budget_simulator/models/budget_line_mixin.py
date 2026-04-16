# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class BudgetLineMixin(models.AbstractModel):
    """Mixin for budget line models (modules, integrations, and lines).

    This mixin provides common fields and methods for budget line models.
    It centralizes the calculation logic for final hours, including complexity
    and an optional Python formula defined on the catalog (master) record.

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
        "with the complexity factor and optional catalog formula applied.",
    )
    final_hours = fields.Float(
        compute="_compute_final_hours",
        store=True,
        digits=(16, 2),
        help="Final calculated hours for this line. By default this is "
        "base_hours × complexity_factor, where base hours are the adjusted "
        "hours (if > 0) or the default hours from the catalog. If the catalog "
        "defines a Python hours formula, that expression is evaluated instead "
        "and its numeric result is used as the final hours.",
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

        Not applied automatically to final hours; exposed for optional use inside
        catalog ``hours_formula`` expressions (``users_factor``).

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

        Not applied automatically to final hours; exposed for optional use inside
        catalog ``hours_formula`` expressions (``company_factor``).

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

    def _eval_hours_formula(self, formula, eval_locals):
        """Evaluate a catalog hours formula with safe_eval.

        The expression must evaluate to a number (final hours for the line).

        Args:
            formula (str): Python expression.
            eval_locals (dict): Names available in the expression.

        Returns:
            float: Evaluated final hours.

        Raises:
            UserError: If evaluation fails or the result is not numeric.
        """
        self.ensure_one()
        line_label = getattr(self, "name", None) or ""
        if not line_label:
            line_label = f"{self._name},{self.id}"
        try:
            result = safe_eval(
                formula.strip(),
                None,
                eval_locals,
                mode="eval",
                nocopy=True,
            )
        except Exception as err:
            # from None: avoid chaining safe_eval errors (e.g. ZeroDivisionError)
            # so test runners and logs do not treat the cause as an uncaught ERROR.
            raise UserError(
                _(
                    "Invalid hours formula for line %(name)s: %(error)s\n\n"
                    "Formula:\n%(formula)s"
                )
                % {
                    "name": line_label,
                    "error": str(err),
                    "formula": formula.strip()[:500],
                }
            ) from None

        try:
            return float(result)
        except (TypeError, ValueError):
            raise UserError(
                _(
                    "Hours formula for line %(name)s must evaluate to a number; "
                    "got %(value)r.\n\nFormula:\n%(formula)s"
                )
                % {
                    "name": line_label,
                    "value": result,
                    "formula": formula.strip()[:500],
                }
            ) from None

    def _finalize_line_hours(
        self, complexity, users_qty, company_qty, base_hours, hours_formula
    ):
        """Apply default scaling and optional catalog formula.

        When ``hours_formula`` is empty, returns base_hours × complexity_factor.
        Otherwise evaluates the formula; its result is the final hours.

        Args:
            complexity (str): low / medium / high.
            users_qty (int): informational count (available in formula).
            company_qty (int): informational count (available in formula).
            base_hours (float): adjusted or default hours.
            hours_formula (str or bool): optional expression from catalog.

        Returns:
            float: Final hours for the line.
        """
        complexity_factor = self._get_complexity_factor(complexity)
        default_hours = base_hours * complexity_factor
        if not hours_formula or not str(hours_formula).strip():
            return default_hours

        users_factor = self._get_users_factor(users_qty)
        company_factor = self._get_company_factor(company_qty)
        eval_locals = {
            "base_hours": base_hours,
            "complexity": complexity,
            "complexity_factor": complexity_factor,
            "default_hours": default_hours,
            "users_qty": users_qty,
            "company_qty": company_qty,
            "users_factor": users_factor,
            "company_factor": company_factor,
            "min": min,
            "max": max,
            "int": int,
            "float": float,
            "round": round,
        }
        return self._eval_hours_formula(hours_formula, eval_locals)
