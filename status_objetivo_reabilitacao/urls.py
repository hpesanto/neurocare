from django.urls import path

from . import views

app_name = "status"

urlpatterns = [
    path("", views.list_status, name="list"),
    path("create/", views.create_status, name="create"),
    path("update/<uuid:pk>/", views.update_status, name="update"),
]
