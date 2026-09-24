# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestDummy(TransactionCase):
    def test_dummy(self):
        self.assertEqual(1, 1)
