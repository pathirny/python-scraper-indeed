from django.contrib import admin
from django.urls import path, include

urlpatters = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]