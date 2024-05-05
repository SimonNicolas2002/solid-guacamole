from django.contrib import admin

# Register your models here.
from .models import Guest, Hotel, Reservation, Room

admin.site.register(Guest)
admin.site.register(Hotel)
admin.site.register(Reservation)
admin.site.register(Room)