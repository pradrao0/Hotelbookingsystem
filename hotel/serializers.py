from rest_framework import serializers
from .models import Hotel, Room, Booking
from datetime import date
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "role"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, data):
        room = data["room"]
        check_in = data["check_in_date"]
        check_out = data["check_out_date"]

        # 1. date validation
        if check_in >= check_out:
            raise serializers.ValidationError("Invalid dates")

        # 2. availability check
        conflict = Booking.objects.filter(
            room=room,
            check_in_date__lt=check_out,
            check_out_date__gt=check_in
        )

        if conflict.exists():
            raise serializers.ValidationError("Room already booked")

        # 3. room active check
        if not room.is_available:
            raise serializers.ValidationError("Room not available")

        # 4. pricing logic
        nights = (check_out - check_in).days
        total = nights * room.price

        # weekend logic
        if check_in.weekday() >= 5:
            total *= 1.2

        # peak season
        if check_in.month in [5, 6, 12]:
            total *= 1.5

        data["total_price"] = total

        return data

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["username"] = self.user.username
        data["role"] = self.user.role

        return data