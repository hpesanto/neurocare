from django.urls import path

from . import views

app_name = "sessoes"

urlpatterns = [
    path("", views.list_sessoes, name="list"),
    path("create/", views.create_sessao, name="create"),
    path("update/<uuid:pk>/", views.update_sessao, name="update"),
]
