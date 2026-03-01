# Copyright 2024 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Escodoo Website Slides Custom",
    "summary": """
        Escodoo Website Slides Custom""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Escodoo",
    "website": "https://github.com/Escodoo/escodoo-addons",
    "depends": ["website_slides"],
    "data": [
        "views/website_slides_templates_homepage.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "escodoo_website_slides_custom/static/src/scss/website_slides.scss",
        ],
    },
}
