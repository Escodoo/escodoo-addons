# Copyright 2025 Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PortalWizardUser(models.TransientModel):
    _inherit = "portal.wizard.user"

    def action_grant_access(self):
        """Override to automatically assign helpdesk group if partner is authorized."""
        result = super().action_grant_access()
        # After granting access, sync helpdesk group if partner is authorized
        if self.partner_id.is_helpdesk_authorized:
            self.partner_id._sync_helpdesk_group_for_portal_users()
        return result
