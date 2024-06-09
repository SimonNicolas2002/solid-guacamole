from django.urls import path
from django.views.generic import TemplateView
from .views import SignUp, CustomLoginView
from . import views
from .views import make_reservation, logout_view, reservas, booking_step, payment, cancel_reservation


urlpatterns = [
    path("", make_reservation, name="index"),
    path("reservaitons/", reservas, name="reservations"),
    path('card_payment/', TemplateView.as_view(template_name="hotel/card_payment.html"), name='card_payment'),
    path("alojamiento/", TemplateView.as_view(template_name="hotel/alojamiento.html"), name="alojamiento"),
    path('cancel-reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
    path("artist/", TemplateView.as_view(template_name="hotel/artist.html"), name="artist"),
    path("events_reunion/", TemplateView.as_view(template_name="hotel/events_reunion.html"), name="events_reunion"),
    path("form/", TemplateView.as_view(template_name="hotel/form.html"), name="form"),
    path("restaurant/", TemplateView.as_view(template_name="hotel/restaurant.html"), name="restaurant"),
    path("services/", TemplateView.as_view(template_name="hotel/services.html"), name="services"),
    path("spa/", TemplateView.as_view(template_name="hotel/spa.html"), name="spa"),
    path('bookingstep/', views.booking_step, name='booking_step'),
    path('payment/<int:room_id>/', payment, name='payment'),
    path('signup/', SignUp.as_view(template_name="registration/signup.html"), name='signup'),
    path('login/', CustomLoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/', logout_view, name='logout'),
]