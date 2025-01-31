from django.urls import path
from . import views
from .views import get_available_rockets

urlpatterns = [
    path("your-launches/", views.view_launches, name="view_launches"),
    path("", views.view_all_launches, name="view_all_launches"),
    path("add/", views.add_launch, name="add_launch"),
    path("edit/<int:id>/", views.edit_launch, name="edit_launch"),
    path("delete/<int:id>/", views.delete_rocket, name="launch_rocket"),
    path("get_available_rockets/", get_available_rockets, name='get_available_rockets'),
]
