import phonenumbers
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django_countries.fields import CountryField
from django.utils.safestring import mark_safe
from django.urls import reverse


class CustomUser(AbstractUser):
    """
    Modelo personalizado de usuario.
    """

    DOCUMENT_TYPES = [
        ('PASSPORT', 'Passport'),
        ('NIE', 'NIE'),
        ('DNI', 'DNI'),
    ]

    guest_id = models.AutoField(primary_key=True)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='PASSPORT')
    document = models.CharField(max_length=9)
    email = models.EmailField()
    nationality = CountryField(default='Spain')
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
    """
    Modelo para representar un hotel.
    """
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    direction = models.CharField(max_length=255)
    CountryField = CountryField(default='Spain')
    city = models.CharField(max_length=50)
    post_code = models.IntegerField()
    phonenumber = models.IntegerField()
    num_rooms = models.IntegerField(default=0)
    email = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Room(models.Model):
    """
    Modelo para representar una habitación de hotel.
    """
    ROOM_CATEGORIES = [
        ('Single', 'Single'),
        ('Suite', 'Suite'),
        ('Double', 'Double'),
    ]

    ESTADO = [
        ("Ocupado", "Ocupado"),
        ("Libre/Disponible", "Libre/Disponible"),
        ("Reservado", "Reservado"),
        ("Sucio/En Limpieza", "Sucio/En Limpieza"),
        ("En Mantenimiento/Reparaciones", "En Mantenimiento/Reparaciones"),
        ("Bloqueado", "Bloqueado"),
        ("Fuera de Servicio", "Fuera de Servicio"),
        ("Inhabitable/No disponible", "Inhabitable/No disponible")
    ]

    ROOM_DESCRIPTIONS = {
        'Single': 'Single room with one bed and a private bathroom',
        'Double': 'Double room with two beds and a private bathroom',
        'Suite': 'Suite with two rooms, an interconnecting door, and a private bathroom',
    }

    room_number = models.CharField(max_length=3)
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=ROOM_CATEGORIES)
    state = models.CharField(max_length=50, choices=ESTADO)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    adults = models.IntegerField(validators=[MaxValueValidator(3)])
    children = models.IntegerField(validators=[MaxValueValidator(3)])
    occupied = models.BooleanField(default=False)
    discapacity = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    television = models.BooleanField(default=False)
    phone = models.BooleanField(default=False)
    description = models.TextField(blank=True, default="")
    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    num_toilets = models.IntegerField(default=0)
    num_beds = models.IntegerField(default=0)

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
    """
    Modelo para representar una reserva de habitación de hotel.
    """
    RESERVATION_STATUS = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed')
    ]

    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    adults = models.IntegerField(validators=[MaxValueValidator(3)])
    children = models.IntegerField(validators=[MaxValueValidator(3)])
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS)
    guest = models.ForeignKey(CustomUser, related_name='reservations', on_delete=models.CASCADE, blank=True, null=True)
    hotel = models.ForeignKey('Hotel', related_name='reservations', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', related_name='reservation', on_delete=models.CASCADE)
    payment_method = models.ForeignKey('Metodo_pago', related_name='reservation', on_delete=models.CASCADE)

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


class Metodo_pago(models.Model):
    """
    Modelo para representar los métodos de pago disponibles.
    """
    PAYMENT_OPTIONS = [
        ('PAYPAL', 'paypal'),
        ('TARJETA BANCARIA', 'Tarjeta Bancaria'),
        ('EFECTIVO', 'Efectivo')     
    ]

    payment_type = models.CharField(max_length=50, choices=PAYMENT_OPTIONS)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.payment_type
