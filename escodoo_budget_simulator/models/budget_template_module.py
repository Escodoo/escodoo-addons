# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BudgetTemplateModule(models.Model):
    """Budget Template Module.

    This model represents a module within a budget template. Each module
    references a module from the catalog and can have its hours adjusted
    per template. The final hours are calculated based on the template's
    complexity and optional Python formula on the catalog module.
    """

    _name = "budget.template.module"
    _description = "Budget Template Module"
    _inherit = "budget.line.mixin"
    _order = "sequence, id"

    # Fields
    template_id = fields.Many2one(
        "budget.template",
        string="Template",
        required=True,
        ondelete="cascade",
        help="The budget template this module belongs to.",
    )
    module_id = fields.Many2one(
        "budget.module",
        string="Module",
        required=True,
        ondelete="restrict",
        help="The module from the catalog. When selected, the name, code, "
        "and default hours are automatically populated from the catalog entry. "
        "Each module can only be added once per template.",
    )
    name = fields.Char(
        required=True,
        help="Name of the module. Automatically populated from the catalog entry "
        "when a module is selected. This value is persisted and will not change "
        "even if the catalog entry is modified later.",
    )
    code = fields.Char(
        help="Code of the module. Automatically populated from "
        "the catalog entry when a module is selected. This value is persisted "
        "and will not change even if the catalog entry is modified later.",
    )
    default_hours = fields.Float(
        default=0.0,
        digits=(16, 2),
        help="Default hours from the catalog entry. Automatically populated when "
        "a module is selected. This value is persisted and will not change even "
        "if the catalog entry is modified later. To override, use the Adjusted "
        "Hours field.",
    )
    description = fields.Text(
        help="Description of this module in the template. Can be used to "
        "document specific considerations or customizations for this module "
        "in this template.",
    )

    # Constraints
    _sql_constraints = [
        (
            "unique_template_module",
            "UNIQUE(template_id, module_id)",
            "Module already exists in this template!",
        ),
    ]

    # Methods
    @api.onchange("module_id")
    def _onchange_module_id(self):
        """Update fields when module_id is selected.

        This method automatically populates the name, code, default_hours, and
        description fields from the selected module catalog entry. These values
        are persisted and will not change even if the catalog entry is modified
        later.

        Returns:
            None: Updates fields directly on the record.
        """
        if self.module_id:
            self.name = self.module_id.name
            self.code = self.module_id.code
            self.default_hours = self.module_id.default_hours
            self.description = self.module_id.description

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to auto-fill fields from module_id.

        This method ensures that when a module is created via XML or API with
        only module_id specified, all related fields are automatically populated
        from the catalog entry.

        Args:
            vals_list (list): List of dictionaries with field values.

        Returns:
            Recordset: Created records.
        """
        for vals in vals_list:
            if vals.get("module_id") and not vals.get("name"):
                module = self.env["budget.module"].browse(vals["module_id"])
                if module:
                    if not vals.get("name"):
                        vals["name"] = module.name
                    if not vals.get("code"):
                        vals["code"] = module.code
                    if not vals.get("default_hours"):
                        vals["default_hours"] = module.default_hours
                    if not vals.get("description"):
                        vals["description"] = module.description
        return super().create(vals_list)

    @api.onchange("template_id", "module_id")
    def _onchange_update_domain(self):
        """Update domain for module_id based on already added modules.

        This method dynamically filters the module selection dropdown to
        exclude modules that are already added to the template, preventing
        duplicates.

        Returns:
            dict: Domain dictionary to filter module_id field.
        """
        if self.template_id:
            excluded_ids = (
                self.template_id.module_line_ids.filtered(
                    lambda x: x.id != self.id and x.module_id
                )
                .mapped("module_id")
                .ids
            )
            return {
                "domain": {"module_id": [("id", "not in", excluded_ids)]},
            }
        return {"domain": {"module_id": []}}

    @api.depends(
        "default_hours",
        "adjusted_hours",
        "template_id.complexity",
        "template_id.users_qty",
        "template_id.company_qty",
        "module_id.hours_formula",
    )
    def _compute_final_hours(self):
        """Compute final hours for this template module.

        Uses base hours (adjusted or default), the template complexity factor,
        and optionally the catalog module's Python hours formula.

        Returns:
            None: Updates final_hours field.
        """
        for rec in self:
            if not rec.template_id or not rec.module_id:
                rec.final_hours = 0.0
                continue

            tmpl = rec.template_id
            base_hours = rec._get_base_hours()
            rec.final_hours = rec._finalize_line_hours(
                tmpl.complexity,
                tmpl.users_qty,
                tmpl.company_qty,
                base_hours,
                rec.module_id.hours_formula,
            )
