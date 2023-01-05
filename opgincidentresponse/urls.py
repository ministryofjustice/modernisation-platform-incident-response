from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.conf.urls import url

from decorator_include import decorator_include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("incident/<int:incident_id>/", views.incident, name="incident_doc"),
    url("", include('social_django.urls', namespace='social')),
    path("admin/", admin.site.urls),
    url(r'^ht/', include('health_check.urls')),
    path("slack/", include("response.slack.urls")),
    path("core/", decorator_include(login_required, "response.core.urls")),
]
