from django.urls import path

from . import views

app_name = "produtos"

urlpatterns = [
    path("", views.list_produtos, name="list"),
    path("novo/", views.create_produto, name="create"),
    path("<uuid:pk>/editar/", views.update_produto, name="update"),
]
