# Part of e-learning-boardkit. See LICENSE for full copyright.

import io

import qrcode
from PIL import Image

from odoo import http
from odoo.http import request


class CertificationValidation(http.Controller):
    """Public endpoints for QR-coded certificate validation."""

    @http.route(
        [
            "/certificacao/validar/<string:token>",
            "/certificacion/validar/<string:token>",
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def validar_certificado(self, token, **kw):
        user_input = (
            request.env["survey.user_input"]
            .sudo()
            .search(
                [
                    ("access_token", "=", token),
                    ("scoring_success", "=", True),
                ],
                limit=1,
            )
        )

        if not user_input:
            return request.render(
                "e-learning-boardkit.certificado_invalido",
                {
                    "token": token,
                },
            )

        return request.render(
            "e-learning-boardkit.certificado_valido",
            {
                "user_input": user_input,
            },
        )

    @http.route(
        [
            "/certificacao/validar/qr/<string:token>",
            "/certificacion/validar/qr/<string:token>",
        ],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def qr_certificado(self, token, **kw):
        """Gera QR code PNG apontando para a URL pública de validação."""
        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        validate_url = f"{base_url}/certificacao/validar/{token}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(validate_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#714B67", back_color="white").convert("RGB")

        # Resize to clean dimensions
        img = img.resize((260, 260), Image.NEAREST)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        png_bytes = buf.getvalue()

        return request.make_response(
            png_bytes,
            headers=[
                ("Content-Type", "image/png"),
                ("Content-Length", len(png_bytes)),
                ("Cache-Control", "public, max-age=86400"),
            ],
        )
