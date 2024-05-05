from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hola Mundo! Estás en Fast hotel, la aplicación definitiva.")