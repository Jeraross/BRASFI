from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User

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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Senha ou usuário inválido."
            })
    else:
        return render(request, "login.html")


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("LandingView"))

def Register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        profile = request.FILES.get("profile")
        tipo = request.POST["tipo"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "register.html", {
                "message": "Senhas não coincidem."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.profilePic = profile
            user.userType = tipo

            user.save()

        except IntegrityError:
            return render(request, "register.html", {
                "message": "Usuário já existe."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("LoginView"))
    else:
        return render(request, "register.html")
