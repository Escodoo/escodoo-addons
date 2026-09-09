# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
import re

_logger = logging.getLogger(__name__)

COMPANY_VALUES = {
    "email": "contato@escodoo.com.br",
    "phone": "+55 16 98872-7010",
    "city": "Ribeirão Preto",
    "state_id": None,
    "website": "https://escodoo.com.br",
}

# The public site is served in Portuguese; English stays the source language of
# every string so the code keeps a single translatable origin.
SITE_DEFAULT_LANG = "pt_BR"
SITE_SOURCE_LANG = "en_US"

MENU_NAMES = {
    "/": ("Home", "Início"),
    "/contactus": ("Talk to a specialist", "Falar com especialista"),
}

# The shipped header and footer variants hard-code sample contact details, so
# patching the shipped arch is the only way to brand them.
BRANDED_VIEWS = (
    "website.footer_custom",
    "website.footer_copyright_company_name",
)

BRANDING_REPLACEMENTS = (
    ("info@yourcompany.example.com", "contato@escodoo.com.br"),
    ("Company name</span>", "Escodoo</span>"),
    ("+1 555-555-5556", "+55 16 98872-7010"),
    ('<a href="#">About us</a>', '<a href="/aboutus">About Escodoo</a>'),
    ('<a href="#">Products</a>', '<a href="/edicoes-odoo">Community + OCA</a>'),
    ('<a href="#">Services</a>', '<a href="/implantacao-odoo">Services</a>'),
    ('<a href="#">Legal</a>', '<a href="/soberania-e-portabilidade">Sovereignty</a>'),
    ('<a href="/extra">Extra Page</a>', '<a href="/faq">FAQ</a>'),
    ('<a href="/extra">Extra page</a>', '<a href="/faq">FAQ</a>'),
    # The shipped social row ends with a home icon pointing at the sample extra
    # page, so the label, the destination and the icon are corrected together.
    (
        '<a href="/" class="text-800" aria-label="Extra page">',
        '<a href="/faq" class="text-800" aria-label="FAQ">',
    ),
    ("fa fa-home rounded-circle", "fa fa-question-circle rounded-circle"),
    (
        "We are a team of passionate people whose goal is to improve everyone's "
        "life through disruptive products. We build great products to solve your "
        "business problems.",
        "Escodoo implements, develops and sustains Odoo Community with the OCA "
        "ecosystem and the Brazilian fiscal localisation. Working with Odoo "
        "since 2015.",
    ),
    (
        "Our products are designed for small to medium size companies willing to "
        "optimize their performance.",
        "The Odoo you control.",
    ),
)

# The strings above land on views the website module owns, so this module's PO
# file cannot reach them and they would ship in English to a Portuguese reader.
# They are translated on the record instead. Matching collapses whitespace and
# drops tags, because the term the framework produces carries the indentation
# and the inline markup of the shipped arch.
BRANDING_TRANSLATIONS = (
    ("About Escodoo", "Sobre a Escodoo"),
    ("Services", "Serviços"),
    ("Sovereignty", "Soberania e portabilidade"),
    (
        "Escodoo implements, develops and sustains Odoo Community with the OCA "
        "ecosystem and the Brazilian fiscal localisation. Working with Odoo "
        "since 2015. The Odoo you control.",
        "A Escodoo implanta, desenvolve e sustenta Odoo Community com o "
        "ecossistema da OCA e a localização fiscal brasileira. Trabalhando com "
        "Odoo desde 2015.<br/><br/>O Odoo que você controla.",
    ),
)

# ERP chrome the corporate site never shows. The default call to action is
# dropped because the layout inherit ships its own two-speed CTA pair, and the
# header text element because it carries the sample phone number of the demo
# company; the real contact details are in the footer and on /contactus.
HIDDEN_HEADER_VIEWS = (
    "website.header_search_box",
    "website.header_call_to_action",
    "website.header_text_element",
    "portal.user_sign_in",
)

# "/" and "/contactus" belong to the website module, which means they cannot be
# claimed by a website.page. The arch is copied onto the shipped views instead.
# The third element is the marker that identifies an already applied copy.
COPIED_VIEWS = (
    ("escodoo_website.homepage", "website.homepage", "oe_structure_escodoo_home"),
    (
        "escodoo_website.contactus",
        "website.contactus",
        "oe_structure_escodoo_contactus",
    ),
    # website ships /contactus-thank-you as a page of its own, so the arch is
    # replaced rather than a second page being registered on the same URL.
    (
        "escodoo_website.contactus_thank_you",
        "website.contactus_thanks",
        "oe_structure_escodoo_contactus_thank_you",
    ),
)


def post_init_hook(env):
    """Serve the public site in Portuguese and align the Escodoo details."""
    _serve_website_languages(env)
    _rename_default_menus(env)
    _brand_header_and_footer(env)
    _hide_erp_chrome(env)
    _hide_extra_page(env)
    apply_copied_views(env)
    # base.main_company is a noupdate record, so its data cannot be set in XML.
    env.company.write({k: v for k, v in COMPANY_VALUES.items() if v is not None})


def apply_copied_views(env):
    """Write the Escodoo home and contact arch onto the views website owns.

    Applied once. A page already carrying our marker is left alone, so an
    editor's changes in the Website Builder survive a module update — the same
    protection ``noupdate="1"`` gives the ``website.page`` records.
    """
    website = env.ref("website.default_website", raise_if_not_found=False)
    if not website:
        return
    website = website.with_context(website_id=website.id)
    for src_xmlid, dest_key, marker in COPIED_VIEWS:
        source = env.ref(src_xmlid, raise_if_not_found=False)
        if source is None:
            continue
        dest = website.viewref(dest_key)
        if marker in dest.arch:
            continue
        dest.write({"arch": source.arch})
    sync_copied_view_translations(env)


def sync_copied_view_translations(env):
    """Copy term translations onto the live home and contact views.

    Those pages replace ``website.homepage`` / ``website.contactus`` on every
    update. Website copy-on-write stores the public arch on a website specific
    view, so the ``escodoo_website`` PO terms would otherwise stay on the source
    records and never reach the visitor.
    """
    portuguese = env["res.lang"].search([("code", "=", SITE_DEFAULT_LANG)], limit=1)
    if not portuguese:
        return
    website = env.ref("website.default_website", raise_if_not_found=False)
    if not website:
        return
    website = website.with_context(website_id=website.id)
    for src_xmlid, dest_key, _marker in COPIED_VIEWS:
        source = env.ref(src_xmlid, raise_if_not_found=False)
        if source is None:
            continue
        dest = website.viewref(dest_key)
        terms, _context = source.get_field_translations(
            "arch_db", langs=[SITE_DEFAULT_LANG]
        )
        mapping = {
            term["source"]: term["value"]
            for term in terms
            if term.get("lang") == SITE_DEFAULT_LANG and term.get("value")
        }
        if mapping:
            dest.update_field_translations("arch_db", {SITE_DEFAULT_LANG: mapping})


def _serve_website_languages(env):
    """Portuguese is the public language; English is the source language."""
    english = env["res.lang"]._activate_lang(SITE_SOURCE_LANG)
    portuguese = env["res.lang"]._activate_lang(SITE_DEFAULT_LANG)
    if not portuguese:
        _logger.warning(
            "Escodoo Website: %s is unavailable, keeping the site locale",
            SITE_DEFAULT_LANG,
        )
        return
    langs = portuguese
    if english:
        langs |= english
    website = env.ref("website.default_website")
    website.write(
        {"language_ids": [(6, 0, langs.ids)], "default_lang_id": portuguese.id}
    )


def _rename_default_menus(env):
    """Keep the inherited menus aligned in both languages."""
    menus = env["website.menu"].search(
        [
            ("website_id", "=", env.ref("website.default_website").id),
            ("url", "in", list(MENU_NAMES)),
        ]
    )
    for menu in menus:
        source, translated = MENU_NAMES[menu.url]
        # The inherited menus carry no escodoo_website xmlid, so the PO terms
        # never bind to them. Write both languages on every registry load.
        menu.with_context(lang=SITE_SOURCE_LANG).name = source
        menu.with_context(lang=SITE_DEFAULT_LANG).name = translated
    contact = menus.filtered(lambda menu: menu.url == "/contactus")
    if contact:
        contact.sequence = 70


def _brand_header_and_footer(env):
    """Replace the sample contact details of the shipped header and footer."""
    website_id = env.ref("website.default_website").id
    website = env["website"].with_context(website_id=website_id)
    for key in BRANDED_VIEWS:
        view = website.viewref(key)
        arch = view.arch
        branded_arch = arch
        for sample, branded in BRANDING_REPLACEMENTS:
            branded_arch = branded_arch.replace(sample, branded)
        if branded_arch != arch:
            view.write({"arch": branded_arch})
    # Writing on a shipped view yields a website specific copy, so read again.
    archs = "".join(website.viewref(key).arch for key in BRANDED_VIEWS)
    for sample, branded in BRANDING_REPLACEMENTS:
        if branded not in archs:
            _logger.info(
                "Escodoo Website: sample text not present in the shipped views: %r",
                sample,
            )
    _translate_branded_views(env, website)


def _branding_key(term):
    """Reduce a translatable term to what can be matched reliably."""
    return " ".join(re.sub(r"<[^>]+>", " ", term).split())


def _translate_branded_views(env, website):
    """Write the Portuguese of the strings injected into the shipped views."""
    if not env["res.lang"].search_count([("code", "=", SITE_DEFAULT_LANG)]):
        return
    wanted = {_branding_key(source): value for source, value in BRANDING_TRANSLATIONS}
    for key in BRANDED_VIEWS:
        view = website.viewref(key)
        terms, _context = view.get_field_translations(
            "arch_db", langs=[SITE_DEFAULT_LANG]
        )
        mapping = {}
        for term in terms:
            if term.get("lang") != SITE_DEFAULT_LANG:
                continue
            translation = wanted.get(_branding_key(term["source"]))
            if translation:
                mapping[term["source"]] = translation
        if mapping:
            view.update_field_translations("arch_db", {SITE_DEFAULT_LANG: mapping})


def _hide_extra_page(env):
    """Drop the sample Extra page the Website module ships with."""
    website_id = env.ref("website.default_website").id
    menus = env["website.menu"].search(
        [
            ("website_id", "=", website_id),
            ("name", "ilike", "extra"),
        ]
    )
    if menus:
        menus.write({"is_visible": False})
    pages = env["website.page"].search(
        [
            ("website_id", "=", website_id),
            "|",
            ("name", "ilike", "extra"),
            ("url", "in", ("/extra", "/page/extra")),
        ]
    )
    if pages:
        pages.write({"is_published": False})


def _hide_erp_chrome(env):
    """Drop search, the default call to action and Sign in from the header."""
    website_id = env.ref("website.default_website").id
    website = env["website"].with_context(website_id=website_id)
    for key in HIDDEN_HEADER_VIEWS:
        view = website.viewref(key)
        if view.active:
            view.write({"active": False})
