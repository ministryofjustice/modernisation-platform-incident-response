import logging
import json
from django.db import models
from datetime import datetime

from response.core.models import Incident
from response.slack.models import CommsChannel
from response.slack import block_kit, dialog_builder
from response.slack.decorators.incident_command import incident_command, get_help
from response.slack.decorators import ActionContext, action_handler, dialog_handler, headline_post_action
from response.slack.client import SlackError, SlackClient
from opgincidentresponse.models import PagerDutySpecialist
from opgincidentresponse.actions.pagerduty import page_specialist


ESCALATE_BUTTON = "escalate-button-id"
PAGE_SPECIALIST_DIALOG = "dialog-page-specialist"

@incident_command(["escalate", "esc", "page"], helptext="Page another team!")
def handle_escalation(incident: Incident, user_id: str, message: str):

    msg = block_kit.Message()
    specialists = PagerDutySpecialist.objects.all().order_by("name")

    if not specialists:
        msg.add_block(
            block_kit.Section(
                text=block_kit.Text("No teams have been configured 😢")
            )
        )
    else:
        msg.add_block(
            block_kit.Section(
                text=block_kit.Text("Let's find the right team to help out 🔍")
            )
        )
        msg.add_block(block_kit.Divider())
        msg.add_block(
            block_kit.Section(
                text=block_kit.Text(
                    "These are the teams available as escalations:"
                )
            )
        )

        for team in specialists:
            team_section = block_kit.Section(
                text=block_kit.Text(f"*{team.name}*\n{team.summary}"),
                accessory=block_kit.Button(
                    f"📟 Page {team.name}", ESCALATE_BUTTON, value=f"{team.name}"
                ),
            )
            msg.add_block(team_section)

        msg.add_block(block_kit.Divider())
        msg.add_block(
            block_kit.Section(
                text=block_kit.Text(
                    "Not sure who to pick? Ask the Incident Lead for help!"
                )
            )
        )

    comms_channel = CommsChannel.objects.get(incident=incident)
    msg.send(comms_channel.channel_id)
    return True, None

@action_handler(ESCALATE_BUTTON)
def handle_page_teams(context: ActionContext):
    dialog = dialog_builder.Dialog(
        title="Escalate to anoter team",
        submit_label="Escalate",
        elements=[
            dialog_builder.Text(
                label="Message",
                name="message",
                placeholder="Why do you need them?",
                hint="You might be waking this person up. Please make this friendly and clear.",
            )
        ],
        state=context.value,
    )

    dialog.send_open_dialog(PAGE_SPECIALIST_DIALOG, context.trigger_id)


@dialog_handler(PAGE_SPECIALIST_DIALOG)
def page_specialist_dialog(
    user_id: str, channel_id: str, submission: json, response_url: str, state: json
):
    logger.debug(f"Handling dialog for `page_specialist_dialog`")

    comms_channel = CommsChannel.objects.get(channel_id=channel_id)
    specialist = PagerDutySpecialist.objects.get(name=state)
    page_specialist(comms_channel.incident, specialist, submission["message"])
