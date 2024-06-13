# Copyright TODAY, 2024 Matheus Marques <matheus.marques@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProjectTaskType(models.Model):
    _name = "project.task.type"
    _description = "Project Task Type"
    _order = "sequence, id"

    name = fields.Char(string="Name", required=True)
    create_date = fields.Datetime(string="Created on", readonly=True)
    create_uid = fields.Many2one("res.users", string="Created by", readonly=True)
    write_date = fields.Datetime(string="Last Updated on", readonly=True)
    write_uid = fields.Many2one("res.users", string="Last Updated by", readonly=True)
    active = fields.Boolean(string="Active", default=True)
    sequence = fields.Integer(string="Sequence")
    description = fields.Text(string="Description")
    display_name = fields.Char(string="Display Name", readonly=True)
    mail_template_id = fields.Many2one("mail.template", string="Mail Template")
    project_ids = fields.Many2many("project.project", string="Projects")
    rating_template_id = fields.Many2one("mail.template", string="Rating Mail Template")
    is_closed = fields.Boolean(string="Is Closed")
    is_cancelled = fields.Boolean(string="Is Cancelled")
    legend_blocked = fields.Char(string="Legend Blocked")
    legend_done = fields.Char(string="Legend Done")
    legend_normal = fields.Char(string="Legend Normal")
    fold = fields.Boolean(string="Folded in Kanban")


class HrTimesheetSheetLine(models.TransientModel):
    _inherit = "hr_timesheet.sheet.line"

    project_task_type = fields.Many2one("project.task.type", string="Task stage")


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    project_task_type = fields.Many2one("project.task.type", string="Task stage")

    @api.model
    def create(self, vals):
        if "task_id" in vals:
            task = self.env["project.task"].browse(vals["task_id"])
            if task:
                vals["project_task_type"] = task.stage_id.id
        return super(AccountAnalyticLine, self).create(vals)
