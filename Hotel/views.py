from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ReservationForm, AnonymousReservationForm
from .models import CustomUser, Room, Reservation, AbstractUser
import logging
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from django.http import HttpResponseNotFound
from django.template import TemplateDoesNotExist
from django.core.paginator import Paginator


def logout_view(request):
    logout(request)
    return redirect('login')


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/login.html'


logger = logging.getLogger(__name__)


from django.contrib.auth.decorators import login_required


def make_reservation(request):
    try:
        if request.method == 'POST':
            form = ReservationForm(request.POST)
            if form.is_valid():
                check_in_date = form.cleaned_data['check_in_date']
                check_out_date = form.cleaned_data['check_out_date']
                room_id = form.cleaned_data['room'].id
                room = Room.objects.get(pk=room_id)

                if room.occupied:
                    messages.error(request, 'Room is already occupied.')
                    return redirect('index')

                if isinstance(request.user, AnonymousUser) or not request.user.is_authenticated:
                    return redirect('login')
                
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
    except PermissionDenied:
        return redirect('login')


def make_anonymous_reservation(request):
    if request.method == 'POST':
        form = AnonymousReservationForm(request.POST)
        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            room_id = form.cleaned_data['room'].id
            room = Room.objects.get(pk=room_id)

            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')

            guest = None

            reservation = Reservation.objects.create(
                guest=guest,
                name=name,
                surname=surname,
                hotel=room.hotel,
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                status='CONFIRMED'
            )

            room.occupied = True
            room.save()

            logger.info(f"Reservation made for room {room.room_number}. Room is now occupied.")
            return redirect('reservation_success')  # Redirect to the reservation success page
        else:
            logger.error("Form is invalid.")
    else:
        form = AnonymousReservationForm()

    rooms = Room.objects.filter(occupied=False)
    return render(request, 'hotel/anon_reservation.html', {'form': form, 'rooms': rooms})


@login_required
def reservas(request):
    current_reservations = Reservation.objects.filter(guest=request.user, status__in=['PENDING', 'CONFIRMED'])
    reservation_history = Reservation.objects.filter(guest=request.user, status__in=['CANCELLED', 'COMPLETED'])
    return render(request, 'hotel/reservas.html', {'current_reservations': current_reservations, 'reservation_history': reservation_history})


def booking_step(request):
    try:
        if request.method == 'POST':
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            adults = request.POST.get('adults')
            children = request.POST.get('children')
            form_source = request.POST.get('form_source')

            if check_in_date and check_out_date:
                if check_in_date > check_out_date:
                    error_message = 'La fecha de check-in no puede ser posterior a la fecha de check-out.'
                    template = 'hotel/index.html' if form_source == 'index' else 'hotel/bookingstep.html'
                    return render(request, template, {
                        'error_message': error_message,
                        'check_in_date': check_in_date,
                        'check_out_date': check_out_date,
                        'adults': adults,
                        'children': children
                    })

            available_rooms = Room.objects.filter(
                adults=adults,
                children=children,
                occupied=False
            )

            categories = set(room.category for room in available_rooms)

            return render(request, 'hotel/bookingstep.html', {
                'available_rooms': available_rooms,
                'check_in_date': check_in_date,
                'check_out_date': check_out_date,
                'adults': adults,
                'children': children,
                'categories': categories
            })
        else:
            return render(request, 'hotel/bookingform.html')
    except TemplateDoesNotExist:
        return render(request, 'hotel/bookingstep.html')


def payment(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    context = {
        'room_number': room.room_number,
        'image': room.image.url if room.image else None,
        'category': room.category,
        'state': room.state,
        'rent': room.rent,
        'adults': room.adults,
        'children': room.children,
        'occupied': room.occupied,
        'discapacity': room.discapacity,
        'wifi': room.wifi,
        'television': room.television,
        'phone': room.phone,
        'description': room.description,
        'hotel': room.hotel,
        'num_toilets': room.num_toilets,
        'num_beds': room.num_beds
    }

    return render(request, 'hotel/payment.html', context)
