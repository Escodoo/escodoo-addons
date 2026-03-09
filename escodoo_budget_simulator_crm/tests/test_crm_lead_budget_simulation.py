# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestCrmLeadBudgetSimulation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.CrmLead = cls.env["crm.lead"]
        cls.BudgetSimulation = cls.env["budget.simulation"]
        cls.CrmLeadToSimulation = cls.env["crm.lead.to.simulation"]
        cls.Partner = cls.env["res.partner"]
        cls.SaleOrder = cls.env["sale.order"]

        # Create test partner
        cls.partner = cls.Partner.create({"name": "Test Partner"})

        # Create test opportunity with partner
        cls.opportunity_with_partner = cls.CrmLead.create(
            {
                "name": "Test Opportunity with Partner",
                "type": "opportunity",
                "partner_id": cls.partner.id,
                "description": "Test opportunity description",
            }
        )

        # Create test opportunity without partner
        cls.opportunity_without_partner = cls.CrmLead.create(
            {
                "name": "Test Opportunity without Partner",
                "type": "opportunity",
                "description": "Test opportunity description without partner",
            }
        )

    def test_create_simulation_from_opportunity_with_partner(self):
        """Test creating a simulation from an opportunity that has a partner."""
        # Call action_create_budget_simulation
        action = self.opportunity_with_partner.action_create_budget_simulation()

        # Check that action returns a form view (not wizard)
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "budget.simulation")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "current")

        # Get the created simulation
        simulation = self.BudgetSimulation.browse(action["res_id"])

        # Check simulation fields
        self.assertEqual(simulation.partner_id, self.partner)
        self.assertEqual(simulation.opportunity_id, self.opportunity_with_partner)
        # notes is HTML field, so we check if text is contained in HTML
        self.assertIn("Test opportunity description", simulation.notes or "")

    def test_create_simulation_from_opportunity_without_partner(self):
        """Test creating a simulation from an opportunity
        without a partner opens wizard."""
        # Call action_create_budget_simulation
        action = self.opportunity_without_partner.action_create_budget_simulation()

        # Check that action returns a wizard
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "crm.lead.to.simulation")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["active_model"], "crm.lead")
        self.assertEqual(
            action["context"]["active_id"], self.opportunity_without_partner.id
        )

    def test_wizard_default_get_with_partner(self):
        """Test wizard default_get when opportunity has a partner."""
        wizard = self.CrmLeadToSimulation.with_context(
            active_model="crm.lead",
            active_id=self.opportunity_with_partner.id,
        )
        defaults = wizard.default_get(["lead_id", "partner_id", "action"])

        self.assertEqual(defaults["lead_id"], self.opportunity_with_partner.id)
        self.assertEqual(defaults["partner_id"], self.partner.id)
        self.assertEqual(defaults["action"], "exist")

    def test_wizard_default_get_without_partner(self):
        """Test wizard default_get when opportunity doesn't have a partner."""
        wizard = self.CrmLeadToSimulation.with_context(
            active_model="crm.lead",
            active_id=self.opportunity_without_partner.id,
        )
        defaults = wizard.default_get(["lead_id", "partner_id", "action"])

        self.assertEqual(defaults["lead_id"], self.opportunity_without_partner.id)
        self.assertFalse(defaults.get("partner_id"))
        self.assertEqual(defaults["action"], "create")

    def test_wizard_default_get_invalid_model(self):
        """Test wizard default_get raises error for invalid model."""
        wizard = self.CrmLeadToSimulation.with_context(
            active_model="res.partner",
            active_id=self.partner.id,
        )
        with self.assertRaises(UserError):
            wizard.default_get(["lead_id"])

    def test_wizard_action_apply_create_new_customer(self):
        """Test wizard action_apply with 'create' action."""
        wizard = self.CrmLeadToSimulation.create(
            {
                "lead_id": self.opportunity_without_partner.id,
                "action": "create",
            }
        )

        # Call action_apply
        action = wizard.action_apply()

        # Check that action returns a form view
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "budget.simulation")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "current")

        # Get the created simulation
        simulation = self.BudgetSimulation.browse(action["res_id"])

        # Check simulation fields
        self.assertEqual(simulation.opportunity_id, self.opportunity_without_partner)
        self.assertTrue(simulation.partner_id)  # Partner should be created
        # notes is HTML field, so we check if text is contained in HTML
        self.assertIn(
            "Test opportunity description without partner",
            simulation.notes or "",
        )

        # Check that partner is linked to opportunity
        self.opportunity_without_partner.invalidate_recordset()
        self.assertEqual(
            self.opportunity_without_partner.partner_id, simulation.partner_id
        )

    def test_wizard_action_apply_link_existing_customer(self):
        """Test wizard action_apply with 'exist' action."""
        wizard = self.CrmLeadToSimulation.create(
            {
                "lead_id": self.opportunity_without_partner.id,
                "action": "exist",
                "partner_id": self.partner.id,
            }
        )

        # Call action_apply
        action = wizard.action_apply()

        # Check that action returns a form view
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "budget.simulation")
        self.assertEqual(action["view_mode"], "form")
        self.assertEqual(action["target"], "current")

        # Get the created simulation
        simulation = self.BudgetSimulation.browse(action["res_id"])

        # Check simulation fields
        self.assertEqual(simulation.partner_id, self.partner)
        self.assertEqual(simulation.opportunity_id, self.opportunity_without_partner)
        # notes is HTML field, so we check if text is contained in HTML
        self.assertIn(
            "Test opportunity description without partner",
            simulation.notes or "",
        )

        # Check that partner is linked to opportunity
        self.opportunity_without_partner.invalidate_recordset()
        self.assertEqual(self.opportunity_without_partner.partner_id, self.partner)

    def test_wizard_action_apply_exist_without_partner(self):
        """Test wizard action_apply with 'exist' action but no partner selected."""
        wizard = self.CrmLeadToSimulation.create(
            {
                "lead_id": self.opportunity_without_partner.id,
                "action": "exist",
            }
        )

        # Call action_apply should raise UserError
        with self.assertRaises(UserError):
            wizard.action_apply()

    def test_simulation_count_computation(self):
        """Test simulation_count field computation."""
        # Initially, count should be 0
        self.assertEqual(self.opportunity_with_partner.simulation_count, 0)

        # Create a simulation
        simulation1 = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "opportunity_id": self.opportunity_with_partner.id,
            }
        )

        # Count should be 1
        self.opportunity_with_partner.invalidate_recordset()
        self.assertEqual(self.opportunity_with_partner.simulation_count, 1)

        # Create another simulation
        self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "opportunity_id": self.opportunity_with_partner.id,
            }
        )

        # Count should be 2
        self.opportunity_with_partner.invalidate_recordset()
        self.assertEqual(self.opportunity_with_partner.simulation_count, 2)

        # Unlink one simulation
        simulation1.unlink()

        # Count should be 1
        self.opportunity_with_partner.invalidate_recordset()
        self.assertEqual(self.opportunity_with_partner.simulation_count, 1)

    def test_action_view_simulations(self):
        """Test action_view_simulations returns correct action."""
        # Create some simulations
        self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "opportunity_id": self.opportunity_with_partner.id,
            }
        )
        self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "opportunity_id": self.opportunity_with_partner.id,
            }
        )

        # Call action_view_simulations
        action = self.opportunity_with_partner.action_view_simulations()

        # Check action structure
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "budget.simulation")
        self.assertIn("domain", action)
        self.assertEqual(
            action["domain"],
            [("opportunity_id", "=", self.opportunity_with_partner.id)],
        )
        self.assertIn("context", action)
        self.assertEqual(
            action["context"]["default_opportunity_id"],
            self.opportunity_with_partner.id,
        )
        self.assertEqual(action["context"]["default_partner_id"], self.partner.id)

    def test_action_view_simulations_without_partner(self):
        """Test action_view_simulations returns correct action when opportunity
        has no partner."""
        # Call action_view_simulations for opportunity without partner
        action = self.opportunity_without_partner.action_view_simulations()

        # Check action structure
        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "budget.simulation")
        self.assertIn("domain", action)
        self.assertEqual(
            action["domain"],
            [("opportunity_id", "=", self.opportunity_without_partner.id)],
        )
        self.assertIn("context", action)
        self.assertEqual(
            action["context"]["default_opportunity_id"],
            self.opportunity_without_partner.id,
        )
        # When opportunity has no partner, default_partner_id should be False
        self.assertFalse(action["context"]["default_partner_id"])

    def test_simulation_opportunity_field(self):
        """Test that opportunity_id field is available in simulation."""
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "opportunity_id": self.opportunity_with_partner.id,
            }
        )

        # Check that opportunity_id is set
        self.assertEqual(simulation.opportunity_id, self.opportunity_with_partner)

        # Check that we can search by opportunity
        simulations = self.BudgetSimulation.search(
            [("opportunity_id", "=", self.opportunity_with_partner.id)]
        )
        self.assertIn(simulation, simulations)

    def test_action_create_quotation_links_opportunity(self):
        """Test that creating a quotation from simulation
        links opportunity to sale order."""
        # Check if sale_crm module is installed
        if "opportunity_id" not in self.SaleOrder._fields:
            self.skipTest(
                "sale_crm module not installed, skipping opportunity linking test"
            )

        # Create a confirmed simulation with opportunity
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "opportunity_id": self.opportunity_with_partner.id,
                "state": "confirmed",
            }
        )

        # Create quotation
        simulation.action_create_quotation()

        # Check that sale order was created
        self.assertTrue(simulation.sale_order_id)

        # Check that opportunity is linked to sale order
        if "opportunity_id" in simulation.sale_order_id._fields:
            self.assertEqual(
                simulation.sale_order_id.opportunity_id, self.opportunity_with_partner
            )

    def test_action_create_quotation_without_opportunity(self):
        """Test that creating a quotation from simulation
        without opportunity works normally."""
        # Create a confirmed simulation without opportunity
        simulation = self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "state": "confirmed",
            }
        )

        # Create quotation
        simulation.action_create_quotation()

        # Check that sale order was created
        self.assertTrue(simulation.sale_order_id)

        # Check that opportunity is not set (should be False)
        if "opportunity_id" in simulation.sale_order_id._fields:
            self.assertFalse(simulation.sale_order_id.opportunity_id)

    def test_simulation_opportunity_readonly_states(self):
        """Test that opportunity_id field has states defined for readonly."""
        # Check that opportunity_id field has states defined
        field = self.BudgetSimulation._fields.get("opportunity_id")
        self.assertTrue(field)
        self.assertTrue(field.states)
        self.assertIn("confirmed", field.states)
        self.assertIn("quotation", field.states)
        self.assertIn("cancelled", field.states)
