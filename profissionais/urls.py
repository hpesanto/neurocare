from django.urls import path

from . import views

app_name = "profissionais"

urlpatterns = [
    path("", views.list_profissionais, name="list"),
    path("novo/", views.create_profissional, name="create"),
    path("<uuid:pk>/editar/", views.update_profissional, name="update"),
]
