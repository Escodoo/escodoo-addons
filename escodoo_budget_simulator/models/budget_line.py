# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class BudgetLine(models.Model):
    """General Activitie Catalog.

    This model stores the catalog of general activities that can be used
    in budget templates and simulations. These activities represent specific
    tasks that are not covered by modules or integrations,
    such as discovery, configuration, training, etc.

    Activities from this catalog can be added to budget templates and simulations,
    and the default hours can be adjusted per template or simulation as needed.
    """

    _name = "budget.line"
    _description = "General Activitie Catalog"
    _order = "sequence, name"

    # Fields
    name = fields.Char(
        required=True,
        help="Display name of the budget activitie (e.g., 'Discovery Analysis', "
        "'Initial Configuration', 'User Training'). This is the name that will "
        "appear in selection dropdowns and reports.",
    )
    code = fields.Char(
        help="Unique code for this budget activitie (e.g., 'discovery_analysis', "
        "'initial_config', 'training'). This code is used internally to "
        "identify the activitie. If not provided, the system will generate one "
        "automatically.",
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
        help="Category of this budget activitie. Categories help organize and "
        "group similar activities together. This is used for filtering and "
        "reporting purposes.",
    )
    default_hours = fields.Float(
        default=0.0,
        digits=(16, 2),
        help="Default number of hours for this budget activitie. This value "
        "represents the typical time required to complete this activity. "
        "It can be adjusted per template or simulation as needed. The default "
        "hours are used as the base for calculating final hours with all "
        "factors (complexity, users, companies) applied.",
    )
    description = fields.Text(
        help="Detailed description of this budget activitie. Use this field to "
        "document what this activity involves, its scope, deliverables, or "
        "any special considerations.",
    )
    active = fields.Boolean(
        default=True,
        help="If unchecked, this budget activitie will be hidden and cannot be "
        "selected in new budget templates or simulations.",
    )
    sequence = fields.Integer(
        default=10,
        help="Sequence number for ordering budget activities. Lower numbers appear "
        "first in selection dropdowns and lists.",
    )
