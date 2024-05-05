from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('name', 'phone_number', 'nationality', 'gender')

    
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser