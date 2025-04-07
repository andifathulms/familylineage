from django.urls import path

from . import views


app_name = "persons"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:person_id>', views.details, name="details"),
]
