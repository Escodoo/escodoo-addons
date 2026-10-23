# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    environment_update_team_id = fields.Many2one(
        related="company_id.environment_update_team_id", readonly=False
    )
