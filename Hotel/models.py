import phonenumbers
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField
from django.conf import settings


class CustomUser(AbstractUser):
    guest_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    nationality = CountryField()
    gender = models.CharField(max_length=10)
    
    def clean(self):
        super().clean()
        try:
            if self.phone_number:
                parsed_number = phonenumbers.parse(self.phone_number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number")

    def __str__(self):
        return self.name


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    num_rooms = models.IntegerField(default=0)    
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Room(models.Model):
    ROOM_CATEGORIES = [
        ('SUITE', 'Suite'),
        ('STUDIO', 'Studio'),
        ('CONNECTING', 'Connecting rooms'),
        ('SINGLE', 'Single room'),
        ('JUNIOR_SUITE', 'Junior Suite'),
        ('DELUXE', 'Deluxe Room'),
        ('DOUBLE', 'Double room'),
        ('PRESIDENTIAL', 'Presidential Suites'),
        ('TRIPLE', 'Triple room'),
    ]

    room_no = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, choices=ROOM_CATEGORIES)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=False)
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Room, self).save(*args, **kwargs)
        self.update_hotel_num_rooms()

    def delete(self, *args, **kwargs):
        super(Room, self).delete(*args, **kwargs)
        self.update_hotel_num_rooms()

    def update_hotel_num_rooms(self):
        hotel = self.hotel
        if hotel:
            hotel.num_rooms = Room.objects.filter(hotel=hotel).count()
            hotel.save()

    def __str__(self):
        return f"{self.category} - Room {self.room_no} - {self.hotel.name}"


class Reservation(models.Model):
    RESERVATION_STATUS = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed')
    ]

    reservation_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(CustomUser, related_name='reservations', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS)

    def __str__(self):
        return f"Reservation id {self.reservation_id} - Room id/number {self.room.room_no} - hotel name - {self.hotel.name}"
