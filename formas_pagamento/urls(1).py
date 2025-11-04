from django.urls import path

from . import views

app_name = "formas_pagamento"

urlpatterns = [
    path("", views.list_formas, name="list"),
    path("create/", views.create_forma, name="create"),
    path("update/<uuid:pk>/", views.update_forma, name="update"),
]
