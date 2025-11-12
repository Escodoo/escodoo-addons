# Copyright 2024 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    def _timesheet_create_project(self):
        """Override to add sale order partner as follower of the project and its tasks."""
        project = super()._timesheet_create_project()
        if project and self.order_id.partner_id:
            partner_id = self.order_id.partner_id.id
            # Add partner as follower of the project
            project.message_subscribe(partner_ids=[partner_id])
            # Add partner as follower of all existing tasks in the project
            # This covers the case of projects created from templates
            if project.tasks:
                project.tasks.message_subscribe(partner_ids=[partner_id])
        return project
