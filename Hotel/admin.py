from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import CustomUser, Hotel, Reservation, Room

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Hotel)
admin.site.register(Reservation)


class RoomAdmin(admin.ModelAdmin):
    # Fields to display in the Django admin
    list_display = ('room_number', 'category', 'rent', 'occupied', 'hotel', 'description')
    
    # Fields to make editable in the change list
    list_editable = ('rent', 'occupied')
    
    # Fields to filter in the right sidebar
    list_filter = ('category', 'hotel')
    
    # Fields to search in the search bar
    search_fields = ('room_number', 'category', 'description')
    
    # Fields to display in the change form
    fields = ('room_number', 'category', 'rent', 'occupied', 'hotel')
    
    # Read-only fields in the change form
    readonly_fields = ('description',)


admin.site.register(Room, RoomAdmin)