from django.urls import path

from . import views

app_name = "transacoes"

urlpatterns = [
    path("", views.list_transacoes, name="list"),
    path("create/", views.create_transacao, name="create"),
    path("update/<uuid:pk>/", views.update_transacao, name="update"),
]
