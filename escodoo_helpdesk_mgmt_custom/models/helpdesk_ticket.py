# Copyright 2024 - TODAY, Wesley Oliveira <wesley.oliveira@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HelpdeskTicket(models.Model):

    _inherit = "helpdesk.ticket"

    last_message_from_partner = fields.Datetime(
        string="Last Message From Partner",
        compute="_compute_last_message_from_partner",
        readonly=True,
    )
    last_message_from_user = fields.Datetime(
        string="Last Message From User",
        compute="_compute_last_message_from_user",
        readonly=True,
    )
    team_id = fields.Many2one(tracking=True)
    project_id = fields.Many2one(tracking=True)
    task_id = fields.Many2one(tracking=True)

    @api.depends("website_message_ids")
    def _compute_last_message_from_partner(self):
        for ticket in self:
            ticket.last_message_from_partner = ticket.create_date
            if ticket.partner_id:
                messages_partner = ticket.website_message_ids.filtered(
                    lambda x: x.author_id == ticket.partner_id
                )
                if messages_partner:
                    ticket.last_message_from_partner = messages_partner.sorted(
                        key="date", reverse=True
                    )[0].date

    @api.depends("website_message_ids")
    def _compute_last_message_from_user(self):
        for ticket in self:
            ticket.last_message_from_user = False
            if ticket.user_id:
                messages_user = ticket.website_message_ids.filtered(
                    lambda x: x.author_id == ticket.user_id.partner_id
                )
                if messages_user:
                    ticket.last_message_from_user = messages_user.sorted(
                        key="date", reverse=True
                    )[0].date
