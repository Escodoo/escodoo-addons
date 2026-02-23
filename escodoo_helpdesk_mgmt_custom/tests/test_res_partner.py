# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.exceptions import UserError

from .common import TestHelpdeskCustomBase


class TestResPartner(TestHelpdeskCustomBase):
    def test_enable_helpdesk_authorized_with_portal_user(self):
        """Enabling is_helpdesk_authorized adds portal user to helpdesk group."""
        self.assertFalse(self.partner_with_portal.is_helpdesk_authorized)
        self.partner_with_portal.write({"is_helpdesk_authorized": True})
        self.assertTrue(self.partner_with_portal.is_helpdesk_authorized)
        self.assertIn(self.group_helpdesk_portal, self.portal_user.groups_id)

    def test_enable_helpdesk_authorized_without_portal_user_raises(self):
        """Enabling is_helpdesk_authorized without portal user raises UserError."""
        with self.assertRaises(UserError):
            self.partner_no_portal.write({"is_helpdesk_authorized": True})

    def test_disable_helpdesk_authorized_removes_group(self):
        """Disabling is_helpdesk_authorized removes portal user from group."""
        self.partner_with_portal.write({"is_helpdesk_authorized": True})
        self.assertIn(self.group_helpdesk_portal, self.portal_user.groups_id)

        self.partner_with_portal.write({"is_helpdesk_authorized": False})
        self.assertFalse(self.partner_with_portal.is_helpdesk_authorized)
        self.assertNotIn(self.group_helpdesk_portal, self.portal_user.groups_id)

    def test_helpdesk_authorized_by_auto_set(self):
        """helpdesk_authorized_by is auto-set to current user's partner."""
        self.partner_with_portal.write({"is_helpdesk_authorized": True})
        expected_partner = self.env.user.partner_id
        self.assertEqual(
            self.partner_with_portal.helpdesk_authorized_by, expected_partner
        )

    def test_helpdesk_authorized_by_explicit_value(self):
        """Explicit helpdesk_authorized_by value is preserved."""
        other_partner = self.env["res.partner"].create({"name": "Authorizer Partner"})
        self.partner_with_portal.write(
            {
                "is_helpdesk_authorized": True,
                "helpdesk_authorized_by": other_partner.id,
            }
        )
        self.assertEqual(self.partner_with_portal.helpdesk_authorized_by, other_partner)

    def test_helpdesk_authorized_by_cleared_on_disable(self):
        """helpdesk_authorized_by is cleared when authorization is disabled."""
        self.partner_with_portal.write({"is_helpdesk_authorized": True})
        self.assertTrue(self.partner_with_portal.helpdesk_authorized_by)

        self.partner_with_portal.write({"is_helpdesk_authorized": False})
        self.assertFalse(self.partner_with_portal.helpdesk_authorized_by)

    def test_write_unrelated_fields_does_not_trigger_sync(self):
        """Writing fields other than is_helpdesk_authorized skips group sync."""
        self.partner_with_portal.write({"is_helpdesk_authorized": True})
        self.assertIn(self.group_helpdesk_portal, self.portal_user.groups_id)

        with patch.object(
            type(self.partner_with_portal),
            "_sync_helpdesk_group_for_portal_users",
            wraps=self.partner_with_portal._sync_helpdesk_group_for_portal_users,
        ) as mock_sync:
            self.partner_with_portal.write({"name": "New Name"})
            mock_sync.assert_not_called()

        self.assertIn(self.group_helpdesk_portal, self.portal_user.groups_id)

    def test_sync_skips_partner_without_portal_users(self):
        """_sync_helpdesk_group_for_portal_users skips partners without portal users."""
        self.env.cr.execute(
            "UPDATE res_partner SET is_helpdesk_authorized = true WHERE id = %s",
            [self.partner_no_portal.id],
        )
        self.partner_no_portal.invalidate_recordset()
        self.partner_no_portal._sync_helpdesk_group_for_portal_users()

    def test_sync_with_missing_group(self):
        """_sync_helpdesk_group_for_portal_users handles missing group gracefully."""
        with patch.object(
            type(self.env["ir.model.data"]),
            "_xmlid_lookup",
            side_effect=ValueError("not found"),
        ):
            self.partner_with_portal._sync_helpdesk_group_for_portal_users()

    def test_enable_idempotent(self):
        """Enabling authorization twice doesn't duplicate group membership."""
        self.partner_with_portal.write({"is_helpdesk_authorized": True})
        self.assertIn(self.group_helpdesk_portal, self.portal_user.groups_id)

        self.partner_with_portal.write({"is_helpdesk_authorized": True})
        group_count = len(
            self.portal_user.groups_id.filtered(
                lambda g: g.id == self.group_helpdesk_portal.id
            )
        )
        self.assertEqual(group_count, 1)

    def test_disable_idempotent(self):
        """Disabling authorization on an already-disabled partner is safe."""
        self.assertFalse(self.partner_with_portal.is_helpdesk_authorized)
        self.partner_with_portal.write({"is_helpdesk_authorized": False})
        self.assertNotIn(self.group_helpdesk_portal, self.portal_user.groups_id)

    def test_multiple_portal_users(self):
        """All portal users are synced when partner has multiple portal users."""
        portal_user_2 = self._create_portal_user(
            self.partner_with_portal, "portal_helpdesk_test_2"
        )

        self.partner_with_portal.write({"is_helpdesk_authorized": True})
        self.assertIn(self.group_helpdesk_portal, self.portal_user.groups_id)
        self.assertIn(self.group_helpdesk_portal, portal_user_2.groups_id)

        self.partner_with_portal.write({"is_helpdesk_authorized": False})
        self.assertNotIn(self.group_helpdesk_portal, self.portal_user.groups_id)
        self.assertNotIn(self.group_helpdesk_portal, portal_user_2.groups_id)

    def test_default_values(self):
        """Default values for helpdesk authorization fields."""
        partner = self.env["res.partner"].create({"name": "New Partner"})
        self.assertFalse(partner.is_helpdesk_authorized)
        self.assertFalse(partner.helpdesk_authorized_by)
