# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class BudgetTemplate(models.Model):
    """Budget Template.

    Budget templates are reusable configurations that can be used to quickly
    create new budget simulations. Templates contain pre-configured modules,
    integrations, and general activities with default values for complexity,
    number of users, and number of companies.

    Templates can be in two states:
    - Draft: Can be edited and modified
    - Confirmed: Locked and cannot be modified (read-only)

    When a template is loaded into a simulation, all its modules, integrations,
    and lines are copied to the simulation, and the default values are applied.
    """

    _name = "budget.template"
    _description = "Budget Template"
    _inherit = ["mail.thread", "mail.activity.mixin", "budget.mixin"]
    _order = "name"

    # Fields
    name = fields.Char(
        required=True,
        tracking=True,
        help="Name of the budget template. This name should be descriptive "
        "and help identify the template's purpose (e.g., 'Standard "
        "Implementation', 'E-commerce Setup', 'Manufacturing Configuration').",
    )
    description = fields.Html(
        help="Detailed description of this budget template. Use this field to "
        "document what scenarios this template is designed for, what modules "
        "and integrations it includes, or any special considerations. "
        "This field supports HTML formatting for rich text content.",
    )
    users_qty = fields.Integer(
        tracking=True,
        help="Default number of users for this template. This value will be "
        "applied when the template is loaded into a simulation, but can be "
        "adjusted in the simulation if needed.",
    )
    company_qty = fields.Integer(
        tracking=True,
        help="Default number of companies for this template. This value will "
        "be applied when the template is loaded into a simulation, but can be "
        "adjusted in the simulation if needed.",
    )
    complexity = fields.Selection(
        tracking=True,
        help="Default complexity level for this template. This value will be "
        "applied when the template is loaded into a simulation, but can be "
        "adjusted in the simulation if needed.",
    )
    integration_line_ids = fields.One2many(
        "budget.template.integration",
        "template_id",
        string="Integrations",
        copy=True,
        help="List of integrations included in this template. These "
        "integrations will be copied to simulations when the template is loaded. "
        "Each integration can have its hours adjusted per template.",
    )
    module_line_ids = fields.One2many(
        "budget.template.module",
        "template_id",
        string="Modules",
        copy=True,
        help="List of modules included in this template. These modules will "
        "be copied to simulations when the template is loaded. Each module "
        "can have its hours adjusted per template.",
    )
    line_ids = fields.One2many(
        "budget.template.line",
        "template_id",
        string="General Activities",
        help="List of general activities included in this template. These "
        "activities represent specific tasks (discovery, configuration, "
        "training, etc.) that are not covered by modules or integrations. "
        "They will be copied to simulations when the template is loaded.",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
        ],
        default="draft",
        tracking=True,
        readonly=True,
        help="Current state of the template. Draft templates can be edited "
        "and modified. Confirmed templates are locked and cannot be modified "
        "(read-only).",
    )

    # Methods
    def action_confirm(self):
        """Confirm template as final.

        This method transitions the template from 'draft' to 'confirmed' state.
        Once confirmed, the template becomes read-only and cannot be modified.

        Returns:
            bool: True if successful.

        Raises:
            UserError: If the template is not in 'draft' state.
        """
        self.ensure_one()
        if self.state != "draft":
            raise UserError(_("Only draft templates can be confirmed."))
        self.state = "confirmed"
        return True

    def action_set_draft(self):
        """Reset template to draft state.

        This method transitions the template from 'confirmed' back to 'draft'
        state, allowing it to be edited again.

        Returns:
            bool: True if successful.
        """
        self.ensure_one()
        if self.state == "confirmed":
            self.state = "draft"
        return True

    def action_recalculate(self):
        """Recalculate totals based on current rules.

        This method triggers a recalculation of all final hours and the total
        hours for this template. It should be used when calculation rules
        have changed or when you want to ensure all values are up to date.

        Returns:
            dict: Action dictionary to display a success notification.

        Raises:
            UserError: If the template is not in 'draft' state.
        """
        self.ensure_one()
        if self.state != "draft":
            raise UserError(_("Only draft templates can be recalculated."))

        # Trigger recompute of totals
        self._compute_totals()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Recalculated"),
                "message": _("Totals have been recalculated."),
                "type": "success",
                "sticky": False,
            },
        }
