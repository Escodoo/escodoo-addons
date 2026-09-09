# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

REPORT_NAME = "escodoo_website.action_report_feature_map"


class EscodooWebsiteFeatureMap(http.Controller):
    @http.route(
        "/mapa-de-funcionalidades/pdf",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def feature_map_pdf(self, **kwargs):
        """Serve the feature map as a PDF.

        The assessment lives on records rather than on page markup, so the
        download is rendered on demand and never drifts from the public page.
        """
        categories = (
            request.env["escodoo.website.feature.category"]
            .sudo()
            .search([("feature_ids", "!=", False)])
        )
        pdf, _content_type = (
            request.env["ir.actions.report"]
            .sudo()
            ._render_qweb_pdf(REPORT_NAME, res_ids=categories.ids)
        )
        return request.make_response(
            pdf,
            headers=[
                ("Content-Type", "application/pdf"),
                ("Content-Length", len(pdf)),
                (
                    "Content-Disposition",
                    http.content_disposition("escodoo-mapa-de-funcionalidades.pdf"),
                ),
            ],
        )
