# Copyright 2024 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTask(models.Model):

    _inherit = "project.task"

    is_cancelled = fields.Boolean(
        related="stage_id.is_cancelled",
        string="Cancelling Stage",
        readonly=True,
        related_sudo=False,
    )

    @api.onchange("user_id")
    def _onchange_escodoo_user_id(self):
        for rec in self:
            for subtask_id in rec._get_all_subtasks().ids:
                subtask = self.env["project.task"].browse(subtask_id)
                subtask.user_id = rec.user_id

    @api.depends(
        "effective_hours",
        "subtask_effective_hours",
        "planned_hours",
        "is_closed",
        "is_cancelled",
    )
    def _compute_progress_hours(self):
        super()._compute_progress_hours()
        for task in self:
            if task.is_closed and task.progress < 100 and not task.is_cancelled:
                task.progress = 100
