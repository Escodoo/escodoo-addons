# Copyright 2021 - TODAY, Marcel Savegnago
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    """CRM Lead extensions for ICP (Ideal Customer Profile) qualification.

    This model adds structured business fields (profile, size, tech maturity,
    budget, etc.) and computes an ICP score and a suggested ICP classification.
    The manual ICP classification remains user-editable (via button or direct edit),
    while the suggestion is recomputed automatically.
    """

    _inherit = "crm.lead"

    # ---------------------------------------------------------------------
    # Profile / Size / Segment
    # ---------------------------------------------------------------------
    escodoo_primary_interest = fields.Selection(
        [
            ("seeking_erp", "My company is seeking an ERP"),
            ("using_odoo", "My company uses Odoo and needs services or improvements"),
            (
                "external_consultant",
                "I am an external consultant and want to recommend Odoo",
            ),
            ("partnership_opportunity", "Partnership Opportunity"),
        ],
        string="Primary Interest",
        tracking=True,
        index=True,
        help=(
            "Indicates the lead’s primary intent regarding Odoo/ERP:\n"
            "- My company is seeking an ERP: the company is looking "
            "to adopt an ERP.\n"
            "- My company uses Odoo and needs services or improvements: "
            "already uses Odoo and seeks support/evolution.\n"
            "- I am an external consultant and want to recommend Odoo: "
            "a consultant evaluating or proposing Odoo to clients.\n"
            "- Partnership Opportunity: a potential commercial or "
            "strategic partnership."
        ),
    )

    escodoo_company_size = fields.Selection(
        [
            ("micro", "Fewer than 5 employees"),
            ("small", "5-20 employees"),
            ("medium_small", "20-50 employees"),
            ("medium", "50-100 employees"),
            ("medium_large", "100-250 employees"),
            ("large", "More than 250 employees"),
        ],
        string="Company Size",
        tracking=True,
        index=True,
        help="Approximate number of employees.",
    )

    escodoo_user_count = fields.Selection(
        [
            ("1_5", "1–5 users"),
            ("6_10", "6–10 users"),
            ("11_20", "11–20 users"),
            ("21_50", "21–50 users"),
            ("51_100", "51–100 users"),
            ("100_plus", "More than 100 users"),
        ],
        string="Estimated Odoo Users",
        tracking=True,
        index=True,
        help=(
            "Estimated number of active Odoo users in the company. "
            "Helps with scoping/effort estimation and infrastructure sizing. "
            "Used only for internal planning — not related to licensing."
        ),
    )

    escodoo_customer_profile = fields.Selection(
        string="Customer Profile",
        selection=[
            ("enterprise", "Enterprise"),
            ("startups_tech", "Startups / Tech"),
            ("middle_market", "Middle Market"),
            ("civic_engagement", "Civic Engagement"),
            ("other", "Other"),
        ],
        tracking=True,
        help=(
            "High-level classification of the customer's business segment "
            "or market context. This helps align the lead with the ICP "
            "and tailor the sales approach.\n\n"
            "Guidelines:\n"
            "- Enterprise → Large corporations or groups with complex "
            "operations.\n"
            "- Startups / Tech → Fast-growing technology or digital-native "
            "companies.\n"
            "- Middle Market → Established mid-sized companies with "
            "structured departments.\n"
            "- Civic Engagement → NGOs, cooperatives, or organizations "
            "with public/social focus.\n"
            "- Other → When the business type does not fit the categories "
            "above."
        ),
    )

    # ---------------------------------------------------------------------
    # Systems / Team
    # ---------------------------------------------------------------------
    escodoo_has_management_system = fields.Boolean(
        string="Has Management/ERP System?",
        tracking=True,
        index=True,
        help="Indicates whether the company currently uses any management/ERP system.",
    )

    escodoo_management_system_name = fields.Char(
        string="Management System Name",
        tracking=True,
        help="Name of the current management/ERP system in use (if any).",
    )

    escodoo_has_dedicated_team = fields.Boolean(
        string="Has a Dedicated Team",
        tracking=True,
        index=True,
        help=(
            "Indicates whether the customer has an internal team dedicated "
            "to supporting the ERP project. Typically includes a key user, "
            "manager, or technical contact responsible for coordination "
            "and validation.\n\n"
            "Guidelines:\n"
            "- Enable if staff are committed to following the project, "
            "testing features, and facilitating decision-making.\n"
            "- Disable if the customer depends entirely on external "
            "support or has no internal resources allocated."
        ),
    )

    escodoo_technological_maturity = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
        ],
        string="Technological Maturity (Auto)",
        compute="_compute_escodoo_technological_maturity",
        store=True,
        readonly=True,
        help=(
            "Automatically computed technological maturity based on "
            "observable signals:\n"
            "- Uses a management/ERP system.\n"
            "- Has a dedicated internal team for the project.\n"
            "- The 'Integrations' field contains meaningful content "
            "(existing/required integrations).\n"
            "- Monthly fiscal invoices volume is at least 100.\n\n"
            "Scoring: +1 per signal (0–4). Mapping → 0–1: Low, 2: Medium, "
            "3–4: High.\n"
            "This field is read-only and updated by the system; use a "
            "manual override only if justified."
        ),
    )

    # ---------------------------------------------------------------------
    # Financial Indicators
    # ---------------------------------------------------------------------
    escodoo_annual_revenue = fields.Monetary(
        string="Annual Revenue (12m)",
        currency_field="company_currency",
        tracking=True,
        help=(
            "Total gross revenue generated by the company over the last "
            "12 months. Used to gauge financial scale and as an input "
            "to ICP scoring and project sizing."
        ),
    )

    escodoo_average_ticket = fields.Monetary(
        string="Average Invoice Value (12m)",
        currency_field="company_currency",
        tracking=True,
        help=(
            "Average value of posted sales invoices during the last 12 months. "
            "Helps understand transaction profile and throughput, informing\
                 complexity estimates."
        ),
    )

    escodoo_monthly_fiscal_docs = fields.Integer(
        string="Average Fiscal Invoices / Month (12m)",
        tracking=True,
        help=(
            "Average number of fiscal sales invoices (NF-e, NFS-e, etc.) "
            "issued per month over the last 12 months. Helps estimate "
            "operational load, integration needs, and technological "
            "maturity."
        ),
    )

    # ---------------------------------------------------------------------
    # Budget & Planning
    # ---------------------------------------------------------------------
    escodoo_project_budget = fields.Monetary(
        "Project Budget",
        currency_field="company_currency",
        tracking=True,
        help=(
            "Estimated amount the customer is willing or able to invest in the\
                 Odoo project.\n\n"
            "Guidelines:\n"
            "- Capture the declared/expected investment range (implementation,\
                 customization, total cost).\n"
            "- If not exact, estimate based on company size, modules in scope, or\
                 negotiation context.\n"
            "- Used to assess feasibility and contributes to the ICP score."
        ),
    )

    escodoo_project_release_date = fields.Date(
        "Target Go-live Date",
        tracking=True,
        help=(
            "Planned or desired go-live date for the Odoo project.\n\n"
            "Guidelines:\n"
            "- Record when the customer expects the system to be operational.\n"
            "- Helps align the implementation schedule and assess urgency.\n"
            "- If unknown, provide an estimated quarter or month based on context."
        ),
    )

    escodoo_budget_gap = fields.Monetary(
        string="Budget Gap (Expected − Budget)",
        currency_field="company_currency",
        compute="_compute_escodoo_budget_gap",
        store=False,
        readonly=True,
        help=(
            "Difference between expected project revenue and the "
            "customer's declared budget.\n\n"
            "Interpretation:\n"
            "- Positive → expected revenue exceeds the available "
            "budget.\n"
            "- Negative → budget exceeds the current project "
            "estimate.\n\n"
            "A quick indicator of financial alignment or potential "
            "gap during negotiations."
        ),
    )

    # ---------------------------------------------------------------------
    # Project Descriptions, pains and integrations
    # ---------------------------------------------------------------------
    escodoo_project_description = fields.Html(
        string="General Description",
        help=(
            "High-level overview of the project: business goals, functional scope, and "
            "expected outcomes.\n\n"
            "Guidelines:\n"
            "- Summarize objectives and covered areas (e.g., Sales, Inventory, "
            "Accounting).\n"
            "- Indicate whether it is an implementation, migration, or improvement "
            "initiative.\n"
            "- Mention key stakeholders, constraints, or special considerations when "
            "relevant.\n"
            "- Helps consultants and account managers with quick context."
        ),
    )

    escodoo_project_primary_pain = fields.Html(
        string="Primary Pains",
        help=(
            "Key operational or strategic problems the customer expects "
            "to address with Odoo.\n\n"
            "Guidelines:\n"
            "- Focus on the top 1–3 pains driving scope and urgency "
            "(e.g., lack of integration, manual processes, low "
            "visibility, compliance issues).\n"
            "- Prefer the customer's own words to preserve context "
            "and nuance.\n"
            "- Clarify impact (cost, risk, SLAs) and urgency to "
            "support prioritization."
        ),
    )

    escodoo_project_secondary_pain = fields.Html(
        string="Secondary Pains",
        help=(
            "Additional operational or strategic problems that are "
            "relevant but not the top priority.\n\n"
            "Guidelines:\n"
            "- Capture complementary or follow-up issues to tackle "
            "after the primary pains.\n"
            "- Keep the customer’s phrasing when possible; note "
            "dependencies if any.\n"
            "- Helps refine the roadmap once primary pains are "
            "addressed."
        ),
    )

    escodoo_project_integration = fields.Html(
        string="Integrations",
        help=(
            "Existing or planned integrations between Odoo and other systems.\n\n"
            "Guidelines:\n"
            "- List external platforms/APIs that must exchange data with Odoo "
            "(e-commerce, logistics, finance, legacy ERP, etc.).\n"
            "- Indicate status (existing vs. to-be-developed), direction of data flow, "
            "and frequency/triggers when applicable.\n"
            "- Helps estimate technical complexity, sequencing, and project scope."
        ),
    )

    # ---------------------------------------------------------------------
    # ICP (manual + computed + score)
    # ---------------------------------------------------------------------
    escodoo_icp_manual_classification = fields.Selection(
        string="ICP Manual Classification",
        selection=[
            ("no_fit", "No Fit"),
            ("low_fit", "Low Fit"),
            ("medium_fit", "Medium Fit"),
            ("high_fit", "High Fit"),
        ],
        default=False,
        tracking=True,
        index=True,
        help=(
            "Manual ICP classification assigned by the sales team. Use this to override\
                 the automatic "
            "ICP suggestion when additional qualitative insight is available.\n\n"
            "Guidelines:\n"
            "- High Fit → Ideal profile (clear alignment in size, maturity, budget)\n"
            "- Medium Fit → Partial alignment or requires adaptation\n"
            "- Low Fit → Weak alignment but potentially viable\n"
            "- No Fit → Outside target or not a viable opportunity"
        ),
    )

    escodoo_icp_manual_classification_reason = fields.Char(
        string="ICP Manual Reason",
        tracking=True,
        help=(
            "Free-text justification for setting a manual ICP classification.\n\n"
            "Use this to capture the business rationale (e.g., special partnership, "
            "board sponsorship, strategic account, atypical timing/budget)."
        ),
    )

    escodoo_icp_score = fields.Integer(
        string="ICP Score",
        compute="_compute_escodoo_icp_score",
        store=True,
        help=(
            "Computed ICP score based on company size, tech maturity, "
            "project budget (or expected revenue as fallback), "
            "expected revenue, and predictive signals."
        ),
    )

    escodoo_icp_classification = fields.Selection(
        [
            ("no_fit", "No Fit"),
            ("low_fit", "Low Fit"),
            ("medium_fit", "Medium Fit"),
            ("high_fit", "High Fit"),
        ],
        string="ICP Classification",
        compute="_compute_escodoo_icp_score",
        store=True,
        help=(
            "Automatically suggested ICP classification calculated from "
            "measurable lead attributes (company size, technological "
            "maturity, project budget/expected revenue, and predictive "
            "probability).\n\n"
            "Interpretation:\n"
            "- High Fit → Excellent alignment; strong lead.\n"
            "- Medium Fit → Partial alignment; may require adjustments "
            "or validation.\n"
            "- Low Fit → Weak alignment; limited potential but possible.\n"
            "- No Fit → Outside target; not recommended to prioritize.\n\n"
            "This value can be manually overridden via 'ICP Classification' "
            "when human judgment provides context."
        ),
    )

    # =====================================================================
    # Create/Write
    # =====================================================================
    @api.model_create_multi
    def create(self, vals_list):
        """Server-side safety to mirror onchange behavior on create."""
        for vals in vals_list:
            # If has_management_system is provided and False -> clear name
            if "escodoo_has_management_system" in vals and not vals.get(
                "escodoo_has_management_system"
            ):
                vals["escodoo_management_system_name"] = False

            # If manual ICP classification is provided and False/0 -> clear reason
            if "escodoo_icp_manual_classification" in vals and not vals.get(
                "escodoo_icp_manual_classification"
            ):
                vals["escodoo_icp_manual_classification_reason"] = False

        return super().create(vals_list)

    def write(self, vals):
        """Server-side safety to mirror onchange behavior on write."""
        # If boolean is explicitly set to False, clear the dependent name field
        if "escodoo_has_management_system" in vals and not vals.get(
            "escodoo_has_management_system"
        ):
            vals = dict(vals)
            vals["escodoo_management_system_name"] = False

        # If manual ICP classification is explicitly set to False/0, clear reason
        if "escodoo_icp_manual_classification" in vals and not vals.get(
            "escodoo_icp_manual_classification"
        ):
            vals = dict(vals)
            vals["escodoo_icp_manual_classification_reason"] = False

        return super().write(vals)

    # =====================================================================
    # Onchanges
    # =====================================================================
    @api.onchange("escodoo_has_management_system")
    def _onchange_clear_mgmt_system_name(self):
        """UX: when the boolean 'Has Management/ERP System?' is unchecked,
        clear the 'Management System Name' field on the form."""
        for lead in self:
            if lead.escodoo_has_management_system is False:
                lead.escodoo_management_system_name = False

    @api.onchange("escodoo_icp_manual_classification")
    def _onchange_icp_manual_clear_reason(self):
        """UX: when the manual ICP classification is cleared (False/0),
        also clear the manual reason."""
        for lead in self:
            if not lead.escodoo_icp_manual_classification:
                lead.escodoo_icp_manual_classification_reason = False

    # =====================================================================
    # Computes
    # =====================================================================
    @api.depends("expected_revenue", "escodoo_project_budget")
    def _compute_escodoo_budget_gap(self):
        """Compute the difference between expected
        revenue and project budget.
        If either side is missing, the field is
        set to False so the view can hide it via attrs.
        """
        for lead in self:
            er = lead.expected_revenue or 0.0
            pb = lead.escodoo_project_budget or 0.0
            lead.escodoo_budget_gap = (er - pb) if (er and pb) else False

    @api.depends(
        "escodoo_company_size",
        "escodoo_technological_maturity",
        "escodoo_project_budget",
        "escodoo_primary_interest",
        "escodoo_has_dedicated_team",
        "escodoo_has_management_system",
        "expected_revenue",
        "escodoo_user_count",
        "escodoo_project_release_date",
        "escodoo_customer_profile",
        "automated_probability",
        "escodoo_icp_manual_classification",
        "equity_capital",
    )
    def _compute_escodoo_icp_score(self):  # noqa: C901
        """Compute ICP numeric score and suggested classification.

        Components (max ~100; all configurable via ir.config_parameter):
        - Company size:              0–25          (escodoo_icp.size_pts)
        - Tech maturity (auto):      0–15          (escodoo_icp.tech_pts)
        - Budget/Expected Rev.:      0–25 (bands)  (escodoo_icp.budget_bands)
        - Primary interest:          0–15          (escodoo_icp.interest_pts)
        - Org signals:               0–4  (+2/+2)  (escodoo_icp.org_pts)
        - Expected revenue:          0–10 (bands)  (escodoo_icp.expected_rev_bands)
        - Equity capital:            0–10 (bands)  (escodoo_icp.equity_bands)  ← NEW
        - Go-live urgency:           0–10 (months) (escodoo_icp.urgency_rules)
        - Estimated users:          -5–10          (escodoo_icp.users_pts)
        - Customer profile:          0–10          (escodoo_icp.profile_pts)

        Notes:
        - For budget points, use escodoo_project_budget; if absent, fall back to
        expected_revenue.
        - Optional: if escodoo_icp.use_equity_in_budget_base is true, equity is
        considered in the budget base as max(project_budget, expected_revenue,
        equity_capital).
        - Automated probability is linearly scaled up to MAX_PROB_PTS.
        - If 'escodoo_icp_manual_classification' is set, it overrides the suggested
        classification after the score calculation is completed.
        """
        import json

        ICP = self.env["ir.config_parameter"].sudo()

        def _json_param(key, default):
            try:
                val = ICP.get_param(key)
                return json.loads(val) if val else default
            except Exception:
                return default

        def _num_param(key, default):
            try:
                val = ICP.get_param(key)
                if val is None:
                    return default
                if "." in val:
                    return float(val)
                return int(val)
            except Exception:
                return default

        def _bool_param(key, default=False):
            val = ICP.get_param(key)
            if val is None:
                return default
            return str(val).strip().lower() in {"1", "true", "yes", "y", "t"}

        SIZE_PTS = _json_param(
            "escodoo_icp.size_pts",
            {
                "micro": 0,
                "small": 5,
                "medium_small": 10,
                "medium": 18,
                "medium_large": 22,
                "large": 25,
            },
        )
        TECH_PTS = _json_param(
            "escodoo_icp.tech_pts", {"low": 0, "medium": 7, "high": 15}
        )
        INTEREST_PTS = _json_param(
            "escodoo_icp.interest_pts",
            {
                "seeking_erp": 10,
                "using_odoo": 15,
                "external_consultant": 6,
                "partnership_opportunity": 6,
            },
        )
        USERS_PTS = _json_param(
            "escodoo_icp.users_pts",
            {"1_5": -5, "6_10": 0, "11_20": 4, "21_50": 7, "51_100": 9, "100_plus": 10},
        )
        PROFILE_PTS = _json_param(
            "escodoo_icp.profile_pts",
            {
                "middle_market": 10,
                "enterprise": 9,
                "startups_tech": 8,
                "civic_engagement": 6,
                "other": 4,
            },
        )

        BUDGET_BANDS = _json_param(
            "escodoo_icp.budget_bands",
            [[300000, 25], [150000, 22], [50000, 15], [10000, 8], [1, 2]],
        )
        EXPECTED_REV_BANDS = _json_param(
            "escodoo_icp.expected_rev_bands",
            [[300000, 10], [150000, 8], [50000, 6], [20000, 3], [5000, 1]],
        )
        URGENCY_RULES = _json_param(
            "escodoo_icp.urgency_rules", [[0, 3, 10], [4, 6, 7], [7, 12, 4]]
        )
        ORG_PTS = _json_param(
            "escodoo_icp.org_pts", {"has_dedicated_team": 2, "has_management_system": 2}
        )
        MAX_PROB_PTS = _num_param("escodoo_icp.max_prob_pts", 15)

        SUGGEST_THRESHOLDS = _json_param(
            "escodoo_icp.suggestion_thresholds",
            {"high_fit": 75, "medium_fit": 50, "low_fit": 30},
        )
        t_high = int(SUGGEST_THRESHOLDS.get("high_fit", 75))
        t_med = int(SUGGEST_THRESHOLDS.get("medium_fit", 50))
        t_low = int(SUGGEST_THRESHOLDS.get("low_fit", 30))

        EQUITY_BANDS = _json_param(
            "escodoo_icp.equity_bands",
            [[1000000, 10], [500000, 8], [100000, 5], [10000, 2]],
        )
        USE_EQUITY_IN_BUDGET_BASE = _bool_param(
            "escodoo_icp.use_equity_in_budget_base", False
        )

        def _score_by_bands(value, bands):
            try:
                v = float(value or 0.0)
            except Exception:
                v = 0.0
            for threshold, pts in sorted(bands, key=lambda x: x[0], reverse=True):
                if v >= threshold:
                    return int(pts)
            return 0

        def _urgency_points_by_months(months):
            if months is None:
                return 0
            for mn, mx, pts in URGENCY_RULES:
                if int(mn) <= months <= int(mx):
                    return int(pts)
            return 0

        for lead in self:
            score = 0

            # Company size (0–25)
            score += int(SIZE_PTS.get(lead.escodoo_company_size or "", 0))

            # Tech maturity (0–15)
            score += int(TECH_PTS.get(lead.escodoo_technological_maturity or "", 0))

            # Budget base (optionally reinforced by equity)
            if USE_EQUITY_IN_BUDGET_BASE:
                budget_base = max(
                    float(lead.escodoo_project_budget or 0.0),
                    float(lead.expected_revenue or 0.0),
                    float(getattr(lead, "equity_capital", 0.0) or 0.0),
                )
            else:
                budget_base = (
                    lead.escodoo_project_budget or lead.expected_revenue or 0.0
                )

            # Budget / Expected revenue (0–25)
            score += _score_by_bands(budget_base, BUDGET_BANDS)

            # Primary interest (0–15)
            score += int(INTEREST_PTS.get(lead.escodoo_primary_interest or "", 0))

            # Org signals (+2 each)
            if lead.escodoo_has_dedicated_team:
                score += int(ORG_PTS.get("has_dedicated_team", 2))
            if lead.escodoo_has_management_system:
                score += int(ORG_PTS.get("has_management_system", 2))

            # Expected revenue (0–10)
            score += _score_by_bands(lead.expected_revenue or 0.0, EXPECTED_REV_BANDS)

            # Equity capital (0–10)
            score += _score_by_bands(
                getattr(lead, "equity_capital", 0.0) or 0.0, EQUITY_BANDS
            )

            # Automated probability (0–MAX_PROB_PTS)
            try:
                p = float(getattr(lead, "automated_probability", 0.0) or 0.0)
            except Exception:
                p = 0.0
            prob_pts = int(round((p / 100.0) * MAX_PROB_PTS))
            score += min(MAX_PROB_PTS, max(0, prob_pts))

            # Go-live urgency (0–10)
            urg_pts = 0
            rgd = lead.escodoo_project_release_date
            if rgd:
                try:
                    today = fields.Date.context_today(lead)
                    days = (rgd - today).days
                    months = max(0, int(round(days / 30.0)))
                    urg_pts = _urgency_points_by_months(months)
                except Exception:
                    urg_pts = 0
            score += urg_pts

            # Estimated users (−5 .. +10)
            score += int(USERS_PTS.get(lead.escodoo_user_count or "", 0))

            # Customer profile (0..10)
            score += int(PROFILE_PTS.get(lead.escodoo_customer_profile or "", 0))

            # Cap and suggest
            score = min(int(score), 100)
            if score >= t_high:
                suggested = "high_fit"
            elif score >= t_med:
                suggested = "medium_fit"
            elif score >= t_low:
                suggested = "low_fit"
            else:
                suggested = "no_fit"

            lead.escodoo_icp_score = score
            manual = lead.escodoo_icp_manual_classification
            lead.escodoo_icp_classification = manual or suggested

    @api.depends(
        "escodoo_has_management_system",
        "escodoo_has_dedicated_team",
        "escodoo_project_integration",
        "escodoo_monthly_fiscal_docs",
        "escodoo_user_count",
    )
    def _compute_escodoo_technological_maturity(self):  # noqa: C901
        """Compute tech maturity level from observable signals (tunable via\
             ir.config_parameter).

        Tunables (JSON in ir.config_parameter):
        - escodoo_icp.tech_maturity_rules:
            {
            "has_management_system": {"points": 1},
            "has_dedicated_team":   {"points": 1},
            "has_integrations":     {"points": 1, "html_min_length": 3},
            "monthly_fiscal_docs":  {"points": 1, "min": 300},
            "user_count": {
                    "points": 1,
                    "bands": [
                        "21_50",
                        "51_100",
                        "100_plus",
                    ],
                },

        Meaning:
            - Each rule contributes "points" if its condition is met.

        - escodoo_icp.tech_maturity_levels:
            [["high", 4], ["medium", 2], ["low", 0]]
        Interpretation: first match wins (evaluated in order).

        Backward-compat:
        - If escodoo_icp.tech_maturity_rules/levels are missing, try legacy
        escodoo_icp.tech_signals = {
            "min_monthly_fiscal_docs": 300,
            "min_user_bucket_for_signal": ["21_50","51_100","100_plus"],
            "mapping": {"high_min": 4, "medium_min": 2}
        }
        """
        import json

        ICP = self.env["ir.config_parameter"].sudo()

        def _json_param(key, default):
            try:
                val = ICP.get_param(key)
                return json.loads(val) if val else default
            except Exception:
                return default

        # --- Load tunables with robust fallbacks ---
        RULES = _json_param(
            "escodoo_icp.tech_maturity_rules",
            None,
        )
        LEVELS = _json_param(
            "escodoo_icp.tech_maturity_levels",
            None,
        )

        # Legacy fallback if new keys aren't defined
        if RULES is None or LEVELS is None:
            legacy = _json_param(
                "escodoo_icp.tech_signals",
                {
                    "min_monthly_fiscal_docs": 300,
                    "min_user_bucket_for_signal": ["21_50", "51_100", "100_plus"],
                    "mapping": {"high_min": 4, "medium_min": 2},
                },
            )
            RULES = RULES or {
                "has_management_system": {"points": 1},
                "has_dedicated_team": {"points": 1},
                "has_integrations": {"points": 1, "html_min_length": 3},
                "monthly_fiscal_docs": {
                    "points": 1,
                    "min": int(legacy.get("min_monthly_fiscal_docs", 300) or 300),
                },
                "user_count": {
                    "points": 1,
                    "bands": legacy.get(
                        "min_user_bucket_for_signal",
                        ["21_50", "51_100", "100_plus"],
                    ),
                },
            }
            # Build levels from legacy mapping (first match wins)
            m = legacy.get("mapping", {}) or {}
            LEVELS = LEVELS or [
                ["high", int(m.get("high_min", 4) or 4)],
                ["medium", int(m.get("medium_min", 2) or 2)],
                ["low", 0],
            ]

        def _has_meaningful_html(text, min_len=3):
            """Treat non-empty, non-whitespace content as meaningful."""
            if not text:
                return False
            stripped = str(text).replace("<", " ").replace(">", " ").strip()
            try:
                return len(stripped) >= int(min_len or 0)
            except Exception:
                return len(stripped) >= 3

        for lead in self:
            score = 0

            # has_management_system
            if lead.escodoo_has_management_system:
                score += int(RULES.get("has_management_system", {}).get("points", 0))

            # has_dedicated_team
            if lead.escodoo_has_dedicated_team:
                score += int(RULES.get("has_dedicated_team", {}).get("points", 0))

            # has_integrations (HTML meaningful)
            integ_rule = RULES.get("has_integrations", {})
            if _has_meaningful_html(
                lead.escodoo_project_integration,
                integ_rule.get("html_min_length", 3),
            ):
                score += int(integ_rule.get("points", 0))

            # monthly_fiscal_docs >= min
            docs_rule = RULES.get("monthly_fiscal_docs", {})
            try:
                min_docs = int(docs_rule.get("min", 300))
            except Exception:
                min_docs = 300
            if (lead.escodoo_monthly_fiscal_docs or 0) >= min_docs:
                score += int(docs_rule.get("points", 0))

            # user_count in allowed bands
            users_rule = RULES.get("user_count", {})
            allowed_bands = set(
                users_rule.get("bands", ["21_50", "51_100", "100_plus"])
            )
            if (lead.escodoo_user_count or "") in allowed_bands:
                score += int(users_rule.get("points", 0))

            # Map score →
            # level (first match wins; list like [["high",4],["medium",2],["low",0]])
            level = "low"  # safe fallback
            try:
                for lvl, min_pts in LEVELS:
                    if score >= int(min_pts):
                        level = str(lvl)
                        break
            except Exception:
                # ultra-safe fallback if LEVELS is malformed
                if score >= 4:
                    level = "high"
                elif score >= 2:
                    level = "medium"
                else:
                    level = "low"

            lead.escodoo_technological_maturity = level

    # =====================================================================
    # Constraints
    # =====================================================================
    @api.constrains(
        "escodoo_icp_manual_classification", "escodoo_icp_manual_classification_reason"
    )
    def _check_icp_manual_reason(self):
        for lead in self:
            if (
                lead.escodoo_icp_manual_classification
                and not (lead.escodoo_icp_manual_classification_reason or "").strip()
            ):
                raise ValidationError(
                    _(
                        "Please provide a reason when setting the ICP Manual "
                        "Classification."
                    )
                )
