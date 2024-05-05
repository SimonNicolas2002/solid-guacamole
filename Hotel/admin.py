from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Hotel, Reservation, Room

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Hotel)
admin.site.register(Reservation)
admin.site.register(Room)