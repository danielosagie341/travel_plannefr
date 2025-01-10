from django.urls import path
from .views import (
    TripListView,
    TripDetailView,
    TripCreateView,
    TripUpdateView,
    TripDeleteView,
    MyTripListView,
)

urlpatterns = [
    path('', TripListView.as_view(), name='trip-list'),
    path('my-trips/', MyTripListView.as_view(), name='my-trips'),
    path('trip/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
    path('trip/new/', TripCreateView.as_view(), name='trip-create'),
    path('trip/<int:pk>/update/', TripUpdateView.as_view(), name='trip-update'),
    path('trip/<int:pk>/delete/', TripDeleteView.as_view(), name='trip-delete'),
]