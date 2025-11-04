from django.urls import path

from . import views

app_name = "convenios"

urlpatterns = [
    path("", views.list_convenios, name="list"),
    path("novo/", views.create_convenio, name="create"),
    path("<uuid:pk>/editar/", views.update_convenio, name="update"),
]
