from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Reservation
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    surname = forms.CharField(max_length=30)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'document', 'first_name', 'surname', 'phone_number', 'nationality', 'gender')

    
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in_date', 'check_out_date', 'room']


class AnonymousReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in_date', 'check_out_date', 'room', 'name', 'surname']

    name = forms.CharField(required=True)
    surname = forms.CharField(required=True)