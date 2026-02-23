# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCrmLeadEscodooBase(TransactionCase):
    """Base class with shared setup for escodoo_crm_custom tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.lead_model = cls.env["crm.lead"]
        cls.icp_model = cls.env["ir.config_parameter"].sudo()

    @classmethod
    def _create_lead(cls, **kwargs):
        vals = {
            "name": kwargs.pop("name", "Test Lead"),
            "type": kwargs.pop("type", "opportunity"),
        }
        vals.update(kwargs)
        return cls.lead_model.create(vals)


class TestCrmLeadFields(TestCrmLeadEscodooBase):
    """Test basic field creation and default values."""

    def test_create_lead_with_all_custom_fields(self):
        lead = self._create_lead(
            escodoo_primary_interest="seeking_erp",
            escodoo_company_size="medium",
            escodoo_user_count="21_50",
            escodoo_customer_profile="enterprise",
            escodoo_has_management_system=True,
            escodoo_management_system_name="SAP",
            escodoo_has_dedicated_team=True,
            escodoo_annual_revenue=5000000,
            escodoo_average_ticket=1500,
            escodoo_monthly_fiscal_docs=500,
            escodoo_project_budget=200000,
            escodoo_project_release_date=fields.Date.today() + timedelta(days=150),
            escodoo_project_description="<p>Full ERP implementation</p>",
            escodoo_project_primary_pain="<p>Manual processes</p>",
            escodoo_project_secondary_pain="<p>No reporting</p>",
            escodoo_project_integration="<p>e-commerce + logistics</p>",
        )
        self.assertEqual(lead.escodoo_primary_interest, "seeking_erp")
        self.assertEqual(lead.escodoo_company_size, "medium")
        self.assertEqual(lead.escodoo_user_count, "21_50")
        self.assertEqual(lead.escodoo_customer_profile, "enterprise")
        self.assertTrue(lead.escodoo_has_management_system)
        self.assertEqual(lead.escodoo_management_system_name, "SAP")
        self.assertTrue(lead.escodoo_has_dedicated_team)
        self.assertEqual(lead.escodoo_annual_revenue, 5000000)
        self.assertEqual(lead.escodoo_average_ticket, 1500)
        self.assertEqual(lead.escodoo_monthly_fiscal_docs, 500)
        self.assertEqual(lead.escodoo_project_budget, 200000)

    def test_create_minimal_lead(self):
        lead = self._create_lead()
        self.assertFalse(lead.escodoo_primary_interest)
        self.assertFalse(lead.escodoo_company_size)
        self.assertFalse(lead.escodoo_user_count)
        self.assertFalse(lead.escodoo_customer_profile)
        self.assertFalse(lead.escodoo_has_management_system)
        self.assertFalse(lead.escodoo_management_system_name)
        self.assertFalse(lead.escodoo_has_dedicated_team)
        self.assertFalse(lead.escodoo_icp_manual_classification)


class TestCrmLeadCreateWrite(TestCrmLeadEscodooBase):
    """Test create() and write() overrides for data consistency."""

    def test_create_clears_mgmt_system_name_when_boolean_false(self):
        lead = self._create_lead(
            escodoo_has_management_system=False,
            escodoo_management_system_name="Should be cleared",
        )
        self.assertFalse(lead.escodoo_management_system_name)

    def test_create_keeps_mgmt_system_name_when_boolean_true(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_management_system_name="SAP",
        )
        self.assertEqual(lead.escodoo_management_system_name, "SAP")

    def test_create_clears_icp_reason_when_classification_false(self):
        lead = self._create_lead(
            escodoo_icp_manual_classification=False,
            escodoo_icp_manual_classification_reason="Should be cleared",
        )
        self.assertFalse(lead.escodoo_icp_manual_classification_reason)

    def test_write_clears_mgmt_system_name_when_boolean_set_false(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_management_system_name="SAP",
        )
        self.assertEqual(lead.escodoo_management_system_name, "SAP")
        lead.write({"escodoo_has_management_system": False})
        self.assertFalse(lead.escodoo_management_system_name)

    def test_write_keeps_mgmt_system_name_when_boolean_stays_true(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_management_system_name="SAP",
        )
        lead.write({"escodoo_has_management_system": True})
        self.assertEqual(lead.escodoo_management_system_name, "SAP")

    def test_write_clears_icp_reason_when_classification_set_false(self):
        lead = self._create_lead(
            escodoo_icp_manual_classification="high_fit",
            escodoo_icp_manual_classification_reason="Strategic account",
        )
        lead.write({"escodoo_icp_manual_classification": False})
        self.assertFalse(lead.escodoo_icp_manual_classification_reason)


class TestCrmLeadOnchange(TestCrmLeadEscodooBase):
    """Test onchange methods."""

    def test_onchange_clears_mgmt_system_name(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_management_system_name="SAP",
        )
        lead.escodoo_has_management_system = False
        lead._onchange_clear_mgmt_system_name()
        self.assertFalse(lead.escodoo_management_system_name)

    def test_onchange_keeps_mgmt_system_name_when_true(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_management_system_name="SAP",
        )
        lead._onchange_clear_mgmt_system_name()
        self.assertEqual(lead.escodoo_management_system_name, "SAP")

    def test_onchange_clears_icp_reason(self):
        lead = self._create_lead(
            escodoo_icp_manual_classification="high_fit",
            escodoo_icp_manual_classification_reason="Strategic account",
        )
        lead.escodoo_icp_manual_classification = False
        lead._onchange_icp_manual_clear_reason()
        self.assertFalse(lead.escodoo_icp_manual_classification_reason)

    def test_onchange_keeps_icp_reason_when_classification_set(self):
        lead = self._create_lead(
            escodoo_icp_manual_classification="high_fit",
            escodoo_icp_manual_classification_reason="Strategic account",
        )
        lead._onchange_icp_manual_clear_reason()
        self.assertEqual(
            lead.escodoo_icp_manual_classification_reason, "Strategic account"
        )


class TestCrmLeadBudgetGap(TestCrmLeadEscodooBase):
    """Test _compute_escodoo_budget_gap computation."""

    def test_budget_gap_positive(self):
        lead = self._create_lead(
            expected_revenue=200000,
            escodoo_project_budget=150000,
        )
        self.assertEqual(lead.escodoo_budget_gap, 50000)

    def test_budget_gap_negative(self):
        lead = self._create_lead(
            expected_revenue=100000,
            escodoo_project_budget=150000,
        )
        self.assertEqual(lead.escodoo_budget_gap, -50000)

    def test_budget_gap_zero(self):
        lead = self._create_lead(
            expected_revenue=100000,
            escodoo_project_budget=100000,
        )
        self.assertEqual(lead.escodoo_budget_gap, 0)

    def test_budget_gap_false_when_no_expected_revenue(self):
        lead = self._create_lead(
            expected_revenue=0,
            escodoo_project_budget=150000,
        )
        self.assertFalse(lead.escodoo_budget_gap)

    def test_budget_gap_false_when_no_budget(self):
        lead = self._create_lead(
            expected_revenue=200000,
            escodoo_project_budget=0,
        )
        self.assertFalse(lead.escodoo_budget_gap)

    def test_budget_gap_false_when_both_missing(self):
        lead = self._create_lead()
        self.assertFalse(lead.escodoo_budget_gap)


class TestCrmLeadTechMaturity(TestCrmLeadEscodooBase):
    """Test _compute_escodoo_technological_maturity computation."""

    def test_tech_maturity_low_one_signal(self):
        lead = self._create_lead(escodoo_has_management_system=True)
        self.assertEqual(lead.escodoo_technological_maturity, "low")

    def test_tech_maturity_medium_two_signals(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_has_dedicated_team=True,
        )
        self.assertEqual(lead.escodoo_technological_maturity, "medium")

    def test_tech_maturity_medium_three_signals(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_has_dedicated_team=True,
            escodoo_project_integration="<p>e-commerce integration</p>",
        )
        self.assertEqual(lead.escodoo_technological_maturity, "medium")

    def test_tech_maturity_high_four_signals(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_has_dedicated_team=True,
            escodoo_project_integration="<p>e-commerce integration</p>",
            escodoo_monthly_fiscal_docs=500,
        )
        self.assertEqual(lead.escodoo_technological_maturity, "high")

    def test_tech_maturity_high_five_signals(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_has_dedicated_team=True,
            escodoo_project_integration="<p>e-commerce integration</p>",
            escodoo_monthly_fiscal_docs=500,
            escodoo_user_count="51_100",
        )
        self.assertEqual(lead.escodoo_technological_maturity, "high")

    def test_tech_maturity_fiscal_docs_below_threshold(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_monthly_fiscal_docs=100,
        )
        self.assertEqual(lead.escodoo_technological_maturity, "low")

    def test_tech_maturity_user_count_low_band(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_user_count="6_10",
        )
        self.assertEqual(lead.escodoo_technological_maturity, "low")

    def test_tech_maturity_user_count_high_band(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_user_count="100_plus",
        )
        self.assertEqual(lead.escodoo_technological_maturity, "medium")

    def test_tech_maturity_integration_whitespace_only(self):
        lead = self._create_lead(
            escodoo_has_management_system=True,
            escodoo_project_integration="   ",
        )
        self.assertEqual(lead.escodoo_technological_maturity, "low")

    def test_tech_maturity_recompute_on_write(self):
        lead = self._create_lead()
        self.assertEqual(lead.escodoo_technological_maturity, "low")
        lead.write(
            {
                "escodoo_has_management_system": True,
                "escodoo_has_dedicated_team": True,
            }
        )
        self.assertEqual(lead.escodoo_technological_maturity, "medium")


class TestCrmLeadICPScore(TestCrmLeadEscodooBase):
    """Test _compute_escodoo_icp_score and classification."""

    def test_icp_score_empty_lead(self):
        lead = self._create_lead()
        self.assertLessEqual(lead.escodoo_icp_score, 30)
        self.assertEqual(lead.escodoo_icp_classification, "no_fit")

    def test_icp_score_company_size_contribution(self):
        lead = self._create_lead(escodoo_company_size="large")
        self.assertGreaterEqual(lead.escodoo_icp_score, 25)

    def test_icp_score_company_size_micro(self):
        lead = self._create_lead(escodoo_company_size="micro")
        score_micro = lead.escodoo_icp_score

        lead2 = self._create_lead(name="Test Lead Large", escodoo_company_size="large")
        score_large = lead2.escodoo_icp_score

        self.assertGreater(score_large, score_micro)

    def test_icp_score_tech_maturity_contribution(self):
        lead_low = self._create_lead(name="Low maturity")
        lead_high = self._create_lead(
            name="High maturity",
            escodoo_has_management_system=True,
            escodoo_has_dedicated_team=True,
            escodoo_project_integration="<p>API integrations</p>",
            escodoo_monthly_fiscal_docs=500,
            escodoo_user_count="51_100",
        )
        self.assertGreater(lead_high.escodoo_icp_score, lead_low.escodoo_icp_score)

    def test_icp_score_budget_bands(self):
        lead_low = self._create_lead(name="Low budget", escodoo_project_budget=5000)
        lead_mid = self._create_lead(name="Mid budget", escodoo_project_budget=60000)
        lead_high = self._create_lead(name="High budget", escodoo_project_budget=350000)
        self.assertGreater(lead_mid.escodoo_icp_score, lead_low.escodoo_icp_score)
        self.assertGreater(lead_high.escodoo_icp_score, lead_mid.escodoo_icp_score)

    def test_icp_score_budget_fallback_to_expected_revenue(self):
        lead = self._create_lead(
            escodoo_project_budget=0,
            expected_revenue=200000,
        )
        self.assertGreater(lead.escodoo_icp_score, 0)

    def test_icp_score_primary_interest(self):
        lead_erp = self._create_lead(
            name="Seeking ERP", escodoo_primary_interest="seeking_erp"
        )
        lead_odoo = self._create_lead(
            name="Using Odoo", escodoo_primary_interest="using_odoo"
        )
        lead_consult = self._create_lead(
            name="Consultant", escodoo_primary_interest="external_consultant"
        )
        self.assertGreater(lead_odoo.escodoo_icp_score, lead_erp.escodoo_icp_score)
        self.assertGreater(lead_erp.escodoo_icp_score, lead_consult.escodoo_icp_score)

    def test_icp_score_org_signals(self):
        lead_no = self._create_lead(name="No org signals")
        lead_team = self._create_lead(name="Team only", escodoo_has_dedicated_team=True)
        lead_both = self._create_lead(
            name="Both signals",
            escodoo_has_dedicated_team=True,
            escodoo_has_management_system=True,
        )
        self.assertGreater(lead_team.escodoo_icp_score, lead_no.escodoo_icp_score)
        self.assertGreater(lead_both.escodoo_icp_score, lead_team.escodoo_icp_score)

    def test_icp_score_expected_revenue_bands(self):
        lead_low = self._create_lead(name="Low rev", expected_revenue=3000)
        lead_high = self._create_lead(name="High rev", expected_revenue=400000)
        self.assertGreater(lead_high.escodoo_icp_score, lead_low.escodoo_icp_score)

    def test_icp_score_urgency_within_range(self):
        lead = self._create_lead(
            escodoo_project_release_date=fields.Date.today() + timedelta(days=150),
        )
        self.assertGreater(lead.escodoo_icp_score, 0)

    def test_icp_score_no_urgency_without_date(self):
        lead = self._create_lead()
        score_no_date = lead.escodoo_icp_score
        lead2 = self._create_lead(
            name="With date",
            escodoo_project_release_date=fields.Date.today() + timedelta(days=90),
        )
        self.assertGreaterEqual(lead2.escodoo_icp_score, score_no_date)

    def test_icp_score_user_count_negative(self):
        lead = self._create_lead(escodoo_user_count="1_5")
        lead2 = self._create_lead(name="No users")
        self.assertLessEqual(lead.escodoo_icp_score, lead2.escodoo_icp_score)

    def test_icp_score_user_count_high(self):
        lead = self._create_lead(escodoo_user_count="100_plus")
        self.assertGreater(lead.escodoo_icp_score, 0)

    def test_icp_score_customer_profile(self):
        lead_mm = self._create_lead(
            name="Middle Market", escodoo_customer_profile="middle_market"
        )
        lead_other = self._create_lead(name="Other", escodoo_customer_profile="other")
        self.assertGreater(lead_mm.escodoo_icp_score, lead_other.escodoo_icp_score)

    def test_icp_classification_no_fit(self):
        lead = self._create_lead()
        self.assertEqual(lead.escodoo_icp_classification, "no_fit")

    def test_icp_classification_high_fit(self):
        lead = self._create_lead(
            escodoo_company_size="large",
            escodoo_primary_interest="using_odoo",
            escodoo_customer_profile="middle_market",
            escodoo_user_count="100_plus",
            escodoo_has_dedicated_team=True,
            escodoo_has_management_system=True,
            escodoo_management_system_name="Legacy ERP",
            escodoo_project_budget=400000,
            escodoo_monthly_fiscal_docs=600,
            escodoo_project_integration="<p>Multiple API integrations</p>",
            expected_revenue=500000,
            escodoo_project_release_date=fields.Date.today() + timedelta(days=150),
        )
        self.assertGreaterEqual(lead.escodoo_icp_score, 75)
        self.assertEqual(lead.escodoo_icp_classification, "high_fit")

    def test_icp_manual_classification_overrides_suggested(self):
        lead = self._create_lead(
            escodoo_icp_manual_classification="high_fit",
            escodoo_icp_manual_classification_reason="CEO sponsorship",
        )
        self.assertEqual(lead.escodoo_icp_classification, "high_fit")
        self.assertLess(lead.escodoo_icp_score, 75)

    def test_icp_manual_override_no_fit_on_high_score_lead(self):
        lead = self._create_lead(
            escodoo_company_size="large",
            escodoo_primary_interest="using_odoo",
            escodoo_customer_profile="enterprise",
            escodoo_user_count="100_plus",
            escodoo_has_dedicated_team=True,
            escodoo_has_management_system=True,
            escodoo_management_system_name="Legacy ERP",
            escodoo_project_budget=400000,
            expected_revenue=500000,
            escodoo_monthly_fiscal_docs=600,
            escodoo_project_integration="<p>Multiple integrations</p>",
            escodoo_icp_manual_classification="no_fit",
            escodoo_icp_manual_classification_reason="Company going bankrupt",
        )
        self.assertEqual(lead.escodoo_icp_classification, "no_fit")
        self.assertGreater(lead.escodoo_icp_score, 0)

    def test_icp_score_capped_at_100(self):
        lead = self._create_lead(
            escodoo_company_size="large",
            escodoo_primary_interest="using_odoo",
            escodoo_customer_profile="middle_market",
            escodoo_user_count="100_plus",
            escodoo_has_dedicated_team=True,
            escodoo_has_management_system=True,
            escodoo_management_system_name="Legacy",
            escodoo_project_budget=500000,
            expected_revenue=500000,
            escodoo_monthly_fiscal_docs=1000,
            escodoo_project_integration="<p>Heavy integrations</p>",
            escodoo_project_release_date=fields.Date.today() + timedelta(days=150),
        )
        self.assertLessEqual(lead.escodoo_icp_score, 100)

    def test_icp_score_recomputes_on_write(self):
        lead = self._create_lead()
        initial_score = lead.escodoo_icp_score
        lead.write(
            {
                "escodoo_company_size": "large",
                "escodoo_primary_interest": "using_odoo",
                "escodoo_project_budget": 200000,
            }
        )
        self.assertGreater(lead.escodoo_icp_score, initial_score)


class TestCrmLeadICPScoreBands(TestCrmLeadEscodooBase):
    """Test specific band thresholds in ICP scoring."""

    def test_budget_band_lowest(self):
        lead_below = self._create_lead(name="Below min", escodoo_project_budget=0)
        lead_above = self._create_lead(name="Above min", escodoo_project_budget=5)
        self.assertGreater(lead_above.escodoo_icp_score, lead_below.escodoo_icp_score)

    def test_budget_band_10k(self):
        lead = self._create_lead(escodoo_project_budget=10000)
        lead2 = self._create_lead(name="Test Lead 2", escodoo_project_budget=9999)
        self.assertGreaterEqual(lead.escodoo_icp_score, lead2.escodoo_icp_score)

    def test_budget_band_50k(self):
        lead = self._create_lead(escodoo_project_budget=50000)
        lead2 = self._create_lead(name="Test Lead 2", escodoo_project_budget=49999)
        self.assertGreater(lead.escodoo_icp_score, lead2.escodoo_icp_score)

    def test_budget_band_150k(self):
        lead = self._create_lead(escodoo_project_budget=150000)
        lead2 = self._create_lead(name="Test Lead 2", escodoo_project_budget=149999)
        self.assertGreater(lead.escodoo_icp_score, lead2.escodoo_icp_score)

    def test_budget_band_300k(self):
        lead = self._create_lead(escodoo_project_budget=300000)
        lead2 = self._create_lead(name="Test Lead 2", escodoo_project_budget=299999)
        self.assertGreater(lead.escodoo_icp_score, lead2.escodoo_icp_score)

    def test_expected_revenue_band_5k(self):
        lead = self._create_lead(expected_revenue=5000)
        lead2 = self._create_lead(name="Test Lead 2", expected_revenue=4999)
        self.assertGreater(lead.escodoo_icp_score, lead2.escodoo_icp_score)

    def test_expected_revenue_band_300k(self):
        lead = self._create_lead(expected_revenue=300000)
        lead2 = self._create_lead(name="Test Lead 2", expected_revenue=299999)
        self.assertGreater(lead.escodoo_icp_score, lead2.escodoo_icp_score)


class TestCrmLeadICPUrgency(TestCrmLeadEscodooBase):
    """Test go-live urgency scoring in ICP computation."""

    def test_urgency_no_date(self):
        lead = self._create_lead()
        score_base = lead.escodoo_icp_score
        lead2 = self._create_lead(
            name="With urgency",
            escodoo_project_release_date=fields.Date.today() + timedelta(days=150),
        )
        self.assertGreaterEqual(lead2.escodoo_icp_score, score_base)

    def test_urgency_near_term(self):
        lead = self._create_lead(
            escodoo_project_release_date=fields.Date.today() + timedelta(days=60),
        )
        self.assertGreater(lead.escodoo_icp_score, 0)

    def test_urgency_mid_term(self):
        lead = self._create_lead(
            escodoo_project_release_date=fields.Date.today() + timedelta(days=150),
        )
        self.assertGreater(lead.escodoo_icp_score, 0)

    def test_urgency_long_term(self):
        lead = self._create_lead(
            escodoo_project_release_date=fields.Date.today() + timedelta(days=270),
        )
        self.assertGreater(lead.escodoo_icp_score, 0)

    def test_urgency_very_far(self):
        lead = self._create_lead(
            escodoo_project_release_date=fields.Date.today() + timedelta(days=730),
        )
        score_far = lead.escodoo_icp_score
        lead2 = self._create_lead(
            name="Near lead",
            escodoo_project_release_date=fields.Date.today() + timedelta(days=150),
        )
        score_near = lead2.escodoo_icp_score
        self.assertGreaterEqual(score_near, score_far)

    def test_urgency_past_date(self):
        lead = self._create_lead(
            escodoo_project_release_date=fields.Date.today() - timedelta(days=30),
        )
        self.assertGreaterEqual(lead.escodoo_icp_score, 0)


class TestCrmLeadConstraints(TestCrmLeadEscodooBase):
    """Test SQL/Python constraints."""

    def test_constraint_manual_classification_without_reason_raises(self):
        with self.assertRaises(ValidationError):
            self._create_lead(
                escodoo_icp_manual_classification="high_fit",
                escodoo_icp_manual_classification_reason=False,
            )

    def test_constraint_manual_classification_empty_reason_raises(self):
        with self.assertRaises(ValidationError):
            self._create_lead(
                escodoo_icp_manual_classification="medium_fit",
                escodoo_icp_manual_classification_reason="   ",
            )

    def test_constraint_manual_classification_with_reason_ok(self):
        lead = self._create_lead(
            escodoo_icp_manual_classification="low_fit",
            escodoo_icp_manual_classification_reason="Needs further analysis",
        )
        self.assertEqual(lead.escodoo_icp_manual_classification, "low_fit")

    def test_constraint_no_classification_no_reason_ok(self):
        lead = self._create_lead()
        self.assertFalse(lead.escodoo_icp_manual_classification)
        self.assertFalse(lead.escodoo_icp_manual_classification_reason)

    def test_constraint_write_classification_without_reason_raises(self):
        lead = self._create_lead()
        with self.assertRaises(ValidationError):
            lead.write(
                {
                    "escodoo_icp_manual_classification": "high_fit",
                    "escodoo_icp_manual_classification_reason": False,
                }
            )

    def test_constraint_write_classification_with_reason_ok(self):
        lead = self._create_lead()
        lead.write(
            {
                "escodoo_icp_manual_classification": "medium_fit",
                "escodoo_icp_manual_classification_reason": "Validated with manager",
            }
        )
        self.assertEqual(lead.escodoo_icp_manual_classification, "medium_fit")

    def test_constraint_all_manual_classifications(self):
        for classification in ["no_fit", "low_fit", "medium_fit", "high_fit"]:
            lead = self._create_lead(
                name=f"Lead {classification}",
                escodoo_icp_manual_classification=classification,
                escodoo_icp_manual_classification_reason=f"Reason for {classification}",
            )
            self.assertEqual(lead.escodoo_icp_manual_classification, classification)


class TestCrmLeadICPClassificationThresholds(TestCrmLeadEscodooBase):
    """Test ICP classification thresholds (default: high>=75, medium>=50, low>=30)."""

    def test_low_fit_threshold(self):
        lead = self._create_lead(
            escodoo_company_size="medium_small",
            escodoo_primary_interest="seeking_erp",
            escodoo_user_count="11_20",
            escodoo_customer_profile="other",
        )
        if 30 <= lead.escodoo_icp_score < 50:
            self.assertEqual(lead.escodoo_icp_classification, "low_fit")

    def test_medium_fit_range(self):
        lead = self._create_lead(
            escodoo_company_size="medium",
            escodoo_primary_interest="seeking_erp",
            escodoo_user_count="21_50",
            escodoo_customer_profile="enterprise",
            escodoo_has_dedicated_team=True,
            escodoo_project_budget=60000,
            expected_revenue=60000,
        )
        if 50 <= lead.escodoo_icp_score < 75:
            self.assertEqual(lead.escodoo_icp_classification, "medium_fit")

    def test_classification_changes_on_field_update(self):
        lead = self._create_lead()
        self.assertEqual(lead.escodoo_icp_classification, "no_fit")
        lead.write(
            {
                "escodoo_company_size": "large",
                "escodoo_primary_interest": "using_odoo",
                "escodoo_project_budget": 400000,
                "expected_revenue": 500000,
                "escodoo_customer_profile": "enterprise",
                "escodoo_user_count": "100_plus",
                "escodoo_has_dedicated_team": True,
                "escodoo_has_management_system": True,
                "escodoo_management_system_name": "ERP",
                "escodoo_monthly_fiscal_docs": 600,
                "escodoo_project_integration": "<p>Many integrations</p>",
            }
        )
        self.assertIn(lead.escodoo_icp_classification, ["medium_fit", "high_fit"])


class TestCrmLeadMultiRecord(TestCrmLeadEscodooBase):
    """Test behavior with multiple records (batch operations)."""

    def test_create_multiple_leads(self):
        leads = self.lead_model.create(
            [
                {
                    "name": "Lead A",
                    "type": "opportunity",
                    "escodoo_company_size": "micro",
                },
                {
                    "name": "Lead B",
                    "type": "opportunity",
                    "escodoo_company_size": "large",
                },
                {
                    "name": "Lead C",
                    "type": "opportunity",
                    "escodoo_company_size": "medium",
                },
            ]
        )
        self.assertEqual(len(leads), 3)
        self.assertGreater(leads[1].escodoo_icp_score, leads[0].escodoo_icp_score)

    def test_write_multiple_leads(self):
        lead1 = self._create_lead(name="Lead 1")
        lead2 = self._create_lead(name="Lead 2")
        leads = lead1 | lead2
        leads.write({"escodoo_company_size": "large"})
        for lead in leads:
            self.assertEqual(lead.escodoo_company_size, "large")
            self.assertGreater(lead.escodoo_icp_score, 0)

    def test_batch_create_clearing_logic(self):
        leads = self.lead_model.create(
            [
                {
                    "name": "Lead mgmt False",
                    "type": "opportunity",
                    "escodoo_has_management_system": False,
                    "escodoo_management_system_name": "Should clear",
                },
                {
                    "name": "Lead mgmt True",
                    "type": "opportunity",
                    "escodoo_has_management_system": True,
                    "escodoo_management_system_name": "SAP",
                },
            ]
        )
        self.assertFalse(leads[0].escodoo_management_system_name)
        self.assertEqual(leads[1].escodoo_management_system_name, "SAP")


class TestCrmLeadEdgeCases(TestCrmLeadEscodooBase):
    """Test edge cases and boundary conditions."""

    def test_all_selection_values_company_size(self):
        sizes = ["micro", "small", "medium_small", "medium", "medium_large", "large"]
        for size in sizes:
            lead = self._create_lead(name=f"Lead {size}", escodoo_company_size=size)
            self.assertEqual(lead.escodoo_company_size, size)
            self.assertIsNotNone(lead.escodoo_icp_score)

    def test_all_selection_values_user_count(self):
        counts = ["1_5", "6_10", "11_20", "21_50", "51_100", "100_plus"]
        for count in counts:
            lead = self._create_lead(name=f"Lead {count}", escodoo_user_count=count)
            self.assertEqual(lead.escodoo_user_count, count)

    def test_all_selection_values_primary_interest(self):
        interests = [
            "seeking_erp",
            "using_odoo",
            "external_consultant",
            "partnership_opportunity",
        ]
        for interest in interests:
            lead = self._create_lead(
                name=f"Lead {interest}", escodoo_primary_interest=interest
            )
            self.assertEqual(lead.escodoo_primary_interest, interest)

    def test_all_selection_values_customer_profile(self):
        profiles = [
            "enterprise",
            "startups_tech",
            "middle_market",
            "civic_engagement",
            "other",
        ]
        for profile in profiles:
            lead = self._create_lead(
                name=f"Lead {profile}", escodoo_customer_profile=profile
            )
            self.assertEqual(lead.escodoo_customer_profile, profile)

    def test_zero_monetary_values(self):
        lead = self._create_lead(
            escodoo_annual_revenue=0,
            escodoo_average_ticket=0,
            escodoo_project_budget=0,
            expected_revenue=0,
        )
        self.assertLessEqual(lead.escodoo_icp_score, 30)

    def test_large_monetary_values(self):
        lead = self._create_lead(
            escodoo_project_budget=10000000,
            expected_revenue=10000000,
        )
        self.assertGreater(lead.escodoo_icp_score, 0)
        self.assertLessEqual(lead.escodoo_icp_score, 100)

    def test_html_fields_accept_complex_content(self):
        complex_html = (
            "<div><h1>Title</h1><ul><li>Item 1</li><li>Item 2</li></ul>"
            "<table><tr><td>Data</td></tr></table></div>"
        )
        lead = self._create_lead(
            escodoo_project_description=complex_html,
            escodoo_project_primary_pain=complex_html,
            escodoo_project_secondary_pain=complex_html,
            escodoo_project_integration=complex_html,
        )
        self.assertTrue(lead.escodoo_project_description)
        self.assertTrue(lead.escodoo_project_integration)
