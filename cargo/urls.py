from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.view_cargo, name='view_cargo'),
    path('add/', views.add_cargo, name='add_cargo'),
    path('edit/<int:id>/', views.edit_cargo, name='edit_cargo'),
    path('delete/<int:id>/', views.delete_cargo, name='delete_cargo'),
    path('launch/<int:id>/', views.launch_cargo, name='launch_cargo'),
]