from django.urls import path

from . import views

app_name = "formas_pagamento"

urlpatterns = [
    path("", views.list_formas, name="list"),
    path("novo/", views.create_forma, name="create"),
    path("<uuid:pk>/editar/", views.update_forma, name="update"),
]
