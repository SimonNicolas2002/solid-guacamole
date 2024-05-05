from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="hotel/index.html"), name="index"),
    path("alojamiento/", TemplateView.as_view(template_name="hotel/alojamiento.html"), name="alojamiento"),
    path("artist/", TemplateView.as_view(template_name="hotel/artist.html"), name="artist"),
    path("events_reunion/", TemplateView.as_view(template_name="hotel/events_reunion.html"), name="events_reunion"),
    path("form/", TemplateView.as_view(template_name="hotel/form.html"), name="form"),
    path("restaurant/", TemplateView.as_view(template_name="hotel/restaurant.html"), name="restaurant"),
    path("services/", TemplateView.as_view(template_name="hotel/services.html"), name="services"),
    path("spa/", TemplateView.as_view(template_name="hotel/spa.html"), name="spa"),
]