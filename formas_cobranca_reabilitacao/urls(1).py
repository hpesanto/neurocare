from django.urls import path

from . import views

app_name = "formas_cobranca_reabilitacao"

urlpatterns = [
    path("", views.list_formas_cobranca, name="list"),
    path("create/", views.create_forma_cobranca, name="create"),
    path("update/<uuid:pk>/", views.update_forma_cobranca, name="update"),
]
