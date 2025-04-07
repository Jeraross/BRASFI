from django.shortcuts import render
from django.views import View

class LandingView(View):
    def get(self, request): 
        return render(request, 'landing.html')