"""
Reservations urls
"""
from django.urls import path

from reservations.views import reservation

urlpatterns = [
    path('reservation/',
         reservation.ReservationListView.as_view(),
         name='reservation_list'),
    path('reservation/<int:pk>/',
         reservation.ReservationDetailView.as_view(),
         name='reservation_detail'),
    path('reservation/create/',
         reservation.ReservationCreationView.as_view(),
         name='reservation_creation'),
    path('reservation/<int:pk>/edit/',
         reservation.ReservationEditView.as_view(),
         name='reservation_edit'),
    path('reservation/<int:pk>/cancel/',
         reservation.ReservationCancelView.as_view(),
         name='reservation_cancel'),
]
