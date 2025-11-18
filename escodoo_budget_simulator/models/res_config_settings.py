# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    quotation_product_id = fields.Many2one(
        "product.product",
        string="Default Product for Quotations",
        domain=[("type", "=", "service"), ("sale_ok", "=", True)],
        help="Default product to use when creating sale orders from confirmed simulations.",
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        IrConfigParameter = self.env["ir.config_parameter"].sudo()
        product_id = IrConfigParameter.get_param(
            "escodoo_budget_simulator.default_quotation_product_id"
        )
        if product_id:
            res["quotation_product_id"] = int(product_id)
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
        return True
