from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView
)

from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import Hotel, Room, Booking
from .serializers import HotelSerializer, RoomSerializer, BookingSerializer

from .permissions import (
    IsAdminOrReadOnly,
    IsOwner,
    IsUser,
    IsOwnerOrAdmin,
    IsBookingOwner
)

from .utils import send_booking_email
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.generics import CreateAPIView
from .serializers import RegisterSerializer 


class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []  # anyone can register
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class HotelListCreateView(ListCreateAPIView):
    serializer_class = HotelSerializer
    permission_classes = [IsOwnerOrAdmin]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["city", "rating"]
    search_fields = ["name", "city"]

    def get_queryset(self):
        cached = cache.get("hotels")

        if cached:
            return cached

        data = Hotel.objects.all()
        cache.set("hotels", data, timeout=60)
        return data

    def perform_create(self, serializer):
        cache.delete("hotels")
        serializer.save(owner=self.request.user)
    

class HotelDetailView(RetrieveAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer



class RoomListCreateView(ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsOwner]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["room_type", "price", "is_available"]
    search_fields = ["room_number"]

    def get_queryset(self):
        hotel_id = self.kwargs.get("hotel_id")
        cache_key = f"rooms_{hotel_id}"

        cached = cache.get(cache_key)
        if cached:
            return cached

        if hotel_id:
            data = Room.objects.filter(hotel_id=hotel_id)
        else:
            data = Room.objects.all()

        cache.set(cache_key, data, timeout=60)
        return data

    def perform_create(self, serializer):
        cache.delete_pattern("rooms_*")

        # ensure owner owns hotel (important rule)
        serializer.save()



class RoomDetailView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingListCreateView(ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsUser]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)

        send_booking_email(
            self.request.user.email,
            booking
        )   
    
class BookingDetailView(RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsBookingOwner]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)