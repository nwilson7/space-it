from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.index, name='home'),
    path('signup/', views.signup_user, name='signup'),
]