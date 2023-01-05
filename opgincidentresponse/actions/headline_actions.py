import logging
import json
from django.db import models
from datetime import datetime

from response.core.models import Incident
from response.slack import block_kit, dialog_builder
from response.slack.decorators import ActionContext, action_handler, dialog_handler, headline_post_action
from opgincidentresponse.models import PagerDutySpecialist
from opgincidentresponse.actions.pagerduty import page_specialist

logger = logging.getLogger(__name__)

PAGE_LEAD_DIALOG = "page-incident-lead"

@headline_post_action(order=150)
def page_incident_lead_headline_action(headline_post):
    return block_kit.Button("📟 Page Incident Lead", PAGE_LEAD_DIALOG, value=headline_post.incident.pk)

@action_handler(PAGE_LEAD_DIALOG)
def handle_page_incident_lead(context: ActionContext):
    dialog = dialog_builder.Dialog(
        title="Page an Incdent Lead",
        submit_label="Page",
        elements=[
            dialog_builder.Text(
                label="Message",
                name="message",
                placeholder="Why do you need them?",
                hint="You might be waking this person up. Please make this friendly and clear.",
            )
        ],
        state=context.incident.pk,
    )

    dialog.send_open_dialog(PAGE_LEAD_DIALOG, context.trigger_id)

@dialog_handler(PAGE_LEAD_DIALOG)
def page_lead_dialog(
    user_id: str, channel_id: str, submission: json, response_url: str, state: json
):
    logger.debug(f"Handling dialog for `page_lead_dialog`")

    incident_id = state
    incident = Incident.objects.get(pk=incident_id)

    specialist = PagerDutySpecialist.objects.get(name="incident-leads")
    page_specialist(incident, specialist, submission["message"])
