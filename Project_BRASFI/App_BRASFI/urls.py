from django.urls import path
from . import views

app_name = 'App_BRASFI'

urlpatterns = [
    path('', views.LandingView.as_view(), name='Landing'),  
]