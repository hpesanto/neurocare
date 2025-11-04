from django.urls import path

from . import views

app_name = "formas_cobranca"

urlpatterns = [
    path("", views.list_formas, name="list"),
    path("create/", views.create_forma, name="create"),
    path("update/<uuid:pk>/", views.update_forma, name="update"),
]
