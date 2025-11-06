# Copyright 2025 Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_helpdesk_authorized = fields.Boolean(
        string="Create Tickets from Portal",
        help="If checked, portal users linked to this partner will be automatically "
        "added to the group that has the right to create tickets through the portal.",
        default=False,
        tracking=True,
    )
    helpdesk_authorized_by = fields.Many2one(
        comodel_name="res.partner",
        string="Create Tickets from Portal Authorized By",
        help="Partner who authorized this partner to create tickets through the portal.",
        tracking=True,
    )

    def _sync_helpdesk_group_for_portal_users(self):
        """Add or remove portal users from the group that allows creating
        tickets through the portal."""
        try:
            group_helpdesk_portal = self.env.ref(
                "escodoo_helpdesk_mgmt_custom.group_helpdesk_mgmt_portal_create_ticket"
            )
        except ValueError:
            # Group not found, skip synchronization
            _logger.warning(
                "Helpdesk portal group not found. " "Skipping group synchronization."
            )
            return

        for partner in self:
            portal_users = partner.user_ids.filtered(
                lambda u: u.has_group("base.group_portal")
            )
            if not portal_users:
                continue

            if partner.is_helpdesk_authorized:
                # Add portal users to the group that allows creating
                # tickets through the portal
                users_to_update = portal_users.filtered(
                    lambda u: group_helpdesk_portal not in u.groups_id
                )
                if users_to_update:
                    users_to_update.with_context(skip_helpdesk_group_sync=True).write(
                        {"groups_id": [(4, group_helpdesk_portal.id)]}
                    )
            else:
                # Remove portal users from the group that allows creating
                # tickets through the portal
                users_to_update = portal_users.filtered(
                    lambda u: group_helpdesk_portal in u.groups_id
                )
                if users_to_update:
                    users_to_update.with_context(skip_helpdesk_group_sync=True).write(
                        {"groups_id": [(3, group_helpdesk_portal.id)]}
                    )

    def write(self, vals):
        """Override write to sync portal users group when is_helpdesk_authorized changes."""
        # Validate if partner has portal users before enabling is_helpdesk_authorized
        if "is_helpdesk_authorized" in vals and vals.get("is_helpdesk_authorized"):
            for partner in self:
                portal_users = partner.user_ids.filtered(
                    lambda u: u.has_group("base.group_portal")
                )
                if not portal_users:
                    raise UserError(
                        _(
                            "This partner must have at least one portal user to be "
                            "authorized to create tickets through the portal."
                        )
                    )
            if "helpdesk_authorized_by" not in vals:
                # Get the current user's partner
                current_user_partner = self.env.user.partner_id
                if current_user_partner:
                    vals["helpdesk_authorized_by"] = current_user_partner.id
        # Clear helpdesk_authorized_by when is_helpdesk_authorized is set to False
        elif "is_helpdesk_authorized" in vals and not vals.get(
            "is_helpdesk_authorized"
        ):
            if "helpdesk_authorized_by" not in vals:
                vals["helpdesk_authorized_by"] = False

        result = super().write(vals)
        if "is_helpdesk_authorized" in vals:
            self._sync_helpdesk_group_for_portal_users()
        return result
