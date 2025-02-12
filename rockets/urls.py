from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.view_rockets, name='view_rockets'),
    path('add/',views.add_rocket, name='add_rocket'),
    path('edit/<int:id>/', views.edit_rocket, name='edit_rocket'),
    path('delete/<int:id>/', views.delete_rocket, name='delete_rocket'),
]