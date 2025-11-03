from django.urls import path

from . import views

app_name = "tipos_produto"

urlpatterns = [
    path("", views.list_tipos, name="list"),
    path("novo/", views.create_tipo, name="create"),
    path("<uuid:pk>/editar/", views.update_tipo, name="update"),
]
