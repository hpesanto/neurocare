from django.urls import path

from . import views

app_name = "paciente_servico"

urlpatterns = [
    path("", views.list_paciente_servicos, name="list"),
    path("novo/", views.create_paciente_servico, name="create"),
    path("<uuid:pk>/editar/", views.update_paciente_servico, name="update"),
]
