# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class BudgetSimulation(models.Model):
    _inherit = "budget.simulation"

    def action_create_quotation(self):
        res = super().action_create_quotation()
        sale_orders = (
            self.sale_order_id
            | self.support_contract_sale_order_id
            | self.migration_contract_sale_order_id
        ).exists()
        if not sale_orders:
            return res
        company = self.company_id
        fiscal_operation = (
            company.budget_simulation_fiscal_operation_id
            or company.sale_fiscal_operation_id
        )
        if not fiscal_operation:
            return res
        order_vals = {"fiscal_operation_id": fiscal_operation.id}
        if fiscal_operation.fiscal_position_id:
            order_vals["fiscal_position_id"] = fiscal_operation.fiscal_position_id.id
        sale_orders.write(order_vals)
        lines = sale_orders.mapped("order_line").filtered(
            lambda line: not line.display_type
        )
        lines.write({"fiscal_operation_id": fiscal_operation.id})
        # Fiscal operation replaces the taxes used while the contract price
        # was calculated, so amount_total changes after that write.
        self._reprice_contract_quotations()
        return res

    def _reprice_contract_quotations(self):
        """Set contract prices from the implementation total after fiscal taxes."""
        for simulation in self:
            implementation = simulation.sale_order_id
            if not implementation:
                continue
            project_cost = simulation._get_project_cost_from_sale_order(implementation)
            contracts = (
                (
                    simulation.support_contract_sale_order_id,
                    simulation._get_support_contract_fixed_amount(),
                ),
                (
                    simulation.migration_contract_sale_order_id,
                    simulation._get_migration_contract_fixed_amount(),
                ),
            )
            for contract, fixed_amount in contracts:
                if not contract:
                    continue
                product_lines = contract.order_line.filtered(
                    lambda line: not line.display_type
                )
                product_lines.write({"price_unit": fixed_amount + project_cost})
