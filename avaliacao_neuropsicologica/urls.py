from django.urls import path

from . import views

app_name = "avaliacao"

urlpatterns = [
    path("", views.list_avaliacao, name="list"),
    path("create/", views.create_avaliacao, name="create"),
    path("update/<uuid:pk>/", views.update_avaliacao, name="update"),
]
