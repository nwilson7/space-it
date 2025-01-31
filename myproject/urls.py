from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< Updated upstream
    path('',include('myapp.urls')),
    path('users/',include('users.urls')),
    path('rockets/',include('rockets.urls')),
    path('cargo/',include('cargo.urls')),
=======
    path('',include('users.urls')),
>>>>>>> Stashed changes
]
