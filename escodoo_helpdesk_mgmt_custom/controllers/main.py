import logging

import werkzeug.exceptions

import odoo.http as http

from odoo.addons.helpdesk_mgmt.controllers.main import HelpdeskTicketController

_logger = logging.getLogger(__name__)


class HelpdeskEscodooCustomController(HelpdeskTicketController):
    def _check_access(self):
        user = http.request.env.user
        if user.has_group("helpdesk_mgmt.group_helpdesk_user_own"):
            return True
        return http.request.env.user.has_group(
            "escodoo_helpdesk_mgmt_custom.group_helpdesk_mgmt_portal_create_ticket"
        )

    @http.route("/new/ticket", type="http", auth="user", website=True)
    def create_new_ticket(self, **kw):
        res = super().create_new_ticket(**kw)
        if not self._check_access():
            return werkzeug.exceptions.Forbidden()
        return res

    @http.route("/ticket/close", type="http", auth="user")
    def support_ticket_close(self, **kw):
        res = super().support_ticket_close(**kw)
        if not self._check_access():
            return werkzeug.exceptions.Forbidden()
        return res

    @http.route("/submitted/ticket", type="http", auth="user", website=True, csrf=True)
    def submit_ticket(self, **kw):
        res = super().submit_ticket(**kw)
        if not self._check_access():
            return werkzeug.exceptions.Forbidden()
        return res
