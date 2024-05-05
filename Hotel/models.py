from django.db import models


class Guest(models.Model):
    guest_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=255)
    nationality = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    reservation_history = models.CharField(max_length=255)


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    num_rooms = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    contact_info = models.CharField(max_length=255)


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

    room_no = models.IntegerField(primary_key=True)
    category = models.CharField(max_length=50, choices=ROOM_CATEGORIES)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)


class Reservation(models.Model):
    RESERVATION_STATUS = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed')
    ]

    reservation_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(Guest, related_name='reservations', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS)
