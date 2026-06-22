from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "User"),
        ("owner", "Owner"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    ROOM_TYPES = (
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('DELUXE', 'Deluxe'),
        ('SUITE', 'Suite'),
    )

    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE,related_name='rooms')
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_number}"


class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='bookings')

    check_in_date = models.DateField()
    check_out_date = models.DateField()

    total_price = models.DecimalField(max_digits=10,decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.room.room_number}"
    
