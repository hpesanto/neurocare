from django.urls import path

from neurocare_project import placeholders as project_placeholders

app_name = "reabilitacao_objetivo"

urlpatterns = [
    path(
        "",
        project_placeholders.placeholder,
        {"title": "Objetivos de Reabilitação"},
        name="list",
    ),
]
