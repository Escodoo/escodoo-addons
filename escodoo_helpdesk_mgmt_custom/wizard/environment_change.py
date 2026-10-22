# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from markupsafe import Markup

from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


class EnvironmentChangeWizard(models.TransientModel):
    _name = "helpdesk.environment.change.wizard"
    _description = "Request environment update"

    source_ticket_id = fields.Many2one(
        "helpdesk.ticket", string="Source ticket", required=True, readonly=True
    )
    name = fields.Char(string="Title", required=True)
    partner_id = fields.Many2one(
        related="source_ticket_id.partner_id", string="Contact"
    )
    team_id = fields.Many2one(
        related="source_ticket_id.company_id.environment_update_team_id", string="Team"
    )
    team_user_ids = fields.Many2many(related="team_id.user_ids")
    user_id = fields.Many2one("res.users", string="Responsible", required=True)
    release_ref = fields.Char(string="PR / version or commit", required=True)
    description = fields.Text(
        required=True,
        help="Briefly describe what Infrastructure should update. "
        "The customer's original problem remains in the source ticket.",
    )

    @api.model
    def default_get(self, field_names):
        values = super().default_get(field_names)
        source = self.env["helpdesk.ticket"].browse(
            values.get("source_ticket_id")
            or self.env.context.get("default_source_ticket_id")
        )
        if not source:
            return values
        if "name" in field_names and not values.get("name"):
            customer = source.commercial_partner_id.name or source.partner_name
            title = _("Update environment")
            values["name"] = f"[{customer}] {title}" if customer else title
        if "user_id" in field_names and not values.get("user_id"):
            team = source.company_id.environment_update_team_id
            responsible = team.user_id or self.env.user
            values["user_id"] = (
                responsible.id if responsible in team.user_ids else False
            )
        return values

    def _prepare_description(self):
        body = (Markup("%s") % self.description).replace("\n", Markup("<br/>"))
        return Markup("<h2>%s</h2><p><strong>%s:</strong> %s</p><p>%s</p>") % (
            _("Environment change request"),
            _("PR / version or commit"),
            self.release_ref,
            body,
        )

    def action_confirm(self):
        self.ensure_one()
        source = self.source_ticket_id
        team = self.team_id
        if not team or not team.active:
            raise UserError(
                _("Configure an active environment update team in Helpdesk settings.")
            )
        stage = team._get_applicable_stages().filtered(lambda s: not s.closed)[:1]
        if not stage:
            raise UserError(_("The configured team must have an open stage."))
        # A new ticket, never a copy: drop the defaults carried by the source
        # form, which would otherwise bring stage and closed date along.
        context = {
            k: v for k, v in self.env.context.items() if not k.startswith("default_")
        }
        # pylint: disable=context-overridden
        tickets = self.env["helpdesk.ticket"].with_context(context)
        ticket = tickets.create(
            {
                "name": self.name,
                "description": self._prepare_description(),
                "company_id": source.company_id.id,
                "partner_id": source.partner_id.id,
                "partner_name": source.partner_name,
                "partner_email": source.partner_email,
                "team_id": team.id,
                "user_id": self.user_id.id,
                "stage_id": stage.id,
            }
        )
        # OCA synchronizes the reverse relationship on write(), not on create().
        ticket.write({"related_ticket_ids": [Command.link(source.id)]})
        return ticket.open_ticket()
