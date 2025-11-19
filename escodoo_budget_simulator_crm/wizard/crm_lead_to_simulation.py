# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CrmLeadToSimulation(models.TransientModel):
    """Wizard to create budget simulation from CRM lead.

    This wizard allows users to create a budget simulation from a CRM opportunity,
    with options to create a new partner or link to an existing partner.
    """

    _name = "crm.lead.to.simulation"
    _description = "Create Budget Simulation from CRM Lead"

    # Fields
    action = fields.Selection(
        [
            ("create", "Create a new customer"),
            ("exist", "Link to an existing customer"),
        ],
        string="Simulation Customer",
        required=True,
        help="Choose how to handle the customer for the budget simulation: "
        "create a new customer or link to an existing one.",
    )
    lead_id = fields.Many2one(
        "crm.lead",
        string="Associated Lead",
        required=True,
        help="The CRM lead/opportunity this simulation will be linked to.",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        help="The customer to link to the simulation. Required when linking to "
        "an existing customer.",
    )

    # Methods
    @api.model
    def default_get(self, fields):
        """Set default values based on the lead."""
        result = super().default_get(fields)

        # Check if lead_id is already provided in result (from create vals)
        # If so, we can skip the active_model check
        lead = False
        if result.get("lead_id"):
            lead = self.env["crm.lead"].browse(result["lead_id"])
        elif "lead_id" in fields and self._context.get("active_id"):
            # Only check active_model if we're using context
            active_model = self._context.get("active_model")
            if active_model and active_model != "crm.lead":
                raise UserError(_("You can only apply this action from a lead."))
            lead = self.env["crm.lead"].browse(self._context["active_id"])

        if lead:
            result["lead_id"] = lead.id
            partner_id = result.get("partner_id") or (
                lead.partner_id.id if lead.partner_id else False
            )
            if "action" in fields and not result.get("action"):
                result["action"] = "exist" if partner_id else "create"
            if "partner_id" in fields and not result.get("partner_id"):
                result["partner_id"] = partner_id

        return result

    def action_apply(self):
        """Apply the wizard action and create the budget simulation.

        This method:
        1. Handles partner assignment based on the selected action
        2. Creates the budget simulation with the appropriate partner
        3. Returns an action to open the created simulation

        Returns:
            dict: Action dictionary to open the created simulation form view.
        """
        self.ensure_one()
        lead = self.lead_id

        # Handle partner assignment
        partner_id = False
        if self.action == "create":
            # Create a new partner from the lead
            lead._handle_partner_assignment(create_missing=True)
            partner_id = lead.partner_id.id if lead.partner_id else False
        elif self.action == "exist":
            # Link to existing partner
            if not self.partner_id:
                raise UserError(_("Please select a customer to link."))
            lead._handle_partner_assignment(
                force_partner_id=self.partner_id.id, create_missing=False
            )
            partner_id = self.partner_id.id

        if not partner_id:
            raise UserError(
                _(
                    "A customer is required to create a budget simulation. "
                    "Please select or create a customer."
                )
            )

        # Create simulation
        simulation = self.env["budget.simulation"].create(
            {
                "partner_id": partner_id,
                "opportunity_id": lead.id,
                "notes": lead.description or "",
            }
        )

        return {
            "type": "ir.actions.act_window",
            "name": _("Budget Simulation"),
            "res_model": "budget.simulation",
            "res_id": simulation.id,
            "view_mode": "form",
            "target": "current",
        }
