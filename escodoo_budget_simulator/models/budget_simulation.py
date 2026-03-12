# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class BudgetSimulation(models.Model):
    """Budget Simulation.

    Budget simulations are detailed cost estimates for Odoo implementation
    projects. They can be created from scratch or loaded from a template.
    Each simulation contains modules, integrations, and general activities with
    calculated hours based on complexity, number of users, and number of
    companies.

    Simulations can be in four states:
    - Draft: Can be edited and modified
    - Confirmed: Locked and can be converted to a sale order
    - Quotation Created: A sale order has been created from this simulation
    - Cancelled: Archived and cannot be modified

    Once confirmed, a simulation can be converted to a sale order with all
    lines automatically converted to order lines. Once a sale order is created,
    the simulation cannot be reset to draft.
    """

    _name = "budget.simulation"
    _description = "Budget Simulation"
    _inherit = ["mail.thread", "mail.activity.mixin", "budget.mixin"]
    _order = "create_date desc"

    # Fields
    name = fields.Char(
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _("New"),
        help="Unique name/identifier for this budget simulation. Automatically "
        "generated from a sequence when created. Format: BSIM-XXXX.",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
        tracking=True,
        help="The customer/partner for this budget simulation. This partner "
        "will be used when creating a sale order from this simulation.",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        required=True,
        help="The company for this budget simulation. This determines the "
        "currency and other company-specific settings.",
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="company_id.currency_id",
        readonly=True,
        store=True,
        help="Currency for this budget simulation. Automatically set from the "
        "company's currency.",
    )
    template_id = fields.Many2one(
        "budget.template",
        string="Template",
        tracking=True,
        domain=[("state", "=", "confirmed")],
        help="Optional budget template to load data from. Only confirmed "
        "templates are available for selection. When a template is selected, "
        "you can use the 'Load from Template' button to populate this "
        "simulation with the template's modules, integrations, and lines.",
    )
    description = fields.Html(
        help="Detailed description of this budget simulation. Use this field "
        "to document the project scope, requirements, or any special "
        "considerations. This field supports HTML formatting for rich text "
        "content.",
    )

    date = fields.Date(
        string="Simulation Date",
        required=True,
        default=fields.Date.today,
        tracking=True,
        help="Date when this budget simulation was created or last updated. "
        "Used for reporting and filtering purposes.",
    )

    users_qty = fields.Integer(
        required=True,
        tracking=True,
        help="Total number of users for this simulation. This value is used "
        "to calculate the users factor: 1% per user above 5, with a maximum "
        "increase of 40%. Can be loaded from a template or set manually.",
    )
    company_qty = fields.Integer(
        required=True,
        tracking=True,
        help="Total number of companies for this simulation. This value is "
        "used to calculate the companies factor: 15% per company above 1, with "
        "no maximum limit. Can be loaded from a template or set manually.",
    )
    complexity = fields.Selection(
        required=True,
        tracking=True,
        help="Complexity level for this simulation. This affects the complexity "
        "factor applied to all lines: Low = 1.00x, Medium = 1.15x, High = 1.30x. "
        "Can be loaded from a template or set manually.",
    )
    integration_line_ids = fields.One2many(
        "budget.simulation.integration",
        "simulation_id",
        string="Integrations",
        copy=True,
        help="List of integrations included in this simulation. These "
        "integrations can be added manually or loaded from a template. Each "
        "integration can have its hours adjusted per simulation.",
    )
    module_line_ids = fields.One2many(
        "budget.simulation.module",
        "simulation_id",
        string="Modules",
        copy=True,
        help="List of modules included in this simulation. These modules can "
        "be added manually or loaded from a template. Each module can have its "
        "hours adjusted per simulation.",
    )
    line_ids = fields.One2many(
        "budget.simulation.line",
        "simulation_id",
        string="General Activities",
        copy=True,
        help="List of general activities included in this simulation. These "
        "activities represent specific tasks (discovery, configuration, "
        "training, etc.) that are not covered by modules or integrations. "
        "They can be added manually or loaded from a template.",
    )
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("quotation", "Quotation Created"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
        readonly=True,
        help="Current state of the simulation. Draft simulations can be "
        "edited and modified. Confirmed simulations are locked and can be "
        "converted to sale orders. Quotation Created indicates that a sale "
        "order has been created from this simulation. Cancelled simulations "
        "are archived and cannot be modified.",
    )
    notes = fields.Html(
        string="Internal Notes",
        help="Internal notes for this budget simulation. These notes are not "
        "visible to the customer and can be used for internal communication, "
        "project planning, or documentation. This field supports HTML "
        "formatting for rich text content.",
    )

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sale Order",
        readonly=True,
        copy=False,
        tracking=True,
        help="The sale order created from this simulation. Once a simulation "
        "is confirmed, it can be converted to a sale order using the 'Create "
        "Quotation' button. This field links back to the created sale order.",
    )

    # Methods
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to generate sequence number for name.

        This method automatically generates a unique name for each simulation
        using a sequence if the name is not provided or is set to "New".

        Args:
            vals_list (list): List of dictionaries with field values.

        Returns:
            Recordset: Created records.
        """
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New") or not vals.get("name"):
                seq = self.env["ir.sequence"].next_by_code("budget.simulation") or _(
                    "New"
                )
                vals["name"] = seq
        return super().create(vals_list)

    def action_load_from_template(self):
        """Load data from selected template, replacing all existing data.

        This method loads all data from the selected template into this
        simulation, including:
        - Default values (complexity, users, companies, description)
        - All integrations from the template
        - All modules from the template
        - All general activities from the template

        Existing data in the simulation is completely replaced. Adjusted hours
        from the template are preserved if they were set.

        Returns:
            bool: True to trigger view reload.

        Raises:
            UserError: If no template is selected.
        """
        self.ensure_one()
        if not self.template_id:
            raise UserError(_("Please select a template first."))

        template = self.template_id

        # Load default values (override if template has defaults)
        if template.complexity:
            self.complexity = template.complexity
        if template.users_qty:
            self.users_qty = template.users_qty
        if template.company_qty:
            self.company_qty = template.company_qty
        if template.description and not self.description:
            self.description = template.description

        # Clear existing data and load integrations from template
        # (5, 0, 0) removes all existing records
        # Use adjusted_hours from template if > 0, otherwise
        # leave empty to use default_hours
        integration_lines = [(5, 0, 0)]
        for template_integration in template.integration_line_ids:
            integration_lines.append(
                (
                    0,
                    0,
                    {
                        "integration_id": template_integration.integration_id.id,
                        "adjusted_hours": (
                            template_integration.adjusted_hours
                            if template_integration.adjusted_hours > 0
                            else 0.0
                        ),
                    },
                )
            )
        self.integration_line_ids = integration_lines

        # Clear existing data and load modules from template
        # Use adjusted_hours from template if > 0, otherwise
        # leave empty to use default_hours
        module_lines = [(5, 0, 0)]
        for template_module in template.module_line_ids:
            module_lines.append(
                (
                    0,
                    0,
                    {
                        "module_id": template_module.module_id.id,
                        "adjusted_hours": (
                            template_module.adjusted_hours
                            if template_module.adjusted_hours > 0
                            else 0.0
                        ),
                    },
                )
            )
        self.module_line_ids = module_lines

        # Clear existing data and load lines from template
        lines = [(5, 0, 0)]
        for template_line in template.line_ids:
            line_vals = {
                "name": template_line.name,
                "description": template_line.description,
                "category": template_line.category,
                "default_hours": template_line.default_hours,
                "adjusted_hours": template_line.adjusted_hours,
            }
            if template_line.line_id:
                line_vals["line_id"] = template_line.line_id.id
            lines.append((0, 0, line_vals))
        self.line_ids = lines

        # Force recompute of totals
        self._compute_totals()

        # Return True to trigger automatic view reload
        # This will refresh all one2many fields
        # (module_line_ids, integration_line_ids, line_ids)
        # The Odoo framework will automatically reload the view
        # when a method returns True
        return True

    def action_recalculate(self):
        """Recalculate totals based on current rules.

        This method triggers a recalculation of all final hours and the total
        hours for this simulation. It should be used when calculation rules
        have changed or when you want to ensure all values are up to date.

        Returns:
            dict: Action dictionary to display a success notification.
        """
        self.ensure_one()

        # Trigger recompute
        self._compute_totals()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Recalculated"),
                "message": _("Totals have been recalculated."),
                "type": "success",
                "sticky": False,
            },
        }

    def action_confirm(self):
        """Confirm simulation as final.

        This method transitions the simulation from 'draft' to 'confirmed'
        state. Once confirmed, the simulation becomes read-only and can be
        converted to a sale order.

        Returns:
            bool: True if successful.

        Raises:
            UserError: If the simulation is not in 'draft' state.
        """
        self.ensure_one()
        if self.state != "draft":
            raise UserError(_("Only draft simulations can be confirmed."))
        self.state = "confirmed"
        return True

    def action_set_draft(self):
        """Reset simulation to draft state.

        This method transitions the simulation from 'confirmed' or 'quotation' back to
        'draft' state, allowing it to be edited again. It cannot be used if a sale
        order is currently linked to this simulation. If the sale order was deleted
        or cancelled, the link is automatically cleared.

        Returns:
            bool: True if successful.

        Raises:
            UserError: If a sale order is currently linked to this simulation.
        """
        self.ensure_one()
        # Check if sale_order_id exists and is still valid
        if self.sale_order_id:
            # If sale order was deleted or cancelled, clear the link
            if not self.sale_order_id.exists() or self.sale_order_id.state in (
                "cancel",
                "draft",
            ):
                self.sale_order_id = False
            else:
                raise UserError(
                    _(
                        "Cannot reset to draft: a sale order is currently linked "
                        "to this simulation."
                    )
                )
        if self.state in ("confirmed", "quotation", "cancelled"):
            self.state = "draft"
        return True

    def action_view_quotation(self):
        """View the sale order created from this simulation.

        This method opens the sale order form view for the sale order that
        was created from this simulation.

        Returns:
            dict: Action dictionary to open the sale order form view.

        Raises:
            UserError: If no sale order has been created from this simulation.
        """
        self.ensure_one()
        if not self.sale_order_id:
            raise UserError(_("No sale order has been created from this simulation."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Sale Order"),
            "res_model": "sale.order",
            "res_id": self.sale_order_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_create_quotation(self):
        """Create sale order from confirmed simulation.

        This method creates a sale order from this confirmed simulation. All
        modules, integrations, and general activities are converted to sale order
        lines with the calculated final hours as quantities.

        The method:
        1. Gets or creates a service product for hours
        2. Creates a sale order with the simulation's partner
        3. Creates order lines for each module, integration, and detailed line
        4. Links the sale order back to this simulation
        5. Updates the simulation state to 'quotation'

        Returns:
            dict: Action dictionary to open the created sale order form view.

        Raises:
            UserError: If the simulation is not confirmed, if a sale order already
            exists, or if no partner is set.
        """
        self.ensure_one()
        if self.state != "confirmed":
            raise UserError(
                _("Only confirmed simulations can be converted to sale orders.")
            )
        if self.sale_order_id:
            raise UserError(
                _("A sale order has already been created from this simulation.")
            )
        if not self.partner_id:
            raise UserError(_("Please set a partner before creating a sale order."))

        # Get or create a service product for hours
        service_product = self._get_service_product()

        # Create sale order
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_id.id,
                "company_id": self.company_id.id,
                "client_order_ref": self.name,
                "note": self.description or "",
            }
        )

        def _execute_onchanges(records, field_name):
            """Helper method that executes all onchanges associated to a field."""
            for onchange in records._onchange_methods.get(field_name, []):
                for record in records:
                    onchange(record)

        # Create order lines from modules
        sequence = 10
        for module_line in self.module_line_ids.sorted("sequence"):
            if module_line.final_hours > 0:
                description = module_line.name
                if module_line.description:
                    description += f"\n{module_line.description}"
                # Use new() to trigger onchanges, then convert to write values
                sol = self.env["sale.order.line"].new(
                    {
                        "order_id": sale_order.id,
                        "product_id": service_product.id,
                    }
                )
                _execute_onchanges(sol, "product_id")
                sol.product_uom_qty = module_line.final_hours
                _execute_onchanges(sol, "product_uom_qty")
                sol.name = description
                sol.sequence = sequence
                sequence += 10
                self.env["sale.order.line"].create(sol._convert_to_write(sol._cache))

        # Create order lines from integrations
        for integration_line in self.integration_line_ids.sorted("sequence"):
            if integration_line.final_hours > 0:
                description = integration_line.name
                if integration_line.description:
                    description += f"\n{integration_line.description}"
                # Use new() to trigger onchanges, then convert to write values
                sol = self.env["sale.order.line"].new(
                    {
                        "order_id": sale_order.id,
                        "product_id": service_product.id,
                    }
                )
                _execute_onchanges(sol, "product_id")
                sol.product_uom_qty = integration_line.final_hours
                _execute_onchanges(sol, "product_uom_qty")
                sol.name = description
                sol.sequence = sequence
                sequence += 10
                self.env["sale.order.line"].create(sol._convert_to_write(sol._cache))

        # Create order lines from lines
        for line in self.line_ids.sorted("sequence"):
            if line.final_hours > 0:
                description = line.name
                if line.description:
                    description += f"\n{line.description}"
                # Use new() to trigger onchanges, then convert to write values
                sol = self.env["sale.order.line"].new(
                    {
                        "order_id": sale_order.id,
                        "product_id": service_product.id,
                    }
                )
                _execute_onchanges(sol, "product_id")
                sol.product_uom_qty = line.final_hours
                _execute_onchanges(sol, "product_uom_qty")
                sol.name = description
                sol.sequence = sequence
                sequence += 10
                self.env["sale.order.line"].create(sol._convert_to_write(sol._cache))

        # Link sale order to simulation and update state
        self.sale_order_id = sale_order.id
        self.state = "quotation"

        return {
            "type": "ir.actions.act_window",
            "name": _("Sale Order"),
            "res_model": "sale.order",
            "res_id": sale_order.id,
            "view_mode": "form",
            "target": "current",
        }

    def _get_service_product(self):
        """Get or create a service product for hours.

        This method retrieves a service product to use when creating sale order
        lines from the simulation. It follows this priority:
        1. Use the configured default product from system parameters
        2. Search for an existing service product with "hour" in the name
        3. Create a new generic "Consulting Service (Hours)" product

        Returns:
            Recordset: Product product record to use for sale order lines.
        """
        # First, try to get the configured default product
        default_product_id = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("escodoo_budget_simulator.default_quotation_product_id")
        )
        if default_product_id:
            product = self.env["product.product"].browse(int(default_product_id))
            if product.exists() and product.type == "service" and product.sale_ok:
                return product

        # Try to find an existing service product for hours
        # In Odoo 16, use 'type' field
        product = self.env["product.product"].search(
            [
                ("type", "=", "service"),
                ("sale_ok", "=", True),
                ("name", "ilike", "hour"),
            ],
            limit=1,
        )
        if not product:
            # Create a generic service product
            product_template = self.env["product.template"].create(
                {
                    "name": _("Consulting Service (Hours)"),
                    "type": "service",
                    "sale_ok": True,
                    "purchase_ok": False,
                }
            )
            product = product_template.product_variant_id
        return product

    def action_duplicate(self):
        """Duplicate simulation.

        This method creates a copy of this simulation with a new name and
        resets it to draft state. All modules, integrations, and lines are
        copied to the new simulation.

        Returns:
            dict: Action dictionary to open the duplicated simulation form view.
        """
        self.ensure_one()
        # Generate new sequence number for the duplicate
        new_name = self.env["ir.sequence"].next_by_code("budget.simulation") or _("New")
        copy = self.copy(
            {
                "name": new_name,
                "state": "draft",
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": _("Budget Simulation"),
            "res_model": "budget.simulation",
            "res_id": copy.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_cancel(self):
        """Cancel simulation.

        This method transitions the simulation to 'cancelled' state. Cancelled
        simulations and cannot be modified or converted to sale orders.
        Cannot cancel if a sale order has been created.

        Returns:
            bool: True if successful.

        Raises:
            UserError: If the simulation is not in a state that can be cancelled
            or if a sale order has been created.
        """
        self.ensure_one()
        if self.sale_order_id:
            raise UserError(
                _("Cannot cancel a simulation that has a sale order created.")
            )
        if self.state in ("quotation", "cancelled"):
            raise UserError(
                _(
                    "Cannot cancel a simulation that is already cancelled or has a "
                    "quotation created."
                )
            )
        self.state = "cancelled"
        return True

    def action_create_template_from_simulation(self):
        """Open wizard to create template from simulation.

        This method opens a wizard that allows the user to create a budget
        template based on this simulation. The wizard will ask for a template
        name and optional description.

        Returns:
            dict: Action dictionary to open the wizard form view.
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Create Template from Simulation"),
            "res_model": "budget.simulation.create.template.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_simulation_id": self.id,
                "default_description": self.description or "",
            },
        }
