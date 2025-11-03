from django.urls import path

from . import views

app_name = "tipos_servico"

urlpatterns = [
    path("", views.list_tipos_servico, name="list"),
    path("novo/", views.create_tipo_servico, name="create"),
    path("<uuid:pk>/editar/", views.update_tipo_servico, name="update"),
]
