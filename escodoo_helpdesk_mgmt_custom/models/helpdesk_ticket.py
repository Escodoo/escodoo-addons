# Copyright 2025 Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, models


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    def action_request_environment_change(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Request environment update"),
            "res_model": "helpdesk.environment.change.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_source_ticket_id": self.id},
        }
