import statuspageio

from django.conf import settings
from django.contrib import admin
from django.db import models

from response.core.models import Incident

class StatusPageError(Exception):
    pass

__statuspage_client = None

def statuspage_client():
    global __statuspage_client
    if __statuspage_client == None:
        if getattr(settings, "STATUSPAGEIO_API_KEY", None) and getattr(
            settings, "STATUSPAGEIO_PAGE_ID", None
        ):
            __statuspage_client = statuspageio.Client(
                api_key=settings.STATUSPAGEIO_API_KEY,
                page_id=settings.STATUSPAGEIO_PAGE_ID,
            )
        else:
            raise ValueError(
                "Statuspage client called but not configured. Check that STATUSPAGEIO_API_KEY and STATUSPAGEIO_PAGE_ID are configured in Django settings."
            )
    return __statuspage_client

class StatusPage(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.PROTECT)
    statuspage_incident_id = models.CharField(max_length=100, unique=True, null=True)

    def update_statuspage(self, **kwargs):
        if self.statuspage_incident_id:
            statuspage_client().incidents.update(
                incident_id=self.statuspage_incident_id, **kwargs
            )
        else:
            response = statuspage_client().incidents.create(**kwargs)
            self.statuspage_incident_id = response["id"]
            self.save()

        if 'component_ids' in kwargs and kwargs['component_ids']:
                if kwargs['status'] == 'resolved':
                    status = 'operational'
                else:
                    status = kwargs['component_status']

                if status:
                    statuspage_client().components.update(
                        component_id=kwargs['component_ids'][0], status=status
                    )

    def get_from_statuspage(self):
        if self.statuspage_incident_id:
            for incident in statuspage_client().incidents.list():
                if incident["id"] == self.statuspage_incident_id:
                    obj = {
                        "name": incident["name"],
                        "status": incident["status"],
                        "message": incident["incident_updates"][0]["body"],
                        "impact_override": incident["impact_override"],
                    }

                    if len(incident["components"]) > 0:
                        obj["component_id"] = incident["components"][0]["id"]
                        obj["component_status"] = incident["components"][0]["status"]

                    return obj
            raise StatusPageError(
                f"Statuspage incident with id {self.statuspage_incident_id} not found"
            )
        return {}

    @staticmethod
    def get_components():
        options = []

        components = statuspage_client().components.list()

        for component in components:
            if component.group:
                continue

            name = component.name

            if component.group_id:
                group_name = [c.name for c in components if c.id == component.group_id][0]
                name = f"{group_name} — {name}"

            options.append( (name, component.id) )

        return sorted(options, key=lambda t: t[0].lower())

@admin.register(StatusPage)
class StatusPageAdmin(admin.ModelAdmin):
    list_display = ("incident_summary", "statuspage_incident_id")

    def incident_summary(self, obj):
        return obj.incident.report


class PagerDutySpecialist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    summary = models.TextField(max_length=1000)
    escalation_policy = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} - {self.escalation_policy}"


@admin.register(PagerDutySpecialist)
class PagerDutySpecialistAdmin(admin.ModelAdmin):
    pass
