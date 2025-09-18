from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import views as project_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", include("accounts.urls")),
    path("cadastro/pacientes/", include("pacientes.urls")),
    path(
        "cadastro/profissionais/",
        project_views.under_construction,
        {"title": "Profissionais"},
        name="profissionais",
    ),
    path(
        "cadastro/usuarios/",
        project_views.under_construction,
        {"title": "Usuários"},
        name="usuarios",
    ),
    path(
        "agendamentos/",
        project_views.under_construction,
        {"title": "Agendamentos"},
        name="agendamentos",
    ),
]
