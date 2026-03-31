# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class BudgetSimulation(models.Model):
    _inherit = "budget.simulation"

    def action_create_quotation(self):
        res = super().action_create_quotation()
        sale_order = self.sale_order_id
        if not sale_order:
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
        sale_order.write(order_vals)
        lines = sale_order.order_line.filtered(lambda line: not line.display_type)
        if lines:
            lines.write({"fiscal_operation_id": fiscal_operation.id})
        return res
