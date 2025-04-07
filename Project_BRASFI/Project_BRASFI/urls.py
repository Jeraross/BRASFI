from django.contrib import admin
from django.urls import path, include #Lembre de importar o include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('App_BRASFI.urls')), 
]