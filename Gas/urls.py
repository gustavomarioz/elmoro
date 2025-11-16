from django.urls import path
from . import views


urlpatterns = [
    path("Crud/", views.gascrud, name="GasCrud"),
    path("Crud/CrearGas/", views.creargas, name="CrearGas"),
    path("Crud/EditarGas/<id>", views.editargas, name="EditarGas"),
    path("Crud/EliminarGas/<id>", views.eliminargas, name="EliminarGas"),
    path("GasConsumo", views.listargas, name="GasConsumo"),
]
