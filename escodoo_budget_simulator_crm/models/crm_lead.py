# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class CrmLead(models.Model):
    """Extend CRM Lead to add budget simulation creation."""

    _inherit = "crm.lead"

    simulation_ids = fields.One2many(
        "budget.simulation",
        "opportunity_id",
        string="Budget Simulations",
        help="Budget simulations created from this opportunity.",
    )
    simulation_count = fields.Integer(
        string="Simulations Count",
        compute="_compute_simulation_count",
        help="Number of budget simulations created from this opportunity.",
    )

    # Methods
    @api.depends("simulation_ids")
    def _compute_simulation_count(self):
        """Compute the number of simulations linked to this opportunity."""
        for rec in self:
            rec.simulation_count = len(rec.simulation_ids)

    def action_create_budget_simulation(self):
        """Create a budget simulation from this opportunity.

        This method opens a wizard that allows the user to choose how to handle
        the partner: create a new one, link to an existing one, or create without
        a partner. If a partner is already set, it creates the simulation directly.

        Returns:
            dict: Action dictionary to open the wizard or the created simulation.
        """
        self.ensure_one()
        # If partner is already set, create simulation directly
        if self.partner_id:
            simulation = self.env["budget.simulation"].create(
                {
                    "partner_id": self.partner_id.id,
                    "opportunity_id": self.id,
                    "notes": self.description or "",
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
        # Otherwise, open wizard
        return {
            "type": "ir.actions.act_window",
            "name": _("Create Budget Simulation"),
            "res_model": "crm.lead.to.simulation",
            "view_mode": "form",
            "target": "new",
            "context": {
                "active_model": "crm.lead",
                "active_id": self.id,
            },
        }

    def action_view_simulations(self):
        """View all budget simulations linked to this opportunity.

        Returns:
            dict: Action dictionary to open the simulations list view.
        """
        self.ensure_one()
        action = self.env.ref(
            "escodoo_budget_simulator.action_budget_simulation"
        ).read()[0]
        action["domain"] = [("opportunity_id", "=", self.id)]
        action["context"] = {
            "default_opportunity_id": self.id,
            "default_partner_id": self.partner_id.id if self.partner_id else False,
        }
        return action
