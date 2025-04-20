from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Video

def LandingView(request):
    return render(request, 'landing.html')

def LoginView(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("App_BRASFI:projecthub"))
        else:
            return render(request, "login.html", {
                "message": "Senha ou usuário inválido."
            })
    else:
        return render(request, "login.html")


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("App_BRASFI:landing"))

def RegisterView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        tipo = request.POST.get("tipo")
        profile = request.FILES.get("profile")

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Senhas não coincidem."
            })

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.userType = tipo

            if profile:
                user.profilePic = profile

            user.save()

        except IntegrityError:
            return render(request, "register.html", {
                "message": "Usuário já existe."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("App_BRASFI:projecthub"))

    return render(request, "register.html")


@login_required
def ProjectHubView(request):
    return render(request, "projecthub.html", {
        "page": "projecthub"
    })

@login_required
def NetworkHubView(request):
    return render(request, "networkhub.html", {
        "page": "networkhub"
    })

@login_required
def VideosView(request):
    all_videos = Video.objects.all().order_by('-created_at')
    return render(request, "videos.html", {
        "page": "videos",
        "videos": all_videos,
    })

def CreateVideoView(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        video_file = request.FILES.get("video_file")

        if title and description and video_file:
            try:
                with transaction.atomic():
                    video = Video.objects.create(
                        title=title,
                        description=description,
                        video_file=video_file,
                        user=request.user
                    )
                    video.save()
                messages.success(request, "Vídeo criado com sucesso!")
                return HttpResponseRedirect(reverse('App_BRASFI:videos'))
            except IntegrityError:
                messages.error(request, "Erro ao criar o vídeo.")
                return HttpResponseRedirect(reverse('App_BRASFI:videos'))
    else:
        return HttpResponse("Method must be 'POST'")

@login_required
def QuizzesView(request):
    return render(request, "quizzes.html", {
        "page": "quizzes"
    })

@login_required
def CuradoriaView(request):
    return render(request, "curadoria.html", {
        "page": "curadoria"
    })