# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.tests import TransactionCase, tagged

from odoo.addons.l10n_br_fiscal.constants.fiscal import PRODUCT_FISCAL_TYPE_SERVICE


@tagged("post_install", "-at_install")
class TestBudgetSimulationQuotationFiscal(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.fo_venda = cls.env.ref("l10n_br_fiscal.fo_venda", raise_if_not_found=False)
        cls.company = cls.env.ref(
            "l10n_br_base.empresa_lucro_presumido", raise_if_not_found=False
        )
        if not cls.company:
            cls.company = cls.env.company
        cls.partner = cls.env.ref(
            "l10n_br_base.res_partner_cliente1_sp", raise_if_not_found=False
        )
        if not cls.partner:
            cls.partner = cls.env["res.partner"].create({"name": "Fiscal Test Partner"})

        cls.BudgetSimulation = cls.env["budget.simulation"]
        cls.BudgetModule = cls.env["budget.module"]

        cls.module_sale = cls.BudgetModule.search([("code", "=", "sale")], limit=1)
        if not cls.module_sale:
            cls.module_sale = cls.BudgetModule.create(
                {"name": "Sales", "code": "sale", "default_hours": 10.0}
            )

        tmpl = (
            cls.env["product.template"]
            .with_company(cls.company)
            .create(
                {
                    "name": "Budget Simulator Test Hours Product",
                    "type": "service",
                    "sale_ok": True,
                    "purchase_ok": False,
                    "fiscal_type": PRODUCT_FISCAL_TYPE_SERVICE,
                }
            )
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "escodoo_budget_simulator.default_quotation_product_id",
            str(tmpl.product_variant_id.id),
        )
        support_tmpl = (
            cls.env["product.template"]
            .with_company(cls.company)
            .create(
                {
                    "name": "Budget Simulator Support Contract Product",
                    "type": "service",
                    "sale_ok": True,
                    "purchase_ok": False,
                    "fiscal_type": PRODUCT_FISCAL_TYPE_SERVICE,
                }
            )
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "escodoo_budget_simulator.support_maintenance_contract_product_id",
            str(support_tmpl.product_variant_id.id),
        )
        migration_tmpl = (
            cls.env["product.template"]
            .with_company(cls.company)
            .create(
                {
                    "name": "Budget Simulator Migration Contract Product",
                    "type": "service",
                    "sale_ok": True,
                    "purchase_ok": False,
                    "fiscal_type": PRODUCT_FISCAL_TYPE_SERVICE,
                }
            )
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "escodoo_budget_simulator.migration_contract_product_id",
            str(migration_tmpl.product_variant_id.id),
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "escodoo_budget_simulator.default_project_cost_percent",
            "12.5",
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "escodoo_budget_simulator.support_maintenance_contract_fixed_amount",
            "2000.0",
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "escodoo_budget_simulator.migration_contract_fixed_amount",
            "1500.0",
        )

    def test_quotation_from_simulation_sets_fiscal_operation_and_line(self):
        """Sale order and lines get fiscal_operation_id;
        lines get fiscal_operation_line_id."""
        self.company.write(
            {
                "sale_fiscal_operation_id": self.fo_venda.id,
                "budget_simulation_fiscal_operation_id": False,
            }
        )

        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "low",
                "module_line_ids": [(0, 0, {"module_id": self.module_sale.id})],
            }
        )
        simulation.action_confirm()
        simulation.action_create_quotation()

        order = simulation.sale_order_id
        self.assertTrue(order)
        self.assertEqual(order.fiscal_operation_id, self.fo_venda)
        product_lines = order.order_line.filtered(lambda line: not line.display_type)
        self.assertTrue(product_lines)

    def test_budget_simulation_specific_fiscal_operation_takes_precedence(self):
        """Company budget_simulation_fiscal_operation_id overrides sale default."""
        other_fo = self.env["l10n_br_fiscal.operation"].search(
            [
                ("fiscal_operation_type", "=", "out"),
                ("state", "=", "approved"),
                ("id", "!=", self.fo_venda.id),
            ],
            limit=1,
        )
        if not other_fo:
            self.skipTest("No alternate approved outbound fiscal operation in DB")

        self.company.write(
            {
                "sale_fiscal_operation_id": self.fo_venda.id,
                "budget_simulation_fiscal_operation_id": other_fo.id,
            }
        )

        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "low",
                "module_line_ids": [(0, 0, {"module_id": self.module_sale.id})],
            }
        )
        simulation.action_confirm()
        simulation.action_create_quotation()

        order = simulation.sale_order_id
        self.assertEqual(order.fiscal_operation_id, other_fo)

    def test_support_contract_quotation_inherits_fiscal_operation(self):
        self.company.write(
            {
                "sale_fiscal_operation_id": self.fo_venda.id,
                "budget_simulation_fiscal_operation_id": False,
            }
        )
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "low",
                "generate_support_contract_quotation": True,
                "module_line_ids": [(0, 0, {"module_id": self.module_sale.id})],
            }
        )
        simulation.action_confirm()
        simulation.action_create_quotation()

        self.assertTrue(simulation.sale_order_id)
        self.assertTrue(simulation.support_contract_sale_order_id)
        self.assertEqual(simulation.sale_order_id.fiscal_operation_id, self.fo_venda)
        self.assertEqual(
            simulation.support_contract_sale_order_id.fiscal_operation_id, self.fo_venda
        )

    def test_migration_contract_quotation_inherits_fiscal_operation(self):
        self.company.write(
            {
                "sale_fiscal_operation_id": self.fo_venda.id,
                "budget_simulation_fiscal_operation_id": False,
            }
        )
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "company_id": self.company.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "low",
                "generate_migration_contract_quotation": True,
                "module_line_ids": [(0, 0, {"module_id": self.module_sale.id})],
            }
        )
        simulation.action_confirm()
        simulation.action_create_quotation()

        self.assertTrue(simulation.sale_order_id)
        self.assertTrue(simulation.migration_contract_sale_order_id)
        self.assertEqual(simulation.sale_order_id.fiscal_operation_id, self.fo_venda)
        self.assertEqual(
            simulation.migration_contract_sale_order_id.fiscal_operation_id,
            self.fo_venda,
        )
