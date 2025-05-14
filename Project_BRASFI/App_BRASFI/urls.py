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
    path('projecthub/', views.ProjectHubView, name='projecthub'),
    path("projecthub/create/", views.CreateProjectView, name="createprojeto"),
    path('projeto/<int:projeto_id>/aprovar/', views.aprovar_projeto, name='aprovar_projeto'),
    path('projeto/<int:projeto_id>/rejeitar/', views.rejeitar_projeto, name='rejeitar_projeto'),
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
    path('profile', views.EditProfileView, name='edit_profile'),
    path('projeto/<int:projeto_id>/forum/', views.forum_projeto, name='forum_projeto'),
    path('projecthub/novo_comentario/<int:projeto_id>/', views.novo_comentario, name='novo_comentario'),
    path('projecthub/responder/<int:comentario_id>/', views.responder_comentario, name='responder_comentario'),
    path('projecthub/delete/<int:projeto_id>/',views.delete_project,name='delete_project'),
    path('projeto/<int:projeto_id>/like/', views.like_projeto, name='like_projeto'),
    path('projeto/<int:projeto_id>/like/', views.curtir_projeto, name='curtir_projeto'),
    path('sugestoes-da-ia/', views.sugerir_desafios, name='sugerir_desafios'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)