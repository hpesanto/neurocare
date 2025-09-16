from django.urls import path

from . import views

app_name = "pacientes"

urlpatterns = [
    path("", views.list_pacientes, name="list"),
    path("novo/", views.create_paciente, name="create"),
    path("<uuid:pk>/editar/", views.update_paciente, name="update"),
]
