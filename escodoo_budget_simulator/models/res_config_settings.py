# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    _SUPPORT_PRODUCT_PARAM = (
        "escodoo_budget_simulator.support_maintenance_contract_product_id"
    )
    _MIGRATION_PRODUCT_PARAM = "escodoo_budget_simulator.migration_contract_product_id"
    _PROJECT_COST_PERCENT_PARAM = (
        "escodoo_budget_simulator.default_project_cost_percent"
    )
    _SUPPORT_FIXED_AMOUNT_PARAM = (
        "escodoo_budget_simulator.support_maintenance_contract_fixed_amount"
    )
    _MIGRATION_FIXED_AMOUNT_PARAM = (
        "escodoo_budget_simulator.migration_contract_fixed_amount"
    )

    quotation_product_id = fields.Many2one(
        "product.product",
        string="Default Product for Quotations",
        domain=[("type", "=", "service"), ("sale_ok", "=", True)],
        config_parameter="escodoo_budget_simulator.default_quotation_product_id",
        help="Default product to use when creating sale orders "
        "from confirmed simulations.",
    )
    support_maintenance_contract_product_id = fields.Many2one(
        "product.product",
        string="Support/Maintenance Contract Product",
        domain=[("type", "=", "service"), ("sale_ok", "=", True)],
        config_parameter=_SUPPORT_PRODUCT_PARAM,
        help="Service product used to create the support/maintenance "
        "contract quotation from a confirmed simulation.",
    )
    migration_contract_product_id = fields.Many2one(
        "product.product",
        string="Migration Contract Product",
        domain=[("type", "=", "service"), ("sale_ok", "=", True)],
        config_parameter=_MIGRATION_PRODUCT_PARAM,
        help="Service product used to create the migration contract quotation "
        "from a confirmed simulation.",
    )
    default_project_cost_percent = fields.Float(
        string="Default Project Cost Percentage",
        config_parameter=_PROJECT_COST_PERCENT_PARAM,
        default_model="budget.simulation",
        help="Default percentage used to calculate project cost.",
    )
    support_maintenance_contract_fixed_amount = fields.Float(
        string="Support/Maintenance Fixed Amount",
        config_parameter=_SUPPORT_FIXED_AMOUNT_PARAM,
        help="Fixed amount added to the support/maintenance contract quotation.",
    )
    migration_contract_fixed_amount = fields.Float(
        string="Migration Fixed Amount",
        config_parameter=_MIGRATION_FIXED_AMOUNT_PARAM,
        help="Fixed amount added to the migration contract quotation.",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        product_id = IrConfigParameter.get_param(
            "escodoo_budget_simulator.default_quotation_product_id"
        )
        support_product_id = IrConfigParameter.get_param(self._SUPPORT_PRODUCT_PARAM)
        migration_product_id = IrConfigParameter.get_param(
            self._MIGRATION_PRODUCT_PARAM
        )
        default_project_cost_percent = IrConfigParameter.get_param(
            self._PROJECT_COST_PERCENT_PARAM
        )
        support_fixed_amount = IrConfigParameter.get_param(
            self._SUPPORT_FIXED_AMOUNT_PARAM
        )
        migration_fixed_amount = IrConfigParameter.get_param(
            self._MIGRATION_FIXED_AMOUNT_PARAM
        )
        if product_id:
            res["quotation_product_id"] = int(product_id)
        if support_product_id:
            res["support_maintenance_contract_product_id"] = int(support_product_id)
        if migration_product_id:
            res["migration_contract_product_id"] = int(migration_product_id)
        if default_project_cost_percent is not None:
            res["default_project_cost_percent"] = float(default_project_cost_percent)
        if support_fixed_amount is not None:
            res["support_maintenance_contract_fixed_amount"] = float(
                support_fixed_amount
            )
        if migration_fixed_amount is not None:
            res["migration_contract_fixed_amount"] = float(migration_fixed_amount)
        return res

    def set_values(self):
        super().set_values()
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        if self.quotation_product_id:
            IrConfigParameter.set_param(
                "escodoo_budget_simulator.default_quotation_product_id",
                self.quotation_product_id.id,
            )
        else:
            IrConfigParameter.set_param(
                "escodoo_budget_simulator.default_quotation_product_id", False
            )
        if self.support_maintenance_contract_product_id:
            IrConfigParameter.set_param(
                self._SUPPORT_PRODUCT_PARAM,
                self.support_maintenance_contract_product_id.id,
            )
        else:
            IrConfigParameter.set_param(
                self._SUPPORT_PRODUCT_PARAM,
                False,
            )
        if self.migration_contract_product_id:
            IrConfigParameter.set_param(
                self._MIGRATION_PRODUCT_PARAM,
                self.migration_contract_product_id.id,
            )
        else:
            IrConfigParameter.set_param(
                self._MIGRATION_PRODUCT_PARAM,
                False,
            )
        IrConfigParameter.set_param(
            self._PROJECT_COST_PERCENT_PARAM,
            self.default_project_cost_percent or 0.0,
        )
        IrConfigParameter.set_param(
            self._SUPPORT_FIXED_AMOUNT_PARAM,
            self.support_maintenance_contract_fixed_amount or 0.0,
        )
        IrConfigParameter.set_param(
            self._MIGRATION_FIXED_AMOUNT_PARAM,
            self.migration_contract_fixed_amount or 0.0,
        )
        return True
