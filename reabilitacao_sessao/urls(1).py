from django.urls import path

from neurocare_project import placeholders as project_placeholders

app_name = "reabilitacao_sessao"

urlpatterns = [
    path("", project_placeholders.placeholder, {"title": "Sessões de Reabilitação"}, name="list"),
]
