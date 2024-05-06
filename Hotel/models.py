import phonenumbers
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField
from django.utils.safestring import mark_safe
from django.urls import reverse


class CustomUser(AbstractUser):
    guest_id = models.AutoField(primary_key=True)
    nationality = CountryField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        try:
            if self.phone_number:
                parsed_number = phonenumbers.parse(self.phone_number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise ValidationError("Invalid phone number")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValidationError("Invalid phone number")

    def __str__(self):
        return self.username


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    num_rooms = models.IntegerField(default=0)
    contact_info = models.CharField(max_length=20)

    def __str__(self):
        return self.name


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

    ROOM_DESCRIPTIONS = {
        'SUITE': 'Big room with two beds and luxurious amenities',
        'STUDIO': 'Spacious room with a sitting area and workspace',
        'CONNECTING': 'Two rooms with an interconnecting door',
        'SINGLE': 'Cozy room with a single bed',
        'JUNIOR_SUITE': 'Room with a separate seating area',
        'DELUXE': 'High-end room with premium amenities',
        'DOUBLE': 'Room with a double bed',
        'PRESIDENTIAL': 'Luxurious and spacious suite',
        'TRIPLE': 'Room with three beds'
    }

    room_number = models.IntegerField(unique=True)
    category = models.CharField(max_length=50, choices=ROOM_CATEGORIES)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    occupied = models.BooleanField(default=False)
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    description = models.TextField(blank=True, default="")

    def save(self, *args, **kwargs):
        self.description = self.ROOM_DESCRIPTIONS.get(self.category, 'No description available')
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
        return f"{self.category} - Room {self.room_number} - {self.hotel.name}"


class Reservation(models.Model):
    RESERVATION_STATUS = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed')
    ]

    guest = models.ForeignKey(CustomUser, related_name='reservations', on_delete=models.CASCADE, blank=True, null=True)
    hotel = models.ForeignKey('Hotel', related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', related_name='reservation', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS)

    def clean(self):
        print(self.guest)
        if not self.check_in_date or not self.check_out_date:
            raise ValidationError("Both check-in and check-out dates are required.")
        elif self.check_in_date >= self.check_out_date:
            raise ValidationError("Check-out date must be after check-in date.")
        
    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.room.occupied:
                raise ValidationError("Room is already occupied.")
            self.room.occupied = True
            self.room.save()
        elif self.status in ['CANCELLED', 'COMPLETED']:
            self.room.occupied = False
            self.room.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation id {self.pk} - Room id/number {self.room.id} - hotel name - {self.hotel.name}"
