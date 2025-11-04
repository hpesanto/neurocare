from django.urls import path

from . import views

app_name = "contatos_emergencia"

urlpatterns = [
    path("", views.list_contatos, name="list"),
    path("novo/", views.create_contato, name="create"),
    path("<uuid:pk>/editar/", views.update_contato, name="update"),
]
