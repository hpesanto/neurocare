from django.urls import path

from . import views

app_name = "evolucao"

urlpatterns = [
    path("", views.list_evolucao, name="list"),
    path("create/", views.create_evolucao, name="create"),
    path("update/<uuid:pk>/", views.update_evolucao, name="update"),
]
