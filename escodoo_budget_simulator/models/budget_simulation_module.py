# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BudgetSimulationModule(models.Model):
    """Budget Simulation Module.

    This model represents a module within a budget simulation. Each module
    references a module from the catalog and can have its hours adjusted
    per simulation. The final hours are calculated based on the simulation's
    complexity, number of users, and number of companies.
    """

    _name = "budget.simulation.module"
    _description = "Budget Simulation Module"
    _inherit = "budget.line.mixin"
    _order = "sequence, id"

    # Fields
    simulation_id = fields.Many2one(
        "budget.simulation",
        string="Simulation",
        required=True,
        ondelete="cascade",
        help="The budget simulation this module belongs to.",
    )
    module_id = fields.Many2one(
        "budget.module",
        string="Module",
        required=True,
        ondelete="restrict",
        help="The module from the catalog. When selected, the name, code, "
        "and default hours are automatically populated from the catalog entry. "
        "Each module can only be added once per simulation.",
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
    description = fields.Text(
        help="Description of this module. Automatically populated from "
        "the catalog entry when a module is selected, but can be manually "
        "edited if needed.",
    )
    default_hours = fields.Float(
        default=0.0,
        digits=(16, 2),
        help="Default hours from the catalog entry. Automatically populated when "
        "a module is selected. This value is persisted and will not change even "
        "if the catalog entry is modified later. To override, use the Adjusted "
        "Hours field.",
    )

    # Constraints
    _sql_constraints = [
        (
            "unique_simulation_module",
            "UNIQUE(simulation_id, module_id)",
            "Module already exists in this simulation!",
        ),
    ]

    # Methods
    @api.onchange("module_id")
    def _onchange_module_id(self):
        """Update fields when module_id is selected.

        This method automatically populates the name, code, and default_hours
        fields from the selected module catalog entry. These values are persisted
        and will not change even if the catalog entry is modified later.

        Returns:
            None: Updates fields directly on the record.
        """
        if self.module_id:
            self.name = self.module_id.name
            self.code = self.module_id.code
            self.description = self.module_id.description
            self.default_hours = self.module_id.default_hours

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
                    if not vals.get("description"):
                        vals["description"] = module.description
                    if not vals.get("default_hours"):
                        vals["default_hours"] = module.default_hours
        return super().create(vals_list)

    @api.onchange("simulation_id", "module_id")
    def _onchange_update_domain(self):
        """Update domain for module_id based on already added modules.

        This method dynamically filters the module selection dropdown to
        exclude modules that are already added to the simulation, preventing
        duplicates.

        Returns:
            dict: Domain dictionary to filter module_id field.
        """
        if self.simulation_id:
            excluded_ids = (
                self.simulation_id.module_line_ids.filtered(
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
        "simulation_id.complexity",
        "simulation_id.users_qty",
        "simulation_id.company_qty",
    )
    def _compute_final_hours(self):
        """Compute final hours for this simulation module.

        This method calculates the final hours by:
        1. Getting the base hours (adjusted or default)
        2. Applying the complexity factor from the simulation
        3. Applying the users factor from the simulation
        4. Applying the companies factor from the simulation
        5. Multiplying all factors together

        Returns:
            None: Updates final_hours field.
        """
        for rec in self:
            if not rec.simulation_id:
                rec.final_hours = 0.0
                continue

            # Base hours (adjusted or default)
            base_hours = rec._get_base_hours()

            # Apply complexity factor
            complexity_factor = rec._get_complexity_factor(rec.simulation_id.complexity)

            # Users factor: 1% per user above 5, max +40%
            users_factor = rec._get_users_factor(rec.simulation_id.users_qty)

            # Companies factor: 15% per company above 1
            company_factor = rec._get_company_factor(rec.simulation_id.company_qty)

            # Apply all factors
            rec.final_hours = (
                base_hours * complexity_factor * users_factor * company_factor
            )
