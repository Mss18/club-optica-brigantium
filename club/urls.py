from django.urls import path

from . import views

app_name = "club"

urlpatterns = [
    path("", views.inicio, name="inicio"),
]
