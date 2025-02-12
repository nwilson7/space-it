from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_your_bookings, name="view_your_bookings"),
    path("cancel/<int:id>/", views.cancel_booking, name="cancel_booking")
]