from django.urls import path
from . import views


urlpatterns = [
    path("Crud/", views.luzcrud, name="LuzCrud"),
    path("Crud/CrearLuz/", views.crearluz, name="CrearLuz"),
    path("Crud/EditarLuz/<id>", views.editarluz, name="EditarLuz"),
    path("Crud/EliminarLuz/<id>", views.eliminarluz, name="EliminarLuz"),
    path("LuzConsumo", views.listarluz, name="LuzConsumo"),
]
