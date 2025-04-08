from django.urls import path

from . import views


app_name = "persons"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:person_id>', views.details, name="details"),
    path('<int:person_id>/add-parents', views.add_parents, name="add_parents"),
    path('<int:person_id>/family-tree', views.family_tree, name="family_tree"),
]
