from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Reservation
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    surname = forms.CharField(max_length=30)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('username', 'email', 'first_name', 'surname', 'document_type','document',  'phone_number', 'nationality', 'gender')

    
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'surname', 'adults', 'children', 'check_in_date', 'check_out_date', 'room', 'hotel', 'payment_method']