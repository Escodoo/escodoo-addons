# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

SUPPORT_LEVELS = [
    ("none", "Not covered"),
    ("partial", "Partially covered"),
    ("full", "Fully covered"),
]

LEVEL_WEIGHT = {False: 0, "none": 0, "partial": 1, "full": 2}


class EscodooWebsiteFeature(models.Model):
    """Single source for the feature map, the edition comparison and the
    industry pages.

    The public site used to repeat the same markup on three URLs, so the three
    renderings drifted apart. Keeping the assessment on records means the OCA
    module that closes a gap is named once and cited everywhere.
    """

    _name = "escodoo.website.feature"
    _description = "Escodoo Website Feature"
    _order = "category_id, sequence, name"

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    category_id = fields.Many2one(
        comodel_name="escodoo.website.feature.category",
        required=True,
        ondelete="cascade",
    )
    segment_ids = fields.Many2many(
        comodel_name="escodoo.website.feature.segment",
        relation="escodoo_website_feature_segment_rel",
        column1="feature_id",
        column2="segment_id",
    )
    community_level = fields.Selection(
        selection=SUPPORT_LEVELS,
        required=True,
        default="none",
        help="Coverage by Odoo Community on its own, without community modules.",
    )
    oca_level = fields.Selection(
        selection=SUPPORT_LEVELS,
        required=True,
        default="none",
        help="Coverage by Odoo Community combined with the OCA ecosystem.",
    )
    enterprise_level = fields.Selection(
        selection=SUPPORT_LEVELS,
        required=True,
        default="none",
        help="Coverage by Odoo Enterprise.",
    )
    oca_module_names = fields.Char(
        help="Comma separated technical names of the modules that close the gap.",
    )
    oca_repo_url = fields.Char()
    note = fields.Text(
        translate=True,
        help="Caveat shown next to the assessment, such as a required "
        "integration or a partial coverage reason.",
    )
    odoo_version = fields.Char(
        required=True,
        default="18.0",
        help="Odoo version the assessment refers to. A capability matrix "
        "without a version is a liability.",
    )
    closes_gap = fields.Boolean(
        compute="_compute_closes_gap",
        store=True,
        help="Set when the OCA ecosystem improves on plain Community.",
    )
    matches_enterprise = fields.Boolean(
        compute="_compute_closes_gap",
        store=True,
        help="Set when Community plus OCA reaches at least the Enterprise level.",
    )
    active = fields.Boolean(default=True)

    @api.depends("community_level", "oca_level", "enterprise_level")
    def _compute_closes_gap(self):
        for feature in self:
            community = LEVEL_WEIGHT[feature.community_level]
            oca = LEVEL_WEIGHT[feature.oca_level]
            enterprise = LEVEL_WEIGHT[feature.enterprise_level]
            feature.closes_gap = oca > community
            feature.matches_enterprise = oca >= enterprise

    @api.model
    def _get_public_categories(self, segment_xmlid=None):
        """Return the categories that carry published features, in order.

        The website templates iterate categories and read ``feature_ids`` from
        them, so the grouping stays in one place instead of being rebuilt in
        QWeb. ``segment_xmlid`` narrows the set down for an industry page.
        """
        domain = []
        if segment_xmlid:
            segment = self.env.ref(segment_xmlid, raise_if_not_found=False)
            if not segment:
                return self.env["escodoo.website.feature.category"].browse()
            domain = [("segment_ids", "in", segment.id)]
        features = self.sudo().search(domain)
        return features.category_id.sorted(lambda c: (c.sequence, c.name))

    @api.model
    def _get_public_features(self, segment_xmlid=None, category=None):
        """Return published features, optionally narrowed by segment/category."""
        domain = []
        if segment_xmlid:
            segment = self.env.ref(segment_xmlid, raise_if_not_found=False)
            if not segment:
                return self.browse()
            domain.append(("segment_ids", "in", segment.id))
        if category:
            domain.append(("category_id", "=", category.id))
        return self.sudo().search(domain)

    @api.model
    def _get_coverage_chart(self):
        """Coverage score per edition, as a percentage of the maximum.

        The edition diagram draws these values, so the chart on the public page
        is derived from the same assessment the feature map publishes instead of
        being a hard-coded illustration.
        """
        features = self.sudo().search([])
        ceiling = len(features) * max(LEVEL_WEIGHT.values())
        if not ceiling:
            return {"community": 0, "oca": 0, "enterprise": 0, "total": 0}

        def score(field_name):
            weight = sum(LEVEL_WEIGHT[feature[field_name]] for feature in features)
            return round(100 * weight / ceiling)

        return {
            "community": score("community_level"),
            "oca": score("oca_level"),
            "enterprise": score("enterprise_level"),
            "total": len(features),
        }

    @api.model
    def _get_coverage_summary(self):
        """Counters shown above the feature map.

        The live widget serves an empty state, so the totals are computed here
        rather than hard-coded in the page markup.
        """
        features = self.sudo().search([])
        return {
            "total": len(features),
            "closed_by_oca": len(features.filtered("closes_gap")),
            "matching_enterprise": len(features.filtered("matches_enterprise")),
            "categories": len(features.category_id),
        }
