from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('users.urls')),
    path('users/',include('users.urls')),
    path('rockets/',include('rockets.urls')),
    path('cargo/',include('cargo.urls')),
    path('launches/',include('launches.urls')),
    path('bookings/',include('bookings.urls'))
]
