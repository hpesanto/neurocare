from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.list_usuarios, name="list"),
    path("novo/", views.create_usuario, name="create"),
    path("<uuid:pk>/editar/", views.update_usuario, name="update"),
]
