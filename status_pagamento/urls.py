from django.urls import path

from . import views

app_name = "status_pagamento"

urlpatterns = [
    path("", views.list_status_pagamento, name="list"),
    path("create/", views.create_status, name="create"),
    path("update/<uuid:pk>/", views.update_status, name="update"),
    path("delete/<uuid:pk>/", views.delete_status, name="delete"),
]
