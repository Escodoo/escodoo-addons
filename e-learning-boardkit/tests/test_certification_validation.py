# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase


class TestCertificationValidation(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Survey = cls.env["survey.survey"]
        cls.UserInput = cls.env["survey.user_input"]
        cls.Partner = cls.env["res.partner"]

    def _make_survey(self):
        return self.Survey.create(
            {
                "title": "Test Certification Survey",
                "certification": True,
            }
        )

    def _make_user_input(self, survey, token, success=True):
        return self.UserInput.create(
            {
                "survey_id": survey.id,
                "access_token": token,
                "scoring_success": success,
                "state": "done",
                "partner_id": self.Partner.create({"name": "Tester"}).id,
            }
        )

    def test_validar_certificado_token_invalido(self):
        """Token sem user_input matching deve renderizar template inválido."""
        response = self.url_open("/certificacao/validar/no-such-token")
        self.assertEqual(response.status_code, 200)
        body = response.text
        self.assertIn("token", body.lower())

    def test_validar_certificado_token_valido_pt(self):
        survey = self._make_survey()
        self._make_user_input(survey, "good-token-pt", success=True)
        response = self.url_open("/certificacao/validar/good-token-pt")
        self.assertEqual(response.status_code, 200)
        body = response.text
        self.assertIn("Tester", body)

    def test_validar_certificado_token_valido_es(self):
        """Spanish route must also resolve."""
        survey = self._make_survey()
        self._make_user_input(survey, "good-token-es", success=True)
        response = self.url_open("/certificacion/validar/good-token-es")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tester", response.text)

    def test_validar_certificado_sem_scoring_success(self):
        """Token that exists but is not scoring_success must render invalid."""
        survey = self._make_survey()
        self._make_user_input(survey, "failed-token", success=False)
        response = self.url_open("/certificacao/validar/failed-token")
        self.assertEqual(response.status_code, 200)
        body = response.text
        self.assertIn("failed-token", body)

    def test_qr_certificado_retorna_png_pt(self):
        response = self.url_open("/certificacao/validar/qr/any-token")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "image/png")
        # PNG magic bytes: 89 50 4E 47
        self.assertEqual(response.content[:4], b"\x89PNG")

    def test_qr_certificado_retorna_png_es(self):
        response = self.url_open("/certificacion/validar/qr/any-token-es")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("Content-Type"), "image/png")
        self.assertEqual(response.content[:4], b"\x89PNG")

    def test_qr_certificado_tem_cache_control(self):
        response = self.url_open("/certificacao/validar/qr/cache-test")
        cache = response.headers.get("Cache-Control", "")
        self.assertIn("max-age", cache)
