# core/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render


class CustomLoginView(LoginView):
    template_name = "core/login.html"


class CustomLogoutView(LogoutView):
    next_page = "/"  # Redireciona para a home após logout


def home(request):
    return render(request, "core/home.html")
