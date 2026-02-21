# Copyright 2025 - Today, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.mail.tests.common import MailCommon, mail_new_test_user
from odoo.addons.sale.tests.common import SaleCommon


@tagged("post_install", "-at_install")
class TestSaleOrderPortalAccess(SaleCommon, MailCommon):
    """Test cases for automatic portal access grant on sale order confirmation."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a partner without portal access
        cls.partner_no_portal = cls.env["res.partner"].create(
            {
                "name": "Partner Without Portal",
                "email": "partner_no_portal@example.com",
            }
        )
        # Create a partner with portal access
        cls.partner_with_portal = cls.env["res.partner"].create(
            {
                "name": "Partner With Portal",
                "email": "partner_with_portal@example.com",
            }
        )
        # Create portal user for partner_with_portal
        cls.portal_user = mail_new_test_user(
            cls.env,
            name="Portal User",
            login="portal_user_test",
            email="partner_with_portal@example.com",
            groups="base.group_portal",
        )
        cls.partner_with_portal.user_ids = [(6, 0, [cls.portal_user.id])]
        # Create a partner without email
        cls.partner_no_email = cls.env["res.partner"].create(
            {
                "name": "Partner Without Email",
                "email": False,
            }
        )
        # Create a commercial partner with child
        cls.commercial_partner = cls.env["res.partner"].create(
            {
                "name": "Commercial Partner",
                "email": "commercial@example.com",
                "is_company": True,
            }
        )
        cls.child_partner = cls.env["res.partner"].create(
            {
                "name": "Child Partner",
                "email": "child@example.com",
                "parent_id": cls.commercial_partner.id,
            }
        )
        # Create a product for sale orders
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
                "list_price": 100.0,
            }
        )

    def test_01_confirm_order_grant_portal_access(self):
        """Test that confirming a sale order grants
        portal access to partner without access."""
        # Create sale order for partner without portal access
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_no_portal.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        # Verify partner has no portal access before confirmation
        portal_users = self.partner_no_portal.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertFalse(
            portal_users, "Partner should not have portal access before confirmation"
        )
        # Confirm order with mail gateway mock
        with self.mock_mail_gateway():
            sale_order.action_confirm()
        # Verify order is confirmed
        self.assertEqual(sale_order.state, "sale", "Sale order should be confirmed")
        # Verify portal access was granted
        self.partner_no_portal.invalidate_recordset()
        portal_users = self.partner_no_portal.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertTrue(
            portal_users, "Partner should have portal access after confirmation"
        )
        # Verify email was sent
        self.assertSentEmail(self.env.user.partner_id, [self.partner_no_portal])

    def test_02_confirm_order_partner_already_has_portal_access(self):
        """Test that confirming a sale order does nothing if partner already
        has portal access."""
        # Create sale order for partner with portal access
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_with_portal.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        # Verify partner has portal access before confirmation
        portal_users = self.partner_with_portal.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertTrue(
            portal_users, "Partner should have portal access before confirmation"
        )
        initial_user_count = len(self.partner_with_portal.user_ids)
        # Confirm order
        with self.mock_mail_gateway():
            sale_order.action_confirm()
        # Verify order is confirmed
        self.assertEqual(sale_order.state, "sale", "Sale order should be confirmed")
        # Verify no new user was created
        self.partner_with_portal.invalidate_recordset()
        self.assertEqual(
            len(self.partner_with_portal.user_ids),
            initial_user_count,
            "No new user should be created if partner already has portal access",
        )
        # Verify no email was sent (since access already exists)
        self.assertNotSentEmail()

    def test_03_confirm_order_partner_without_email(self):
        """Test that confirming a sale order does not grant portal access if
        partner has no email."""
        # Create sale order for partner without email
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_no_email.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        # Verify partner has no portal access before confirmation
        portal_users = self.partner_no_email.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertFalse(
            portal_users, "Partner should not have portal access before confirmation"
        )
        # Confirm order
        with self.mock_mail_gateway():
            sale_order.action_confirm()
        # Verify order is confirmed
        self.assertEqual(sale_order.state, "sale", "Sale order should be confirmed")
        # Verify portal access was NOT granted (no email)
        self.partner_no_email.invalidate_recordset()
        portal_users = self.partner_no_email.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertFalse(
            portal_users, "Partner should not have portal access if no email address"
        )
        # Verify no email was sent
        self.assertNotSentEmail()

    def test_04_confirm_order_commercial_partner_with_child(self):
        """Test that confirming a sale order checks commercial partner and
        children for portal access."""
        # Create sale order for child partner
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.child_partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        # Verify neither commercial partner nor child has portal access
        commercial_portal_users = self.commercial_partner.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        child_portal_users = self.child_partner.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertFalse(
            commercial_portal_users, "Commercial partner should not have portal access"
        )
        self.assertFalse(
            child_portal_users, "Child partner should not have portal access"
        )
        # Confirm order
        with self.mock_mail_gateway():
            sale_order.action_confirm()
        # Verify order is confirmed
        self.assertEqual(sale_order.state, "sale", "Sale order should be confirmed")
        # Verify portal access was granted to child partner
        self.child_partner.invalidate_recordset()
        child_portal_users = self.child_partner.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertTrue(
            child_portal_users,
            "Child partner should have portal access after confirmation",
        )
        # Verify email was sent to child partner
        self.assertSentEmail(self.env.user.partner_id, [self.child_partner])

    def test_05_confirm_order_commercial_partner_has_portal_access(self):
        """Test that if commercial partner has portal access, child partner
        order does not create new access."""
        # Grant portal access to commercial partner
        portal_wizard = self.env["portal.wizard"].create(
            {"partner_ids": [(6, 0, [self.commercial_partner.id])]}
        )
        portal_wizard_user = portal_wizard.user_ids.filtered(
            lambda u: u.partner_id == self.commercial_partner
        )
        portal_wizard_user.email = self.commercial_partner.email
        with self.mock_mail_gateway():
            portal_wizard_user.action_grant_access()
        # Verify commercial partner has portal access
        commercial_portal_users = self.commercial_partner.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertTrue(
            commercial_portal_users, "Commercial partner should have portal access"
        )
        # Create sale order for child partner
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.child_partner.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        initial_child_user_count = len(self.child_partner.user_ids)
        # Confirm order
        with self.mock_mail_gateway():
            sale_order.action_confirm()
        # Verify order is confirmed
        self.assertEqual(sale_order.state, "sale", "Sale order should be confirmed")
        # Verify no new user was created for child
        # (commercial partner already has access)
        self.child_partner.invalidate_recordset()
        self.assertEqual(
            len(self.child_partner.user_ids),
            initial_child_user_count,
            "No new user should be created if commercial partner "
            "already has portal access",
        )
        # Verify no email was sent
        self.assertNotSentEmail()

    def test_06_confirm_multiple_orders_same_partner(self):
        """Test confirming multiple orders for the same partner."""
        # Create two sale orders for the same partner
        sale_order_1 = self.env["sale.order"].create(
            {
                "partner_id": self.partner_no_portal.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        sale_order_2 = self.env["sale.order"].create(
            {
                "partner_id": self.partner_no_portal.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 2.0,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        # Confirm first order
        with self.mock_mail_gateway():
            sale_order_1.action_confirm()
        # Verify portal access was granted
        self.partner_no_portal.invalidate_recordset()
        portal_users_after_first = self.partner_no_portal.mapped("user_ids").filtered(
            lambda u: u.has_group("base.group_portal")
        )
        self.assertTrue(
            portal_users_after_first,
            "Partner should have portal access after first confirmation",
        )
        initial_user_count = len(self.partner_no_portal.user_ids)
        # Confirm second order
        with self.mock_mail_gateway():
            sale_order_2.action_confirm()
        # Verify order is confirmed
        self.assertEqual(
            sale_order_2.state, "sale", "Second sale order should be confirmed"
        )
        # Verify no new user was created (access already exists)
        self.partner_no_portal.invalidate_recordset()
        self.assertEqual(
            len(self.partner_no_portal.user_ids),
            initial_user_count,
            "No new user should be created on second confirmation",
        )
