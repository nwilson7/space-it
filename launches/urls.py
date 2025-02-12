from django.urls import path
from . import views
from . import utils

urlpatterns = [
    path("your-launches/", views.view_your_launches, name="view_your_launches"),
    path("", views.view_all_launches, name="view_all_launches"),
    path("add/", views.add_launch, name="add_launch"),
    path("edit/<int:id>/", views.edit_launch, name="edit_launch"),
    path("delete/<int:id>/", views.delete_launch, name="delete_launch"),
    path("get_available_rockets/", utils.get_available_rockets, name='get_available_rockets'),
    path("make_booking/<int:id>/", views.make_booking, name="make_booking"),
    path("view_booked/<int:id>/", views.view_booked, name="view_booked")
]
