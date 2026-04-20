# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestHoursFormula(TransactionCase):
    """Validates the hours_formula feature on catalog items (modules, integrations,
    and general activities).

    Scenarios covered:
    - All available formula variables: base_hours, default_hours, complexity_factor,
      users_qty, company_qty, users_factor, company_factor, round, min, max
    - users_qty / company_qty do NOT affect hours when no formula is set
    - adjusted_hours is correctly reflected as base_hours inside a formula
    - Formula result replaces the default calc (not re-multiplied by complexity)
    - Recomputation is triggered when simulation fields change
    - Error cases: invalid syntax, division by zero, non-numeric result, undefined var
    - Mixed formula/default total_hours calculation
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.BudgetSimulation = cls.env["budget.simulation"]
        cls.BudgetModule = cls.env["budget.module"]
        cls.BudgetIntegration = cls.env["budget.integration"]
        cls.BudgetLine = cls.env["budget.line"]
        cls.BudgetSimulationLine = cls.env["budget.simulation.line"]
        cls.partner = cls.env["res.partner"].create({"name": "Formula Test Partner"})

        cls.module = cls.BudgetModule.create(
            {
                "name": "Formula Test Module",
                "code": "formula_test_mod",
                "default_hours": 20.0,
            }
        )
        cls.integration = cls.BudgetIntegration.create(
            {
                "name": "Formula Test Integration",
                "code": "formula_test_int",
                "default_hours": 40.0,
            }
        )
        cls.line = cls.BudgetLine.create(
            {
                "name": "Formula Test Activity",
                "code": "formula_test_act",
                "category": "other",
                "default_hours": 100.0,
            }
        )

    def _sim(self, users_qty=5, company_qty=1, complexity="low", **kw):
        return self.BudgetSimulation.create(
            {
                "partner_id": self.partner.id,
                "users_qty": users_qty,
                "company_qty": company_qty,
                "complexity": complexity,
                **kw,
            }
        )

    def _add_activity(self, sim, adjusted_hours=0.0):
        return self.BudgetSimulationLine.create(
            {
                "simulation_id": sim.id,
                "line_id": self.line.id,
                "adjusted_hours": adjusted_hours,
            }
        )

    def test_formula_constant(self):
        """Formula returning a literal value ignores all other variables."""
        self.line.hours_formula = "42.5"
        sl = self._add_activity(self._sim())
        self.assertAlmostEqual(sl.final_hours, 42.5, places=2)

    def test_formula_users_qty(self):
        """Formula can read users_qty from the simulation."""
        self.line.hours_formula = "base_hours + users_qty"
        # 10 users → 100 + 10 = 110
        self.assertAlmostEqual(
            self._add_activity(self._sim(users_qty=10)).final_hours, 110.0, places=2
        )
        # 25 users → 100 + 25 = 125
        self.assertAlmostEqual(
            self._add_activity(self._sim(users_qty=25)).final_hours, 125.0, places=2
        )

    def test_formula_company_qty(self):
        """Formula can read company_qty from the simulation."""
        self.line.hours_formula = "base_hours + company_qty * 10"
        # 3 companies → 100 + 30 = 130
        self.assertAlmostEqual(
            self._add_activity(self._sim(company_qty=3)).final_hours, 130.0, places=2
        )

    def test_formula_users_factor(self):
        """users_factor = 1% per user above 5, capped at +40%."""
        self.line.hours_formula = "base_hours * users_factor"
        # 10 users: 1 + (10-5)*0.01 = 1.05 → 100 * 1.05 = 105
        self.assertAlmostEqual(
            self._add_activity(self._sim(users_qty=10)).final_hours, 105.0, places=2
        )
        # 5 users (boundary): factor = 1.0 → 100
        self.assertAlmostEqual(
            self._add_activity(self._sim(users_qty=5)).final_hours, 100.0, places=2
        )
        # 50 users: 1 + min(45*0.01, 0.40) = 1.40 → 140
        self.assertAlmostEqual(
            self._add_activity(self._sim(users_qty=50)).final_hours, 140.0, places=2
        )

    def test_formula_company_factor(self):
        """company_factor = 15% per company above 1, no cap."""
        self.line.hours_formula = "base_hours * company_factor"
        # 3 companies: 1 + (3-1)*0.15 = 1.30 → 130
        self.assertAlmostEqual(
            self._add_activity(self._sim(company_qty=3)).final_hours, 130.0, places=2
        )
        # 1 company (boundary): factor = 1.0 → 100
        self.assertAlmostEqual(
            self._add_activity(self._sim(company_qty=1)).final_hours, 100.0, places=2
        )

    def test_formula_complexity_factor(self):
        """Formula can explicitly reference complexity_factor."""
        self.line.hours_formula = "base_hours * complexity_factor * 2"
        # low → 100 * 1.00 * 2 = 200
        self.assertAlmostEqual(
            self._add_activity(self._sim(complexity="low")).final_hours, 200.0, places=2
        )
        # high → 100 * 1.30 * 2 = 260
        self.assertAlmostEqual(
            self._add_activity(self._sim(complexity="high")).final_hours,
            260.0,
            places=2,
        )

    def test_formula_default_hours_includes_complexity(self):
        """default_hours inside the formula = base_hours × complexity_factor."""
        self.line.hours_formula = "default_hours"
        # medium: default_hours_local = 100 * 1.15 = 115
        self.assertAlmostEqual(
            self._add_activity(self._sim(complexity="medium")).final_hours,
            115.0,
            places=2,
        )

    def test_formula_result_not_re_scaled_by_complexity(self):
        """Formula result replaces the default calc"""
        self.line.hours_formula = "base_hours"
        # medium without formula: 100 * 1.15 = 115
        # medium with formula "base_hours": returns raw 100, NOT 115
        self.assertAlmostEqual(
            self._add_activity(self._sim(complexity="medium")).final_hours,
            100.0,
            places=2,
        )

    def test_formula_uses_adjusted_hours_as_base(self):
        """When adjusted_hours > 0, base_hours in the formula equals adjusted_hours."""
        self.line.hours_formula = "base_hours + users_qty"
        # adjusted=150, users=5 → 150 + 5 = 155
        sim = self._sim(users_qty=5)
        sl = self._add_activity(sim, adjusted_hours=150.0)
        self.assertAlmostEqual(sl.final_hours, 155.0, places=2)

    def test_formula_round_min_max(self):
        """Formula supports round(), min(), and max() built-in functions."""
        self.line.hours_formula = "round(max(base_hours * 1.5, 120), 0)"
        sim = self._sim()
        # 100 * 1.5 = 150 → max(150, 120) = 150 → round = 150
        self.assertAlmostEqual(self._add_activity(sim).final_hours, 150.0, places=2)
        # Small line forces the max() branch: 10 * 1.5 = 15 → max(15, 120) = 120
        small_line = self.BudgetLine.create(
            {
                "name": "Small Formula Line",
                "code": "formula_small_act",
                "category": "other",
                "default_hours": 10.0,
                "hours_formula": "round(max(base_hours * 1.5, 120), 0)",
            }
        )
        sl2 = self.BudgetSimulationLine.create(
            {"simulation_id": sim.id, "line_id": small_line.id}
        )
        self.assertAlmostEqual(sl2.final_hours, 120.0, places=2)

    def test_formula_combined_variables(self):
        """Formula combining complexity_factor, users_factor and company_factor."""
        self.line.hours_formula = (
            "base_hours * complexity_factor * users_factor * company_factor"
        )
        # medium=1.15, users=10 → uf=1.05, companies=3 → cf=1.30
        sim = self._sim(users_qty=10, company_qty=3, complexity="medium")
        sl = self._add_activity(sim)
        expected = 100.0 * 1.15 * 1.05 * 1.30
        self.assertAlmostEqual(sl.final_hours, expected, places=2)

    def test_formula_removal_restores_default_calc(self):
        """Clearing hours_formula reverts to base_hours × complexity_factor."""
        self.line.hours_formula = "base_hours + 999"
        sim = self._sim(complexity="medium")
        sl = self._add_activity(sim)
        self.assertAlmostEqual(sl.final_hours, 1099.0, places=2)  # 100 + 999

        self.line.hours_formula = False
        sl._compute_final_hours()
        self.assertAlmostEqual(sl.final_hours, 115.0, places=2)  # 100 * 1.15

    def test_users_qty_change_recomputes_formula_line(self):
        """Changing users_qty on the simulation recomputes formula-based final_hours."""
        self.line.hours_formula = "base_hours + users_qty"
        sim = self._sim(users_qty=5)
        sl = self._add_activity(sim)
        self.assertAlmostEqual(sl.final_hours, 105.0, places=2)  # 100 + 5
        sim.users_qty = 20
        self.assertAlmostEqual(sl.final_hours, 120.0, places=2)  # 100 + 20

    def test_company_qty_change_recomputes_formula_line(self):
        """
        Changing company_qty on the simulation
        recomputes formula-based final_hours.
        """
        self.line.hours_formula = "base_hours + company_qty * 5"
        sim = self._sim(company_qty=1)
        sl = self._add_activity(sim)
        self.assertAlmostEqual(sl.final_hours, 105.0, places=2)  # 100 + 1*5
        sim.company_qty = 4
        self.assertAlmostEqual(sl.final_hours, 120.0, places=2)  # 100 + 4*5

    def test_users_company_no_effect_without_formula(self):
        """Without formula, changing users_qty/company_qty has zero effect on hours."""
        sim = self._sim(users_qty=5, company_qty=1, complexity="low")
        sl = self._add_activity(sim)
        self.assertAlmostEqual(sl.final_hours, 100.0, places=2)
        sim.write({"users_qty": 50, "company_qty": 10})
        sl._compute_final_hours()
        self.assertAlmostEqual(sl.final_hours, 100.0, places=2)

    # ── module formulas ───────────────────────────────────────────────────────

    def test_module_formula_users_qty(self):
        """Module catalog formula using users_qty."""
        self.module.hours_formula = "base_hours + users_qty * 2"
        sim = self._sim(
            users_qty=10, module_line_ids=[(0, 0, {"module_id": self.module.id})]
        )
        mod = sim.module_line_ids[0]
        # 20 + 10*2 = 40
        self.assertAlmostEqual(mod.final_hours, 40.0, places=2)

    def test_module_formula_company_factor(self):
        """Module catalog formula using company_factor."""
        self.module.hours_formula = "base_hours * company_factor"
        sim = self._sim(
            company_qty=3, module_line_ids=[(0, 0, {"module_id": self.module.id})]
        )
        mod = sim.module_line_ids[0]
        # 20 * (1 + 2*0.15) = 20 * 1.30 = 26
        self.assertAlmostEqual(mod.final_hours, 26.0, places=2)

    def test_module_formula_uses_adjusted_hours(self):
        """Module formula receives adjusted_hours as base_hours when adjusted > 0."""
        self.module.hours_formula = "base_hours * 2"
        sim = self._sim()
        sim.write(
            {
                "module_line_ids": [
                    (0, 0, {"module_id": self.module.id, "adjusted_hours": 50.0})
                ]
            }
        )
        mod = sim.module_line_ids[0]
        # base_hours = 50 (adjusted), formula: 50 * 2 = 100
        self.assertAlmostEqual(mod.final_hours, 100.0, places=2)

    def test_module_no_formula_complexity_only(self):
        """Without formula, module hours = default_hours × complexity_factor only."""
        self.module.hours_formula = False
        sim = self._sim(
            users_qty=50,
            company_qty=10,
            complexity="high",
            module_line_ids=[(0, 0, {"module_id": self.module.id})],
        )
        mod = sim.module_line_ids[0]
        # 20 * 1.30 = 26 (users/company ignored)
        self.assertAlmostEqual(mod.final_hours, 26.0, places=2)

    # ── integration formulas ──────────────────────────────────────────────────

    def test_integration_formula_users_factor(self):
        """Integration catalog formula using users_factor."""
        self.integration.hours_formula = "base_hours * users_factor"
        sim = self._sim(
            users_qty=10,
            integration_line_ids=[(0, 0, {"integration_id": self.integration.id})],
        )
        int_line = sim.integration_line_ids[0]
        # 40 * (1 + 5*0.01) = 40 * 1.05 = 42
        self.assertAlmostEqual(int_line.final_hours, 42.0, places=2)

    def test_integration_formula_company_qty(self):
        """Integration catalog formula using company_qty directly."""
        self.integration.hours_formula = "base_hours + company_qty * 8"
        sim = self._sim(
            company_qty=3,
            integration_line_ids=[(0, 0, {"integration_id": self.integration.id})],
        )
        int_line = sim.integration_line_ids[0]
        # 40 + 3*8 = 64
        self.assertAlmostEqual(int_line.final_hours, 64.0, places=2)

    def test_integration_no_formula_complexity_only(self):
        """
        Without formula, integration hours =
        default_hours × complexity_factor only.
        """
        self.integration.hours_formula = False
        sim = self._sim(
            users_qty=50,
            company_qty=10,
            complexity="medium",
            integration_line_ids=[(0, 0, {"integration_id": self.integration.id})],
        )
        int_line = sim.integration_line_ids[0]
        # 40 * 1.15 = 46 (users/company ignored)
        self.assertAlmostEqual(int_line.final_hours, 46.0, places=2)

    def test_invalid_syntax_raises_user_error(self):
        """Syntactically invalid formula raises UserError on evaluation."""
        sl = self._add_activity(self._sim())
        with self.assertRaises(UserError):
            sl._eval_hours_formula("base_hours +", {"base_hours": 100.0})

    def test_division_by_zero_raises_user_error(self):
        """Division by zero inside a formula raises UserError."""
        sl = self._add_activity(self._sim())
        with self.assertRaises(UserError):
            sl._eval_hours_formula("base_hours / 0", {"base_hours": 100.0})

    def test_non_numeric_result_raises_user_error(self):
        """Formula that evaluates to a non-numeric value raises UserError."""
        sl = self._add_activity(self._sim())
        with self.assertRaises(UserError):
            sl._eval_hours_formula("'not_a_number'", {"base_hours": 100.0})

    def test_undefined_variable_raises_user_error(self):
        """Formula referencing an undefined name raises UserError."""
        sl = self._add_activity(self._sim())
        with self.assertRaises(UserError):
            sl._eval_hours_formula("unknown_var * 10", {"base_hours": 100.0})

    def test_mixed_formula_and_default_total(self):
        """total_hours correctly sums formula-driven and complexity-only lines."""
        self.module.hours_formula = "base_hours + 10"  # 20 + 10 = 30
        self.integration.hours_formula = False  # 40 * 1.00 = 40  (low complexity)
        self.line.hours_formula = "base_hours * 2"  # 100 * 2 = 200
        sim = self._sim(
            module_line_ids=[(0, 0, {"module_id": self.module.id})],
            integration_line_ids=[(0, 0, {"integration_id": self.integration.id})],
        )
        self._add_activity(sim)
        sim._compute_totals()
        # 30 + 40 + 200 = 270
        self.assertAlmostEqual(sim.total_hours, 270.0, places=2)
