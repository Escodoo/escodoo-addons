# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestBudgetSimulation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.BudgetSimulation = cls.env["budget.simulation"]
        cls.BudgetTemplate = cls.env["budget.template"]
        cls.BudgetIntegration = cls.env["budget.integration"]
        cls.BudgetModule = cls.env["budget.module"]
        cls.BudgetLine = cls.env["budget.line"]
        cls.BudgetSimulationLine = cls.env["budget.simulation.line"]
        cls.Partner = cls.env["res.partner"]

        # Create test partner
        cls.partner = cls.Partner.create({"name": "Test Partner"})

        # Get or create test integrations (may exist from demo data)
        cls.integration_nfe = cls.BudgetIntegration.search(
            [("code", "=", "nfe")], limit=1
        )
        if not cls.integration_nfe:
            cls.integration_nfe = cls.BudgetIntegration.create(
                {
                    "name": "NFe",
                    "code": "nfe",
                    "default_hours": 40.0,
                }
            )
        cls.integration_nfse = cls.BudgetIntegration.search(
            [("code", "=", "nfse")], limit=1
        )
        if not cls.integration_nfse:
            cls.integration_nfse = cls.BudgetIntegration.create(
                {
                    "name": "NFS-e",
                    "code": "nfse",
                    "default_hours": 30.0,
                }
            )

        # Get or create test modules (may exist from demo data)
        cls.module_sale = cls.BudgetModule.search([("code", "=", "sale")], limit=1)
        if not cls.module_sale:
            cls.module_sale = cls.BudgetModule.create(
                {
                    "name": "Sales",
                    "code": "sale",
                    "default_hours": 20.0,
                }
            )
        cls.module_stock = cls.BudgetModule.search([("code", "=", "stock")], limit=1)
        if not cls.module_stock:
            cls.module_stock = cls.BudgetModule.create(
                {
                    "name": "Stock",
                    "code": "stock",
                    "default_hours": 25.0,
                }
            )

        # Get or create test budget lines (catalog entries)
        cls.line_discovery = cls.BudgetLine.search(
            [("code", "=", "discovery_analysis")], limit=1
        )
        if not cls.line_discovery:
            cls.line_discovery = cls.BudgetLine.create(
                {
                    "name": "Discovery and Requirements Analysis",
                    "code": "discovery_analysis",
                    "category": "discovery",
                    "default_hours": 40.0,
                }
            )
        cls.line_config = cls.BudgetLine.search(
            [("code", "=", "system_configuration")], limit=1
        )
        if not cls.line_config:
            cls.line_config = cls.BudgetLine.create(
                {
                    "name": "System Configuration",
                    "code": "system_configuration",
                    "category": "config",
                    "default_hours": 60.0,
                }
            )
        # Create a test line for general testing
        cls.line_test = cls.BudgetLine.search([("code", "=", "test_line")], limit=1)
        if not cls.line_test:
            cls.line_test = cls.BudgetLine.create(
                {
                    "name": "Test Line",
                    "code": "test_line",
                    "category": "other",
                    "default_hours": 100.0,
                }
            )

        # Create test template
        cls.template = cls.BudgetTemplate.create(
            {
                "name": "Test Template",
                "complexity": "medium",
                "users_qty": 10,
                "company_qty": 2,
                "integration_line_ids": [
                    (0, 0, {"integration_id": cls.integration_nfe.id}),
                ],
                "module_line_ids": [
                    (0, 0, {"module_id": cls.module_sale.id}),
                ],
            }
        )

        # Create template lines
        cls.template_line1 = cls.env["budget.template.line"].create(
            {
                "template_id": cls.template.id,
                "line_id": cls.line_discovery.id,
            }
        )
        cls.template_line2 = cls.env["budget.template.line"].create(
            {
                "template_id": cls.template.id,
                "line_id": cls.line_config.id,
            }
        )

    def test_create_simulation(self):
        """Test creating a budget simulation"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 10,
                "company_qty": 1,
                "complexity": "medium",
            }
        )
        self.assertTrue(simulation.name)
        self.assertEqual(simulation.state, "draft")
        self.assertEqual(simulation.users_qty, 10)
        self.assertEqual(simulation.company_qty, 1)
        self.assertEqual(simulation.complexity, "medium")

    def test_load_from_template(self):
        """Test loading data from template"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "low",
                "template_id": self.template.id,
            }
        )
        simulation.action_load_from_template()

        # Check that template data was loaded
        self.assertEqual(simulation.complexity, "medium")
        self.assertEqual(simulation.users_qty, 10)
        self.assertEqual(simulation.company_qty, 2)
        self.assertEqual(len(simulation.integration_line_ids), 1)
        self.assertEqual(len(simulation.module_line_ids), 1)
        self.assertEqual(len(simulation.line_ids), 2)

        # Check line data
        # Refresh to ensure we have the latest data
        simulation.refresh()
        line1 = simulation.line_ids.filtered(
            lambda l: l.name == "Discovery and Requirements Analysis"
        )
        self.assertTrue(line1, "Line 'Discovery and Requirements Analysis' not found")
        self.assertEqual(line1.default_hours, 40.0)
        self.assertEqual(line1.category, "discovery")

    def test_complexity_factors(self):
        """Test complexity factor calculation"""
        # Low complexity: factor 1.00, users: 5 (no factor), companies: 1 (no factor)
        sim_low = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "low",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": sim_low.id,
                "line_id": self.line_test.id,
            }
        )
        sim_low._compute_totals()
        # final_hours = 100 * 1.00 * 1.00 * 1.00 = 100.0
        self.assertAlmostEqual(sim_low.total_hours, 100.0, places=2)

        # Medium complexity: factor 1.15, users: 5 (no factor), companies: 1 (no factor)
        sim_medium = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "medium",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": sim_medium.id,
                "line_id": self.line_test.id,
            }
        )
        sim_medium._compute_totals()
        # final_hours = 100 * 1.15 * 1.00 * 1.00 = 115.0
        self.assertAlmostEqual(sim_medium.total_hours, 115.0, places=2)

        # High complexity: factor 1.30, users: 5 (no factor), companies: 1 (no factor)
        sim_high = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "high",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": sim_high.id,
                "line_id": self.line_test.id,
            }
        )
        sim_high._compute_totals()
        # final_hours = 100 * 1.30 * 1.00 * 1.00 = 130.0
        self.assertAlmostEqual(sim_high.total_hours, 130.0, places=2)

    def test_users_factor(self):
        """Test users factor calculation"""
        # 10 users: 5 base + 5 additional = 1.05 factor
        sim = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 10,
                "company_qty": 1,
                "complexity": "low",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": sim.id,
                "line_id": self.line_test.id,
            }
        )
        sim._compute_totals()
        # final_hours = 100 * 1.00 * 1.05 * 1.00 = 105.0
        self.assertAlmostEqual(sim.total_hours, 105.0, places=2)

        # 25 users: max factor 1.40 (40% limit)
        sim2 = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 25,
                "company_qty": 1,
                "complexity": "low",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": sim2.id,
                "line_id": self.line_test.id,
            }
        )
        sim2._compute_totals()
        # final_hours = 100 * 1.00 * 1.20 * 1.00 = 120.0 (20 users above 5 = 20% = 1.20)
        self.assertAlmostEqual(sim2.total_hours, 120.0, places=2)

    def test_integrations_and_modules_hours(self):
        """Test that integration and module hours are included"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "low",
                "integration_line_ids": [
                    (0, 0, {"integration_id": self.integration_nfe.id}),
                    (0, 0, {"integration_id": self.integration_nfse.id}),
                ],
                "module_line_ids": [
                    (0, 0, {"module_id": self.module_sale.id}),
                    (0, 0, {"module_id": self.module_stock.id}),
                ],
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": simulation.id,
                "line_id": self.line_test.id,
            }
        )
        simulation._compute_totals()
        # All with low complexity (1.00), 5 users (1.00), 1 company (1.00)
        # Line: 100 * 1.00 * 1.00 * 1.00 = 100.0
        # Integrations: (40 + 30) * 1.00 * 1.00 * 1.00 = 70.0
        # Modules: (20 + 25) * 1.00 * 1.00 * 1.00 = 45.0
        # Total: 100 + 70 + 45 = 215.0
        self.assertAlmostEqual(simulation.total_hours, 215.0, places=2)

    def test_adjusted_hours(self):
        """Test that adjusted hours override base hours"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 5,
                "company_qty": 1,
                "complexity": "low",
            }
        )
        line = self.BudgetSimulationLine.create(
            {
                "simulation_id": simulation.id,
                "line_id": self.line_test.id,
                "adjusted_hours": 150.0,
            }
        )
        # Adjusted hours override base, then factors applied
        # final_hours = 150 * 1.00 * 1.00 * 1.00 = 150.0
        self.assertAlmostEqual(line.final_hours, 150.0, places=2)

    def test_state_transitions(self):
        """Test state transitions"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 10,
                "company_qty": 1,
                "complexity": "medium",
            }
        )
        self.assertEqual(simulation.state, "draft")

        # Confirm simulation
        simulation.action_confirm()
        self.assertEqual(simulation.state, "confirmed")

        # Reset to draft (should work)
        simulation.action_set_draft()
        self.assertEqual(simulation.state, "draft")

    def test_state_transitions_errors(self):
        """Test state transition errors"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 10,
                "company_qty": 1,
                "complexity": "medium",
            }
        )

        # Confirm from draft (should work)
        simulation.action_confirm()
        self.assertEqual(simulation.state, "confirmed")

        # Try to confirm again (should fail)
        with self.assertRaises(UserError):
            simulation.action_confirm()

    def test_recalculate(self):
        """Test recalculate action"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 10,
                "company_qty": 1,
                "complexity": "medium",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": simulation.id,
                "line_id": self.line_test.id,
            }
        )
        result = simulation.action_recalculate()
        self.assertTrue(result)
        simulation._compute_totals()
        self.assertGreater(simulation.total_hours, 0)

    def test_duplicate_simulation(self):
        """Test duplicating a simulation"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 10,
                "company_qty": 1,
                "complexity": "medium",
                "state": "confirmed",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": simulation.id,
                "line_id": self.line_test.id,
            }
        )

        copy = simulation.copy({"name": "New"})
        self.assertNotEqual(copy.id, simulation.id)
        self.assertEqual(copy.state, "draft")
        self.assertEqual(len(copy.line_ids), 1)

    def test_load_from_template_without_template(self):
        """Test loading from template without template selected"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 10,
                "company_qty": 1,
                "complexity": "medium",
            }
        )
        with self.assertRaises(UserError):
            simulation.action_load_from_template()

    def test_companies_factor(self):
        """Test companies factor calculation"""
        # 3 companies: 1 base + 2 additional = 1.30 factor (2 * 0.15)
        sim = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 5,
                "company_qty": 3,
                "complexity": "low",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": sim.id,
                "line_id": self.line_test.id,
            }
        )
        sim._compute_totals()
        # final_hours = 100 * 1.00 * 1.00 * 1.30 = 130.0
        self.assertAlmostEqual(sim.total_hours, 130.0, places=2)

        # 16 companies: 1 base + 15 additional = 1 + (15 * 0.15) = 3.25 (no max limit)
        sim2 = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 5,
                "company_qty": 16,
                "complexity": "low",
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": sim2.id,
                "line_id": self.line_test.id,
            }
        )
        sim2._compute_totals()
        # final_hours = 100 * 1.00 * 1.00 * 3.25 = 325.0
        self.assertAlmostEqual(sim2.total_hours, 325.0, places=2)

    def test_all_factors_combined(self):
        """Test all factors combined (complexity, users, companies)"""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": 10,  # 5 additional = 1.05 (min(5 * 0.01, 0.40))
                "company_qty": 3,  # 2 additional = 1.30 (1 + 2 * 0.15)
                "complexity": "medium",  # 1.15
            }
        )
        self.BudgetSimulationLine.create(
            {
                "simulation_id": simulation.id,
                "line_id": self.line_test.id,
            }
        )
        simulation._compute_totals()
        # final_hours = 100 * 1.15 * 1.05 * 1.30 = 156.975
        self.assertAlmostEqual(simulation.total_hours, 156.98, places=2)
