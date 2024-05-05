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


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    success_url = reverse_lazy('index')
    template_name = 'registration/login.html'
