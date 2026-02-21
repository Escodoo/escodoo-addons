# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestHelpdeskCustomBase(common.TransactionCase):
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

        cls.partner_with_portal = cls.env["res.partner"].create(
            {"name": "Partner With Portal User"}
        )
        cls.portal_user = cls._create_portal_user(
            cls, cls.partner_with_portal, "portal_helpdesk_test"
        )

        cls.partner_no_portal = cls.env["res.partner"].create(
            {"name": "Partner Without Portal User"}
        )

    def _create_portal_user(self, partner, login):
        return (
            self.env["res.users"]
            .with_context(no_reset_password=True)
            .create(
                {
                    "name": partner.name,
                    "login": login,
                    "email": f"{login}@test.com",
                    "partner_id": partner.id,
                    "groups_id": [(6, 0, [self.group_portal.id])],
                }
            )
        )
