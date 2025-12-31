# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BudgetTemplateIntegration(models.Model):
    """Budget Template Integration.

    This model represents an integration within a budget template. Each
    integration references an integration from the catalog and can have its
    hours adjusted per template. The final hours are calculated based on the
    template's complexity, number of users, and number of companies.
    """

    _name = "budget.template.integration"
    _description = "Budget Template Integration"
    _inherit = "budget.line.mixin"
    _order = "sequence, id"

    # Fields
    template_id = fields.Many2one(
        "budget.template",
        string="Template",
        required=True,
        ondelete="cascade",
        help="The budget template this integration belongs to.",
    )
    integration_id = fields.Many2one(
        "budget.integration",
        string="Integration",
        required=True,
        ondelete="restrict",
        help="The integration from the catalog. When selected, the name, code, "
        "and default hours are automatically populated from the catalog entry. "
        "Each integration can only be added once per template.",
    )
    name = fields.Char(
        required=True,
        help="Name of the integration. Automatically populated from the catalog "
        "entry when an integration is selected. This value is persisted and will "
        "not change even if the catalog entry is modified later.",
    )
    code = fields.Char(
        help="Code of the integration. Automatically populated from the catalog "
        "entry when an integration is selected. This value is persisted and will "
        "not change even if the catalog entry is modified later.",
    )
    default_hours = fields.Float(
        default=0.0,
        digits=(16, 2),
        help="Default hours from the catalog entry. Automatically populated when "
        "an integration is selected. This value is persisted and will not change "
        "even if the catalog entry is modified later. To override, use the "
        "Adjusted Hours field.",
    )
    description = fields.Text(
        help="Description of this integration in the template. Can be used to "
        "document specific considerations or customizations for this integration "
        "in this template.",
    )

    # Constraints
    _sql_constraints = [
        (
            "unique_template_integration",
            "UNIQUE(template_id, integration_id)",
            "Integration already exists in this template!",
        ),
    ]

    # Methods
    @api.onchange("integration_id")
    def _onchange_integration_id(self):
        """Update fields when integration_id is selected.

        This method automatically populates the name, code, default_hours, and
        description fields from the selected integration catalog entry. These
        values are persisted and will not change even if the catalog entry is
        modified later.

        Returns:
            None: Updates fields directly on the record.
        """
        if self.integration_id:
            self.name = self.integration_id.name
            self.code = self.integration_id.code
            self.default_hours = self.integration_id.default_hours
            self.description = self.integration_id.description

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to auto-fill fields from integration_id.

        This method ensures that when an integration is created via XML or API
        with only integration_id specified, all related fields are automatically
        populated from the catalog entry.

        Args:
            vals_list (list): List of dictionaries with field values.

        Returns:
            Recordset: Created records.
        """
        for vals in vals_list:
            if vals.get("integration_id") and not vals.get("name"):
                integration = self.env["budget.integration"].browse(
                    vals["integration_id"]
                )
                if integration:
                    if not vals.get("name"):
                        vals["name"] = integration.name
                    if not vals.get("code"):
                        vals["code"] = integration.code
                    if not vals.get("default_hours"):
                        vals["default_hours"] = integration.default_hours
                    if not vals.get("description"):
                        vals["description"] = integration.description
        return super().create(vals_list)

    @api.onchange("template_id", "integration_id")
    def _onchange_update_domain(self):
        """Update domain for integration_id based on already added integrations.

        This method dynamically filters the integration selection dropdown to
        exclude integrations that are already added to the template, preventing
        duplicates.

        Returns:
            dict: Domain dictionary to filter integration_id field.
        """
        if self.template_id:
            excluded_ids = (
                self.template_id.integration_line_ids.filtered(
                    lambda x: x.id != self.id and x.integration_id
                )
                .mapped("integration_id")
                .ids
            )
            return {
                "domain": {"integration_id": [("id", "not in", excluded_ids)]},
            }
        return {"domain": {"integration_id": []}}

    @api.depends(
        "default_hours",
        "adjusted_hours",
        "template_id.complexity",
        "template_id.users_qty",
        "template_id.company_qty",
    )
    def _compute_final_hours(self):
        """Compute final hours for this template integration.

        This method calculates the final hours by:
        1. Getting the base hours (adjusted or default)
        2. Applying the complexity factor from the template
        3. Applying the users factor from the template
        4. Applying the companies factor from the template
        5. Multiplying all factors together

        Returns:
            None: Updates final_hours field.
        """
        for rec in self:
            if not rec.template_id:
                rec.final_hours = 0.0
                continue

            # Base hours (adjusted or default)
            base_hours = rec._get_base_hours()

            # Apply complexity factor
            complexity_factor = rec._get_complexity_factor(rec.template_id.complexity)

            # Users factor: 1% per user above 5, max +40%
            users_factor = rec._get_users_factor(rec.template_id.users_qty)

            # Companies factor: 15% per company above 1
            company_factor = rec._get_company_factor(rec.template_id.company_qty)

            # Apply all factors
            rec.final_hours = (
                base_hours * complexity_factor * users_factor * company_factor
            )
