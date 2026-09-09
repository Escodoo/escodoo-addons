# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models

from ..hooks import (
    _rename_default_menus,
    apply_copied_views,
    sync_copied_view_translations,
)

LEAD_TEAM_NAME = "Website"

COLOR_PALETTE_SCSS = "/website/static/src/scss/options/colors/user_color_palette.scss"

# Escodoo purple as the primary, a near-black violet for text and headers, and a
# very light tint of the same hue for the alternate section background. The
# custom SCSS reads these through the o-color() helper instead of repeating the
# hex values, so a rebrand only has to change this dictionary.
THEME_COLORS = {
    "o-color-1": "#7963b8",
    "o-color-2": "#2b2340",
    "o-color-3": "#f4f2fa",
    "o-color-4": "#ffffff",
    "o-color-5": "#1b1630",
}


class Website(models.Model):
    _inherit = "website"

    @api.model
    def _register_hook(self):
        super()._register_hook()
        _rename_default_menus(self.env)
        sync_copied_view_translations(self.env)

    @api.model
    def escodoo_apply_theme(self):
        """Entry point for data/website_theme_apply.xml."""
        apply_copied_views(self.env)

    @api.model
    def escodoo_apply_palette(self):
        """Write the brand palette into the website colour customisation.

        The palette is a generated SCSS asset rather than a stored field, so it
        cannot be shipped as a record. Going through the customisation API also
        means the colours reach the snippet options in the Website Builder, and
        an editor can still change them without touching this module.
        """
        website = self.env.ref("website.default_website", raise_if_not_found=False)
        if not website:
            return
        self.env["web_editor.assets"].with_context(
            website_id=website.id
        ).make_scss_customization(COLOR_PALETTE_SCSS, THEME_COLORS)

    @api.model
    def escodoo_lead_defaults(self, source_xmlid=None):
        """Sales team, medium and source the public forms write on the lead.

        Resolved when the page renders rather than substituted into the arch at
        install time, because the forms share one template and each page needs
        its own source. It also means a team renamed in the back office does not
        silently leave new leads unassigned.
        """
        team = (
            self.env["crm.team"].sudo().search([("name", "=", LEAD_TEAM_NAME)], limit=1)
        )
        if not team:
            team = self.env.ref(
                "sales_team.team_sales_department", raise_if_not_found=False
            )
        medium = self.env.ref("utm.utm_medium_website", raise_if_not_found=False)
        source = (
            self.env.ref(source_xmlid, raise_if_not_found=False)
            if source_xmlid
            else None
        )
        return {
            "team_id": team.id if team else "",
            "medium_id": medium.id if medium else "",
            "source_id": source.id if source else "",
        }

    @api.model
    def escodoo_newsletter_list_id(self):
        """Id of the mailing list the subscribe block posts to.

        The list is created by this module, so its id is only known once the
        database exists. The subscribe widget reads it from ``data-list-id`` and
        sends it straight to the subscription route, which means a placeholder
        left in the arch would fail silently for every visitor.
        """
        mailing_list = self.env.ref(
            "escodoo_website.mailing_list_newsletter", raise_if_not_found=False
        )
        return mailing_list.id if mailing_list else 0
