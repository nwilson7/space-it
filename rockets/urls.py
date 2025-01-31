from django.urls import path,include
from . import views

urlpatterns = [
    path('view_rockets',views.view_rockets, name='view_rockets'),
    path('add_rocket/',views.add_rocket, name='add_rocket'),
    path('edit_rocket/<int:id>/', views.edit_rocket, name='edit_rocket'),
    path('delete_rocket/<int:id>/', views.delete_rocket, name='delete_rocket'),
]