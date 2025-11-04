from django.urls import path

from . import views

app_name = "reabilitacao"

urlpatterns = [
    path("", views.list_reabilitacao, name="list"),
    path("create/", views.create_reabilitacao, name="create"),
    path("update/<uuid:pk>/", views.update_reabilitacao, name="update"),
]
