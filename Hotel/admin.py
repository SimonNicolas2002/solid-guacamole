from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser, Hotel, Reservation, Room

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Hotel)
admin.site.register(Reservation)


class RoomAdmin(admin.ModelAdmin):

    list_display = ('room_number', 'category', 'rent', 'occupied', 'hotel', 'description')
    
    list_editable = ('rent', 'occupied')
    
    list_filter = ('category', 'hotel')
    
    search_fields = ('room_number', 'category', 'description')
    
    fields = ('room_number', 'category', 'rent', 'occupied', 'hotel')
    
    readonly_fields = ('description',)


admin.site.register(Room, RoomAdmin)