from django.urls import path

from . import views


app_name = "marriages"

urlpatterns = [
    path('', views.index, name="index")
]
