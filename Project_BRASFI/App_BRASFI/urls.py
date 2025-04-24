from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'App_BRASFI'

urlpatterns = [
    path('', views.LandingView, name='landing'), 
    path("login", views.LoginView, name="login"),
    path("logout", views.LogoutView, name="logout"), 
    path("register", views.RegisterView, name="register"),
    path('projecthub', views.ProjectHubView, name='projecthub'),
    path('networkhub', views.NetworkHubView, name='networkhub'), 
    path('videos', views.VideosView, name='videos'),
    path('videos/create/', views.CreateVideoView, name="createvideo"),
    path('video/delete/<int:video_id>/', views.DeleteVideoView, name='delete_video'),
    path('quizzes', views.QuizzesView, name='quizzes'),
    path('quizzes/create/', views.CreateQuizView, name='create_quiz'),
    path('quizzes/delete/<int:quiz_id>/', views.DeleteQuizView, name='delete_quiz'), 
    path('curadoria', views.CuradoriaView, name='curadoria'),
    path('quizzes/play/<int:quiz_id>/', views.PlayQuizView, name='play_quiz'),
    path('quizzes/submit/', views.SubmitQuizResultView, name='submit_quiz'),
    path('', views.landing, name='landing'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)