from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser, Hotel, Reservation, Room, Metodo_pago

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Hotel)
admin.site.register(Reservation)
admin.site.register(Metodo_pago)
admin.site.register(Room)
