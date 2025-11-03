from django.urls import path

from . import views

app_name = "vendas"

urlpatterns = [
    path("", views.list_vendas, name="list"),
    path("create/", views.create_venda, name="create"),
    path("update/<uuid:pk>/", views.update_venda, name="update"),
]
