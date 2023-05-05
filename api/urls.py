from django.urls import path

from . import views

urlpatterns = [
    path("request", views.request),
    path("upload", views.upload),
    path("command", views.command),
    path("reboot", views.reboot),
    path("disabled_resource", views.disabled_resource),
]
