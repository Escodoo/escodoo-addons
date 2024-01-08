# Copyright 2024 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProjectTaskType(models.Model):

    _inherit = "project.task.type"

    is_cancelled = fields.Boolean(
        "Cancelling Stage", help="Tasks in this stage are considered as cancelled."
    )
