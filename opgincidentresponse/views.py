from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest
from django.shortcuts import render

from response.core.models import Action, Incident
from response.slack.models import PinnedMessage, UserStats

def bypassable_login_required(func):
    if settings.RESPONSE_LOGIN_REQUIRED:
        return login_required(func)
    else:
        return func

@bypassable_login_required
def home(request: HttpRequest):
    incidents = Incident.objects.all().order_by('-end_time')
    return render(request, template_name="index.html", context={"incidents": incidents})

@bypassable_login_required
def incident(request: HttpRequest, incident_id: str):
    try:
        incident = Incident.objects.get(pk=incident_id)
    except Incident.DoesNotExist:
        raise Http404("Incident does not exist")

    events = PinnedMessage.objects.filter(incident=incident).order_by("timestamp")
    actions = Action.objects.filter(incident=incident).order_by("created_date")
    user_stats = UserStats.objects.filter(incident=incident).order_by("-message_count")[
        :5
    ]
    return render(
        request,
        template_name="incident.html",
        context={
            "incident": incident,
            "events": events,
            "actions": actions,
            "user_stats": user_stats,
        },
    )
