from django.urls import path

from . import views

app_name = "faixas"

urlpatterns = [
    path("", views.list_faixas, name="list"),
    path("novo/", views.create_faixa, name="create"),
    path("<uuid:pk>/editar/", views.update_faixa, name="update"),
]
