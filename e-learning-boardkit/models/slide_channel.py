from odoo import models


class SlideChannel(models.Model):
    _inherit = "slide.channel"

    # Native Odoo gamification is used as-is:
    # - karma_gen_channel_finish: reward for completing the channel
    # - karma_gen_slide_vote, karma_review, karma_slide_comment: thresholds
    # - quiz_first_attempt_reward on slide: karma per quiz completed
    #
    # No custom XP gate is added — channel completion uses native Odoo flow.
