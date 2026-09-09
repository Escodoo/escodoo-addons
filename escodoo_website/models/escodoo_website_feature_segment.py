# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class EscodooWebsiteFeatureSegment(models.Model):
    _name = "escodoo.website.feature.segment"
    _description = "Escodoo Website Feature Segment"
    _order = "sequence, name"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    page_url = fields.Char(
        help="Public page that renders the features tagged with this segment.",
    )
    feature_ids = fields.Many2many(
        comodel_name="escodoo.website.feature",
        relation="escodoo_website_feature_segment_rel",
        column1="segment_id",
        column2="feature_id",
    )
    active = fields.Boolean(default=True)
