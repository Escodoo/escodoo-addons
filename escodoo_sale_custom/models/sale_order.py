# Copyright 2025 - Today, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging

from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """Override to check and grant portal access to partner if needed."""
        result = super().action_confirm()

        for order in self:
            partner = order.partner_id
            if not partner:
                continue

            # Check if partner already has portal access
            # Check both the partner and the commercial partner and its children
            commercial_partner = partner.commercial_partner_id
            all_partners = commercial_partner | commercial_partner.child_ids | partner

            portal_users = all_partners.mapped("user_ids").filtered(
                lambda u: u.has_group("base.group_portal")
            )

            if not portal_users:
                # If no access, grant portal access
                try:
                    self._grant_portal_access(partner)
                except UserError as e:
                    # UserError indicates that partner already has access or invalid email
                    # This can happen in race condition cases or if access was
                    # granted between the check and the grant
                    _logger.info(
                        "Portal access already exists or cannot be granted for partner %s: %s",
                        partner.name,
                        str(e),
                    )
                except Exception as e:
                    _logger.warning(
                        "Failed to grant portal access to partner %s: %s",
                        partner.name,
                        str(e),
                    )

        return result

    def _grant_portal_access(self, partner):
        """Grant portal access to partner and send invitation email.

        :param partner: res.partner record
        """
        if not partner.email:
            _logger.warning(
                "Cannot grant portal access to partner %s: no email address",
                partner.name,
            )
            return

        # Create portal wizard
        portal_wizard = self.env["portal.wizard"].create(
            {
                "partner_ids": [(6, 0, [partner.id])],
            }
        )

        # The user_ids compute is executed automatically when accessing the field
        # Find the portal_wizard_user corresponding to the partner
        portal_wizard_user = portal_wizard.user_ids.filtered(
            lambda u: u.partner_id == partner
        )

        if not portal_wizard_user:
            _logger.warning(
                "Could not find portal wizard user for partner %s", partner.name
            )
            return

        # Check if already has access before trying to grant
        portal_wizard_user._compute_group_details()
        if portal_wizard_user.is_portal or portal_wizard_user.is_internal:
            # Already has access, no need to do anything
            return

        # Grant portal access and send invitation
        portal_wizard_user.action_grant_access()
