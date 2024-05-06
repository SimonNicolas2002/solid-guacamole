from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ReservationForm
from .models import Room, Reservation
import logging


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/login.html'


logger = logging.getLogger(__name__)


def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            room_id = form.cleaned_data['room'].id
            room = Room.objects.get(pk=room_id)

            reservation = Reservation.objects.create(
                guest=request.user,
                hotel=room.hotel,
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                status='CONFIRMED'
            )
      
            room.occupied = True
            room.save()

            logger.info(f"Reservation made for room {room.room_number}. Room is now occupied.")
            return redirect('services')
        else:
            logger.error("Form is invalid.")
    else:
        form = ReservationForm()

    rooms = Room.objects.filter(occupied=False)
    return render(request, 'hotel/index.html', {'form': form, 'rooms': rooms})