from django.urls import path

from . import views

app_name = "vendas_geral"

urlpatterns = [
    path("", views.list_venda_geral, name="list"),
    path("create/", views.create_venda_geral, name="create"),
    path("update/<uuid:pk>/", views.update_venda_geral, name="update"),
    # Itens de Venda Geral
    path("itens/", views.list_venda_geral_itens, name="itens_list"),
    path("itens/create/", views.create_venda_geral_item, name="itens_create"),
    path("itens/update/<uuid:pk>/", views.update_venda_geral_item, name="itens_update"),
]
