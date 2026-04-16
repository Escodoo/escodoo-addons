# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class BudgetSimulationLine(models.Model):
    """Budget Simulation Line.

    This model represents a general activity within a budget simulation.
    Each line references a budget activitie from the catalog and can have its
    hours adjusted per simulation. The final hours are calculated based on
    the simulation's complexity and optional Python formula on the catalog
    activity.
    """

    _name = "budget.simulation.line"
    _description = "Budget Simulation Line"
    _inherit = "budget.line.mixin"
    _order = "sequence, id"

    # Fields
    simulation_id = fields.Many2one(
        "budget.simulation",
        string="Simulation",
        required=True,
        ondelete="cascade",
        help="The budget simulation this line belongs to.",
    )
    line_id = fields.Many2one(
        "budget.line",
        string="Activitie",
        required=True,
        ondelete="restrict",
        help="The budget activitie from the catalog. When selected, the name, "
        "category, default hours, and description are automatically "
        "populated from the catalog entry.",
    )
    name = fields.Char(
        required=True,
        help="Name of this budget activitie. Automatically populated from the "
        "catalog entry when a activitie is selected, but can be manually edited "
        "if needed.",
    )
    category = fields.Selection(
        [
            ("discovery", "Discovery"),
            ("config", "Configuration"),
            ("dev", "Development"),
            ("migration", "Migration"),
            ("train", "Training"),
            ("support", "Support"),
            ("other", "Other"),
        ],
        required=True,
        default="other",
        help="Category of this budget activitie. Automatically populated from the "
        "catalog entry when a activitie is selected. Categories help organize and "
        "group similar activities together.",
    )
    description = fields.Text(
        help="Description of this budget activitie. Automatically populated from "
        "the catalog entry when a activitie is selected, but can be manually "
        "edited if needed.",
    )
    default_hours = fields.Float(
        default=0.0,
        digits=(16, 2),
        help="Default hours from the catalog entry. Automatically populated when "
        "a line is selected. This value is persisted and will not change even if "
        "the catalog entry is modified later. To override, use the Adjusted "
        "Hours field.",
    )

    # Methods
    @api.onchange("line_id")
    def _onchange_line_id(self):
        """Update fields when line_id is selected.

        This method automatically populates the name, category, default_hours,
        and description fields from the selected budget activitie catalog entry. These
        values are persisted and will not change even if the catalog entry is
        modified later.

        Returns:
            None: Updates fields directly on the record.
        """
        if self.line_id:
            self.name = self.line_id.name
            self.category = self.line_id.category
            self.default_hours = self.line_id.default_hours
            self.description = self.line_id.description

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to auto-fill fields from line_id.

        This method ensures that when a line is created via XML or API with
        only line_id specified, all related fields are automatically populated
        from the catalog entry.

        Args:
            vals_list (list): List of dictionaries with field values.

        Returns:
            Recordset: Created records.
        """
        for vals in vals_list:
            if vals.get("line_id") and not vals.get("name"):
                line = self.env["budget.line"].browse(vals["line_id"])
                if line:
                    if not vals.get("name"):
                        vals["name"] = line.name
                    if not vals.get("category"):
                        vals["category"] = line.category
                    if not vals.get("default_hours"):
                        vals["default_hours"] = line.default_hours
                    if not vals.get("description"):
                        vals["description"] = line.description
        return super().create(vals_list)

    @api.depends(
        "default_hours",
        "adjusted_hours",
        "simulation_id.complexity",
        "simulation_id.users_qty",
        "simulation_id.company_qty",
        "line_id.hours_formula",
    )
    def _compute_final_hours(self):
        """Compute final hours for this simulation line.

        Uses base hours (adjusted or default), the simulation complexity factor,
        and optionally the catalog activity's Python hours formula.

        Returns:
            None: Updates final_hours field.
        """
        for rec in self:
            if not rec.simulation_id or not rec.line_id:
                rec.final_hours = 0.0
                continue

            sim = rec.simulation_id
            base_hours = rec._get_base_hours()
            rec.final_hours = rec._finalize_line_hours(
                sim.complexity,
                sim.users_qty,
                sim.company_qty,
                base_hours,
                rec.line_id.hours_formula,
            )
