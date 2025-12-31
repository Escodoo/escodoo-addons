# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BudgetSimulation(models.Model):
    """Extend Budget Simulation to add CRM opportunity integration."""

    _inherit = "budget.simulation"

    # Fields
    opportunity_id = fields.Many2one(
        "crm.lead",
        string="Opportunity",
        tracking=True,
        domain="[('type', '=', 'opportunity')]",
        states={
            "confirmed": [("readonly", True)],
            "quotation": [("readonly", True)],
            "cancelled": [("readonly", True)],
        },
        help="The CRM opportunity this budget simulation is linked to. When a "
        "simulation is created from an opportunity, this field is automatically "
        "populated. When a sale order is created from this simulation, it will "
        "be linked to this opportunity.",
    )

    # Methods

    def action_create_quotation(self):
        """Extend to associate opportunity with sale order.

        This method extends the base action_create_quotation to automatically
        link the created sale order to the opportunity associated with this
        simulation, if any.
        """
        result = super().action_create_quotation()
        self.ensure_one()
        if self.opportunity_id and self.sale_order_id:
            # Associate opportunity with sale order
            # The sale_crm module adds the opportunity_id field to sale.order
            self.sale_order_id.write({"opportunity_id": self.opportunity_id.id})
        return result
