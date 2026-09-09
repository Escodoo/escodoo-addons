# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EscodooWebsiteFeatureCategory(models.Model):
    _name = "escodoo.website.feature.category"
    _description = "Escodoo Website Feature Category"
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    feature_ids = fields.One2many(
        comodel_name="escodoo.website.feature",
        inverse_name="category_id",
    )
    feature_count = fields.Integer(compute="_compute_feature_count")
    active = fields.Boolean(default=True)

    def _compute_feature_count(self):
        counts = dict(
            self.env["escodoo.website.feature"]._read_group(
                domain=[("category_id", "in", self.ids)],
                groupby=["category_id"],
                aggregates=["__count"],
            )
        )
        for category in self:
            feature_count = counts.get(category, 0)
            category.feature_count = feature_count
