from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'App_BRASFI'

urlpatterns = [
    path('', views.LandingView, name='landing'), 
    path("n/login", views.LoginView, name="login"),
    path("n/logout", views.LogoutView, name="logout"), 
    path("n/register", views.Register, name="register"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)