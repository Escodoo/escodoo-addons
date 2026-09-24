# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSlideChannelInherit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Channel = cls.env["slide.channel"]

    def test_inherit_model_loaded(self):
        """The _inherit = 'slide.channel' extension must be loaded."""
        # If the model extension wasn't loaded, the Channel singleton wouldn't
        # expose our subclass fields/methods. We assert the model class is ours.
        self.assertIn(
            "e-learning-boardkit",
            str(self.Channel._module or ""),
            msg="slide.channel must be present (inherited by the module)",
        )

    def test_create_minimal_channel(self):
        """We can create a slide.channel with the inherited model."""
        channel = self.Channel.create(
            {
                "name": "Test Channel eLearning",
                "channel_type": "training",
            }
        )
        self.assertEqual(channel.name, "Test Channel eLearning")
        self.assertTrue(channel.channel_type == "training")
