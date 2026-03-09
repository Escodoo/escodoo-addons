# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class BudgetSimulationCreateTemplateWizard(models.TransientModel):
    """Wizard to create a template from a budget simulation.

    This wizard allows users to create a budget template based on an existing
    budget simulation. The template will include all modules, integrations,
    and general activities from the simulation, along with the default values
    for complexity, users, and companies.
    """

    _name = "budget.simulation.create.template.wizard"
    _description = "Create Template from Simulation Wizard"

    # Fields
    simulation_id = fields.Many2one(
        "budget.simulation",
        string="Simulation",
        required=True,
        readonly=True,
        help="The budget simulation to create a template from.",
    )
    name = fields.Char(
        string="Template Name",
        required=True,
        help="Name for the new budget template. This name should be descriptive "
        "and help identify the template's purpose.",
    )
    description = fields.Html(
        help="Optional description for the new template. If not provided, "
        "the description from the simulation will be used.",
    )

    # Methods
    def action_create_template(self):
        """Create template from simulation.

        This method creates a new budget template based on the selected
        simulation. It copies:
        - Default values (complexity, users, companies, description)
        - All modules with their adjusted hours
        - All integrations with their adjusted hours
        - All general activities with their adjusted hours

        Returns:
            dict: Action dictionary to open the created template form view.

        Raises:
            UserError: If no simulation is selected.
        """
        self.ensure_one()
        if not self.simulation_id:
            raise UserError(_("Please select a simulation."))

        simulation = self.simulation_id

        # Create template with default values from simulation
        template_vals = {
            "name": self.name,
            "description": self.description or simulation.description or "",
            "complexity": simulation.complexity,
            "users_qty": simulation.users_qty,
            "company_qty": simulation.company_qty,
            "state": "draft",
        }
        template = self.env["budget.template"].create(template_vals)

        # Copy integrations from simulation to template
        integration_lines = []
        for sim_integration in simulation.integration_line_ids:
            integration_lines.append(
                (
                    0,
                    0,
                    {
                        "integration_id": sim_integration.integration_id.id,
                        "adjusted_hours": (
                            sim_integration.adjusted_hours
                            if sim_integration.adjusted_hours > 0
                            else 0.0
                        ),
                    },
                )
            )
        template.integration_line_ids = integration_lines

        # Copy modules from simulation to template
        module_lines = []
        for sim_module in simulation.module_line_ids:
            module_lines.append(
                (
                    0,
                    0,
                    {
                        "module_id": sim_module.module_id.id,
                        "adjusted_hours": (
                            sim_module.adjusted_hours
                            if sim_module.adjusted_hours > 0
                            else 0.0
                        ),
                    },
                )
            )
        template.module_line_ids = module_lines

        # Copy lines from simulation to template
        lines = []
        for sim_line in simulation.line_ids:
            line_vals = {
                "name": sim_line.name,
                "description": sim_line.description or "",
                "category": sim_line.category,
                "default_hours": sim_line.default_hours,
                "adjusted_hours": sim_line.adjusted_hours,
            }
            if sim_line.line_id:
                line_vals["line_id"] = sim_line.line_id.id
            lines.append((0, 0, line_vals))
        template.line_ids = lines

        # Force recompute of totals
        template._compute_totals()

        return {
            "type": "ir.actions.act_window",
            "name": _("Budget Template"),
            "res_model": "budget.template",
            "res_id": template.id,
            "view_mode": "form",
            "target": "current",
        }
