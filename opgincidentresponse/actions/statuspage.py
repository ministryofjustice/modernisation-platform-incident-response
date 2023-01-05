import logging
import json
from django.db import models

from response.core.models import Incident
from response.slack import block_kit, dialog_builder
from response.slack.models import CommsChannel
from response.slack.decorators import ActionContext, action_handler, dialog_handler, keyword_handler
from response.slack.decorators.incident_command import incident_command
from datetime import datetime

from opgincidentresponse.models import StatusPage

logger = logging.getLogger(__name__)

OPEN_STATUS_PAGE_DIALOG = "dialog-open-status-page"
STATUS_PAGE_UPDATE = "status-page-update"

@incident_command(
    ["statuspage", "sp"], helptext="Update the statuspage for this incident"
)
def handle_statuspage(incident: Incident, user_id: str, message: str):

    logger.info("Handling statuspage command")
    comms_channel = CommsChannel.objects.get(incident=incident)

    try:
        status_page = StatusPage.objects.get(incident=incident)
        values = status_page.get_from_statuspage()

        if values.get("status") == "resolved":
            comms_channel.post_in_channel(
                "The status page can't be updated after it has been resolved."
            )
            return True, None
    except models.ObjectDoesNotExist:
        logger.info(
            "Existing status page not found. Posting button to create a new one"
        )

    msg = block_kit.Message()
    msg.add_block(
        block_kit.Section(
            block_id="title",
            text=block_kit.Text(f"To update the Statuspage, click below!"),
        )
    )
    msg.add_block(
        block_kit.Actions(
            block_id="actions",
            elements=[
                block_kit.Button(
                    "Update Statuspage", OPEN_STATUS_PAGE_DIALOG, value=incident.pk
                )
            ],
        )
    )

    msg.send(comms_channel.channel_id)
    return True, None


@action_handler(OPEN_STATUS_PAGE_DIALOG)
def handle_open_status_page_dialog(action_context: ActionContext):
    try:
        status_page = StatusPage.objects.get(incident=action_context.incident)
        values = status_page.get_from_statuspage()

        if values.get("status") == "resolved":
            logger.info(
                f"Status Page incident '{values.get('name')}' has been resolved"
            )
            status_page.incident.comms_channel().post_in_channel(
                "The status page can't be updated after it has been resolved."
            )
            return

    except models.ObjectDoesNotExist:
        values = {
            "name": "We're experiencing some issues at the moment",
            "status": "investigating",
            "message": "We're getting all the information we need to fix this and will update the status page as soon as we can.",
            "impact_override": "major",
            "component_id": None,
            "component_status": "operational",
        }

    dialog = dialog_builder.Dialog(
        title="Statuspage Update",
        submit_label="Update",
        state=action_context.incident.pk,
        elements=[
            dialog_builder.Text(
                label="Name",
                name="name",
                value=values.get("name"),
                hint="Make this concise and clear - it's what will show in the apps",
            ),
            dialog_builder.SelectWithOptions(
                [
                    ("Investigating", "investigating"),
                    ("Identified", "identified"),
                    ("Monitoring", "monitoring"),
                    ("Resolved", "resolved"),
                ],
                label="Status",
                name="incident_status",
                value=values.get("status"),
            ),
            dialog_builder.TextArea(
                label="Description",
                name="message",
                optional=True,
                value=values.get("message"),
            ),
            dialog_builder.SelectWithOptions(
                [
                    ("Minor", "minor"),
                    ("Major", "major"),
                    ("Critical", "critical"),
                ],
                label="Severity",
                name="impact_override",
                optional=True,
                value=values.get("impact_override"),
            ),
            dialog_builder.SelectWithOptions(
                StatusPage.get_components(),
                label="Affected component",
                name="component_id",
                optional=True,
                value=values.get("component_id"),
            ),
            dialog_builder.SelectWithOptions(
                [
                    ("Operational", "operational"),
                    ("Under maintenance", "under_maintenance"),
                    ("Degraded performance", "degraded_performance"),
                    ("Partial outage", "partial_outage"),
                    ("Major outage", "major_outage"),
                ],
                label="Component status",
                name="component_status",
                optional=True,
                value=values.get("component_status"),
            ),
        ],
    )

    dialog.send_open_dialog(STATUS_PAGE_UPDATE, action_context.trigger_id)


@dialog_handler(STATUS_PAGE_UPDATE)
def update_status_page(
    user_id: str, channel_id: str, submission: json, response_url: str, state: json
):
    incident_id = state
    incident = Incident.objects.get(pk=incident_id)

    try:
        status_page = StatusPage.objects.get(incident=incident_id)
    except models.ObjectDoesNotExist:
        status_page = StatusPage(incident=incident)
        status_page.save()

    statuspage_incident = {
        "name": submission["name"],
        "status": submission["incident_status"],
        "message": submission["message"] or "",
        "component_status": submission["component_status"],
    }

    if submission["component_id"]:
        statuspage_incident["component_ids"] = [submission["component_id"]]

    if submission["impact_override"]:
        statuspage_incident["impact_override"] = submission["impact_override"]

    status_page.update_statuspage(**statuspage_incident)
