# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "eLearning — Boardkit Course",
    "version": "16.0.1.0.0",
    "summary": """
        Curso completo de eLearning sobre o boardkit (Escodoo Odoo) com
        12 capítulos, conteúdo rich HTML, quiz final, certificação nativa
        via survey e certificado PDF Escodoo Portrait A4 com QR code de
        validação pública.""",
    "author": "Escodoo",
    "license": "AGPL-3",
    "category": "Tools/Training",
    "website": "https://github.com/Escodoo/escodoo-addons",
    "depends": ["website_slides_survey"],
    "data": [
        "data/slide_channel_data.xml",
        "data/survey_certification_data.xml",
        "data/survey_certification_questions.xml",
        "data/slide_slide_data.xml",
        "data/slide_quiz_data.xml",
        "data/slide_question_data.xml",
        "views/slide_channel_views.xml",
        "views/certificate_template.xml",
        "views/certification_validation.xml",
    ],
    "installable": True,
    "application": False,
}
