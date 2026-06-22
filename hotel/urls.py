from django.urls import path
from .views import (
    HotelListCreateView,
    HotelDetailView,
    RoomListCreateView,
    RoomDetailView,
    BookingListCreateView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    # 🏨 HOTEL APIs
    path('hotels/', HotelListCreateView.as_view(), name='hotel-list-create'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='hotel-detail'),

    # 🛏️ ROOM APIs
    path('rooms/', RoomListCreateView.as_view(), name='room-list-create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),

    # 🏨➡️🛏️ ROOMS UNDER SPECIFIC HOTEL
    path('hotels/<int:hotel_id>/rooms/', RoomListCreateView.as_view(), name='hotel-rooms'),

    # 📅 BOOKING APIs
    path('bookings/', BookingListCreateView.as_view(), name='booking-list-create'),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
]