# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestPortalWizardUser(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ctx = {
            "mail_create_nolog": True,
            "mail_create_nosubscribe": True,
            "mail_notrack": True,
            "no_reset_password": True,
            "tracking_disable": True,
        }
        cls.env = cls.env(context=dict(cls.env.context, **ctx))

        cls.group_portal = cls.env.ref("base.group_portal")
        cls.group_helpdesk_portal = cls.env.ref(
            "escodoo_helpdesk_mgmt_custom.group_helpdesk_mgmt_portal_create_ticket"
        )

        cls.partner_authorized = cls.env["res.partner"].create(
            {
                "name": "Authorized Partner",
                "email": "authorized@test.com",
            }
        )
        cls.partner_not_authorized = cls.env["res.partner"].create(
            {
                "name": "Not Authorized Partner",
                "email": "notauthorized@test.com",
            }
        )

    def _run_portal_wizard(self, partner):
        wizard = self.env["portal.wizard"].create({})
        wizard_user = self.env["portal.wizard.user"].create(
            {
                "wizard_id": wizard.id,
                "partner_id": partner.id,
                "email": partner.email,
            }
        )
        wizard_user.action_grant_access()
        return wizard_user

    def test_grant_access_authorized_partner(self):
        """Granting portal access to an authorized partner syncs helpdesk group."""
        self.env.cr.execute(
            "UPDATE res_partner SET is_helpdesk_authorized = true WHERE id = %s",
            [self.partner_authorized.id],
        )
        self.partner_authorized.invalidate_recordset()

        self._run_portal_wizard(self.partner_authorized)

        portal_user = self.partner_authorized.user_ids.filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertTrue(portal_user)
        self.assertIn(self.group_helpdesk_portal, portal_user.groups_id)

    def test_grant_access_not_authorized_partner(self):
        """Granting portal access to a non-authorized partner doesn't add group."""
        self.assertFalse(self.partner_not_authorized.is_helpdesk_authorized)

        self._run_portal_wizard(self.partner_not_authorized)

        portal_user = self.partner_not_authorized.user_ids.filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertTrue(portal_user)
        self.assertNotIn(self.group_helpdesk_portal, portal_user.groups_id)
