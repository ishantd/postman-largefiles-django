from django.contrib import admin
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('upload/', include('upload.urls')),
    path('data/', include('data.urls')),
]
