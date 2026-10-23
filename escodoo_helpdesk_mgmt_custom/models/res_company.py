# Copyright 2026 Marcus Paulo Dib Lopes
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    environment_update_team_id = fields.Many2one(
        "helpdesk.ticket.team",
        string="Environment update team",
        domain="[('company_id', 'in', [False, id])]",
        help="Fixed team used for environment update requests from this company.",
    )
