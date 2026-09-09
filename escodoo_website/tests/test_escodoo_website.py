# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re

from odoo.tests import HttpCase, TransactionCase, tagged

FORM_MARKER = 'data-model_name="crm.lead"'
TOKEN_MARKER = 'csrf_token: "'
HIDDEN_INPUT_RE = re.compile(
    r'<input[^>]*type="hidden"[^>]*name="(?P<name>[^"]+)"[^>]*value="(?P<value>[^"]*)"'
)

# Every route the module claims. Kept as a literal list rather than read back
# from website.page so a page silently dropped from the data files fails here.
PUBLIC_URLS = [
    "/",
    # Solutions
    "/implantacao-odoo",
    "/resgate-de-projeto-odoo",
    "/migracao-de-versao-odoo",
    "/migrar-para-odoo",
    "/padronizacao-odoo",
    "/reforma-tributaria-odoo",
    # Services
    "/consultoria-e-desenvolvimento",
    "/manutencao-odoo",
    "/hospedagem-odoo",
    "/arquitetura-de-processos",
    "/segunda-opiniao",
    "/academia",
    # Industries
    "/odoo-erp-para-manufatura",
    "/odoo-erp-para-comercio-e-distribuicao",
    "/odoo-erp-para-prestacao-de-servicos",
    "/odoo-erp-para-servico-de-campo",
    "/odoo-erp-para-manutencao",
    "/odoo-erp-para-assistencia-tecnica",
    "/odoo-erp-para-gestao-de-projetos",
    # Community + OCA
    "/edicoes-odoo",
    "/oca",
    "/mapa-de-funcionalidades",
    "/investimento",
    "/soberania-e-portabilidade",
    "/odoo",
    "/odoo-brasil",
    "/freelancer-odoo-ou-empresa-especializada",
    # Company
    "/aboutus",
    "/cases",
    "/cases/industria-metalmecanica",
    "/cases/distribuidora",
    "/cases/servicos-tecnicos",
    "/internacional",
    "/faq",
    # Conversion
    "/contactus",
    "/diagnostico-gratuito",
    "/solicitacao-de-orcamento",
    "/solicitacao-de-consultoria-e-desenvolvimento",
    "/solicitacao-de-contrato-de-manutencao",
    "/solicitacao-de-migracao-e-hospedagem",
    "/solicitacao-de-demonstracao",
    "/acesso-ao-ambiente-de-demonstracao",
    "/obrigado",
    "/contactus-thank-you",
    "/mapa-de-funcionalidades/obrigado",
]

REDIRECTS = {
    "/servicos-de-infraestrutura-e-sustentacao": "/hospedagem-odoo",
    "/sua-jornada-odoo": "/segunda-opiniao",
    "/ebook-thank-you": "/obrigado",
}


class EscodooWebsiteHttpCase(HttpCase):
    """Shared setup for the frontend cases.

    Two things have to be arranged before a request can be compared to
    anything. The anonymous session binds the request to the test database,
    which is otherwise only resolved when the server hosts a single one. And
    the session language has to be the site language, because a request with
    no language prefix is redirected to the prefix of the session language,
    which would make the Portuguese assertions run against English pages.
    """

    def setUp(self):
        super().setUp()
        self.authenticate(None, None, session_extra={"context": {"lang": "pt_BR"}})
        self.en_prefix = (
            self.env["res.lang"].search([("code", "=", "en_US")], limit=1).url_code
        )

    def en(self, url):
        """Return the English URL for a site path."""
        return f"/{self.en_prefix}" if url == "/" else f"/{self.en_prefix}{url}"


@tagged("post_install", "-at_install")
class TestEscodooWebsiteRoutes(EscodooWebsiteHttpCase):
    def test_public_pages_render(self):
        """Every published route answers 200 to an anonymous visitor.

        Renders in English so a missing translation does not mask a broken
        template.
        """
        for url in PUBLIC_URLS:
            with self.subTest(url=url):
                response = self.url_open(self.en(url), timeout=60)
                self.assertEqual(
                    response.status_code,
                    200,
                    f"{url} answered {response.status_code}",
                )

    def test_public_pages_render_in_portuguese(self):
        """The site is served in Portuguese, so the default locale is covered."""
        for url in PUBLIC_URLS:
            with self.subTest(url=url):
                response = self.url_open(url, timeout=60)
                self.assertEqual(response.status_code, 200)

    def test_portuguese_is_actually_translated(self):
        """The PO file has to reach the visitor, not merely exist in the addon.

        The site is served in Portuguese, so a translation that fails to load is
        not a cosmetic problem: every reader gets the English source copy.
        """
        body = self.url_open("/", timeout=60).text
        self.assertIn("O Odoo que você controla", body)
        self.assertIn("Falar com especialista", body)

    def test_redirects(self):
        """The consolidated URLs keep their accumulated authority."""
        for source, target in REDIRECTS.items():
            with self.subTest(url=source):
                response = self.url_open(source, timeout=60)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(
                    response.url.endswith(target),
                    f"{source} landed on {response.url} instead of {target}",
                )

    def test_feature_map_pdf(self):
        """The gated PDF is what the feature map exchanges for a contact."""
        response = self.url_open("/mapa-de-funcionalidades/pdf", timeout=120)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/pdf")

    def test_home_carries_the_positioning(self):
        """The thesis, the proof and the verifiable source are all on the home.

        Any one of them silently disappearing costs the whole differentiation,
        and the live site lost the ranking block exactly that way.
        """
        body = self.url_open(self.en("/"), timeout=60).text
        self.assertIn("oe_structure_escodoo_home", body)
        self.assertIn("escodoo-seal", body)
        self.assertIn("OCA-contributors/monthly-statistics", body)

    def test_newsletter_block_matches_the_widget(self):
        """The subscribe block ships every hook the Odoo widget dereferences.

        ``publicWidget.registry.subscribe`` reads these elements without
        guarding against a missing one, so a block written against an older
        snippet shape raises on page load and takes the rest of the frontend
        JavaScript down with it. The list id is asserted as a number because a
        placeholder left in the arch would still render a working page while
        every subscription silently failed.
        """
        body = self.url_open(self.en("/"), timeout=60).text
        for hook in (
            "js_subscribe",
            "js_subscribe_wrap",
            "js_subscribed_wrap",
            "js_subscribe_btn",
            "js_subscribe_value",
        ):
            self.assertIn(hook, body, f"the subscribe widget needs .{hook}")
        newsletter = self.env.ref("escodoo_website.mailing_list_newsletter")
        self.assertIn(f'data-list-id="{newsletter.id}"', body)

    def test_contactus_was_replaced(self):
        """The core contact view carries our arch, not the stock form."""
        body = self.url_open(self.en("/contactus"), timeout=60).text
        self.assertIn("oe_structure_escodoo_contactus", body)
        self.assertIn("escodoo-trust", body)


@tagged("post_install", "-at_install")
class TestEscodooWebsiteForms(EscodooWebsiteHttpCase):
    def _submit(self, url, values):
        """Post a form the way the website form snippet does.

        Two details are copied from the browser's behaviour. The snippet renders
        no token input of its own, so the token comes from what the layout
        exposes to JavaScript, otherwise the request is rejected as a forgery.
        And the routing values are hidden inputs resolved when the page renders,
        so they are read back from the page instead of being restated here —
        which is what makes this test able to fail when the routing breaks.
        """
        page = self.url_open(url, timeout=60)
        self.assertEqual(page.status_code, 200)
        self.assertIn(FORM_MARKER, page.text, f"{url} rendered no lead form")
        form = page.text.split(FORM_MARKER, 1)[1].split("</form>", 1)[0]
        payload = {
            match["name"]: match["value"] for match in HIDDEN_INPUT_RE.finditer(form)
        }
        payload.update(values)
        payload["csrf_token"] = page.text.split(TOKEN_MARKER, 1)[1].split('"', 1)[0]
        return self.url_open("/website/form/crm.lead", data=payload, timeout=60)

    def test_diagnostic_form_creates_a_routed_lead(self):
        leads_before = self.env["crm.lead"].search([])
        response = self._submit(
            "/diagnostico-gratuito",
            {
                "contact_name": "Ana Souza",
                "email_from": "ana@example.com",
                "partner_name": "Example Industria",
                "Current situation": "Our Odoo project stalled",
                "name": "Free diagnostic",
                "description": "We went live and stock is wrong.",
            },
        )
        self.assertEqual(response.status_code, 200)
        lead = self.env["crm.lead"].search([]) - leads_before
        self.assertEqual(len(lead), 1)
        self.assertEqual(lead.email_from, "ana@example.com")
        source = self.env.ref("escodoo_website.utm_source_diagnostic")
        self.assertEqual(
            lead.source_id,
            source,
            "the lead does not say which page produced it",
        )
        self.assertTrue(lead.team_id, "the lead landed without a sales team")
        self.assertIn("Our Odoo project stalled", lead.description or "")

    def test_demo_access_form_is_short(self):
        """Five fields. The live page asks for twelve, including revenue."""
        body = self.url_open(
            self.en("/acesso-ao-ambiente-de-demonstracao"), timeout=60
        ).text
        self.assertNotIn("Annual revenue", body)
        self.assertNotIn(
            'name="description"', body.split("escodoo_demo_access_form")[1]
        )


@tagged("post_install", "-at_install")
class TestEscodooWebsiteFeatures(TransactionCase):
    def setUp(self):
        super().setUp()
        self.Feature = self.env["escodoo.website.feature"]

    def test_data_is_loaded_and_versioned(self):
        features = self.Feature.search([])
        self.assertGreater(
            len(features), 100, "the feature map is the site's strongest asset"
        )
        self.assertFalse(
            features.filtered(lambda f: not f.odoo_version),
            "a capability matrix without a version is a liability",
        )

    def test_named_modules_back_the_claims(self):
        """Every claim of full coverage through the ecosystem names its modules.

        This is the difference between our comparison and the ones that assert
        coverage without evidence. Rows that only reach partial coverage are
        allowed to explain themselves in the note instead, because there the
        coverage comes from configuration or from a per-client integration
        rather than from a module a reader could go and install.
        """
        closing = self.Feature.search([("closes_gap", "=", True)])
        self.assertTrue(closing)
        unnamed = closing.filtered(
            lambda f: f.oca_level == "full" and not f.oca_module_names
        )
        self.assertFalse(
            unnamed,
            f"full coverage claimed with no module named: {unnamed.mapped('name')}",
        )
        unevidenced = closing.filtered(lambda f: not f.oca_module_names and not f.note)
        self.assertFalse(
            unevidenced,
            f"improvement claimed with no evidence: {unevidenced.mapped('name')}",
        )

    def test_comparison_is_honest_about_enterprise(self):
        """Some rows must go to Enterprise, or the table is marketing.

        Community plus OCA winning every row would be the same dishonesty as
        the comparisons that leave the ecosystem out of the table.
        """
        losing = self.Feature.search([("matches_enterprise", "=", False)])
        self.assertTrue(
            losing, "no row where Enterprise wins means the assessment is not credible"
        )

    def test_coverage_chart_is_derived_from_the_data(self):
        chart = self.Feature._get_coverage_chart()
        self.assertGreater(chart["total"], 0)
        self.assertGreaterEqual(chart["oca"], chart["community"])
        for edition in ("community", "oca", "enterprise"):
            self.assertLessEqual(chart[edition], 100)

    def test_every_segment_page_has_features(self):
        """An industry page with an empty feature block is worse than none."""
        segments = self.env["escodoo.website.feature.segment"].search([])
        self.assertTrue(segments)
        for segment in segments:
            with self.subTest(segment=segment.name):
                self.assertTrue(
                    self.Feature.search([("segment_ids", "in", segment.id)]),
                    f"{segment.name} has no features attached",
                )

    def test_public_user_can_read_the_features(self):
        public = self.env.ref("base.public_user")
        features = self.Feature.with_user(public).search([], limit=5)
        self.assertTrue(features)
        self.assertTrue(features[0].name)
