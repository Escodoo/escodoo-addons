# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.exceptions import AccessError, UserError
from odoo.tests import Form, TransactionCase, tagged
from odoo.tests.common import new_test_user


@tagged("post_install", "-at_install")
class TestEnvironmentChange(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = new_test_user(
            cls.env,
            login="change_requester",
            groups="helpdesk_mgmt.group_helpdesk_user",
        )
        cls.team = cls.env["helpdesk.ticket.team"].create(
            {
                "name": "Infraestrutura e Atualizações",
                "user_ids": [(6, 0, cls.user.ids)],
            }
        )
        cls.env.company.environment_update_team_id = cls.team
        cls.closed = cls.env["helpdesk.ticket.stage"].create(
            {
                "name": "Executed",
                "sequence": -20,
                "closed": True,
                "team_ids": [(6, 0, cls.team.ids)],
            }
        )
        cls.open = cls.env["helpdesk.ticket.stage"].create(
            {"name": "Requested", "sequence": -10, "team_ids": [(6, 0, cls.team.ids)]}
        )
        cls.partner = cls.env["res.partner"].create(
            {"name": "Customer", "email": "customer@example.invalid"}
        )
        cls.source = cls.env["helpdesk.ticket"].create(
            {
                "name": "Original HT",
                "description": "Previous execution result",
                "partner_id": cls.partner.id,
                "team_id": cls.team.id,
                "stage_id": cls.closed.id,
                "closed_date": fields.Datetime.now(),
            }
        )
        cls.source.message_post(body="Original discussion")
        cls.Wizard = cls.env["helpdesk.environment.change.wizard"].with_user(cls.user)

    def _values(self, **extra):
        values = {
            "source_ticket_id": self.source.id,
            "name": "[Customer] Update Staging",
            "user_id": self.user.id,
            "release_ref": "PR #123 / abcdef",
            "description": "Apply the purchase order popup correction.",
        }
        values.update(extra)
        return values

    def _confirm(self, **extra):
        wizard = self.Wizard.create(self._values(**extra))
        return self.env["helpdesk.ticket"].browse(wizard.action_confirm()["res_id"])

    def test_wizard_starts_from_source_context(self):
        action = self.source.with_user(self.user).action_request_environment_change()
        form = Form(self.Wizard.with_context(**action["context"]))
        self.assertEqual(form.partner_id, self.partner)
        self.assertEqual(form.name, "[Customer] Update environment")
        self.assertEqual(form.user_id, self.user)

    def test_creates_fresh_related_ticket(self):
        wizard = self.Wizard.create(self._values()).with_context(
            default_stage_id=self.closed.id,
            default_closed_date=fields.Datetime.now(),
            default_description="Old result",
        )
        ticket = self.env["helpdesk.ticket"].browse(wizard.action_confirm()["res_id"])
        self.assertNotEqual(ticket.number, self.source.number)
        for name in ("partner_id", "company_id"):
            self.assertEqual(ticket[name], self.source[name])
        self.assertEqual(ticket.partner_name, self.partner.name)
        self.assertEqual(ticket.partner_email, self.partner.email)
        self.assertEqual(ticket.team_id, self.team)
        self.assertEqual(ticket.user_id, self.user)
        self.assertEqual(ticket.stage_id, self.open)
        self.assertFalse(ticket.closed_date)
        self.assertNotIn("Previous execution result", ticket.description)
        self.assertFalse(ticket.message_ids & self.source.message_ids)
        self.assertEqual(ticket.related_ticket_ids, self.source)
        self.assertIn(ticket, self.source.related_ticket_ids)

    def test_production_relates_to_staging_only(self):
        staging = self._confirm()
        production = self._confirm(
            source_ticket_id=staging.id, name="[Customer] Update Production"
        )
        self.assertEqual(staging.related_ticket_ids, self.source | production)
        self.assertEqual(production.related_ticket_ids, staging)
        self.assertNotIn(production, self.source.related_ticket_ids)

    def test_missing_team_blocks_creation(self):
        self.env.company.environment_update_team_id = False
        with self.assertRaises(UserError):
            self._confirm()

    def test_portal_cannot_use_wizard(self):
        portal = new_test_user(
            self.env, login="change_portal", groups="base.group_portal"
        )
        with self.assertRaises(AccessError):
            self.Wizard.with_user(portal).create(self._values())

    def test_description_escapes_input(self):
        ticket = self._confirm(description="<script>alert(1)</script>\nDeploy")
        self.assertIn("&lt;script&gt;", ticket.description)
        # The ticket description is sanitized HTML, so the line break is normalized.
        self.assertIn("<br>", ticket.description)
