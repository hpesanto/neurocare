from django.urls import path

from . import views

app_name = "tipos_transacao"

urlpatterns = [
    path("", views.list_tipos, name="list"),
    path("create/", views.create_tipo, name="create"),
    path("update/<uuid:pk>/", views.update_tipo, name="update"),
    path("delete/<uuid:pk>/", views.delete_tipo, name="delete"),
]
