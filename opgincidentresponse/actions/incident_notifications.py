from response.core.models import Incident
from response.slack.models import CommsChannel
from response.slack.decorators import recurring_notification, single_notification
from response.slack import incident_notifications

@single_notification()
def incident_response_process(incident: Incident):
    try:
        comms_channel = CommsChannel.objects.get(incident=incident)
        comms_channel.post_in_channel("📗 You can find our Incident Response process here https://ministryofjustice.github.io/opg-technical-guidance/incidents/incident-response-process/#incident-response-process")
    except CommsChannel.DoesNotExist:
        pass

@recurring_notification(interval_mins=30, max_notifications=10)
def take_a_break(incident: Incident):
    try:
        comms_channel = CommsChannel.objects.get(incident=incident)
        comms_channel.post_in_channel("👋 30 minutes have elapsed. Think about taking a few minutes away from the screen.")
    except CommsChannel.DoesNotExist:
        pass