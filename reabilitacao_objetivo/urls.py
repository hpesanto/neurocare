from django.urls import path

from . import views

app_name = "reabilitacao_objetivo"

urlpatterns = [
    path("", views.list_objetivos, name="list"),
    path("create/", views.create_objetivo, name="create"),
    path("update/<uuid:pk>/", views.update_objetivo, name="update"),
]
