from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Reservation
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('name', 'phone_number', 'nationality', 'gender')

    
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in_date', 'check_out_date', 'room']
