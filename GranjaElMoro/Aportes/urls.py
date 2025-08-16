from django.urls import path
from . import views

urlpatterns = [
    path("Crud/", views.aportecrud, name="Acrud"),
    path("Crud/CrearAporte/", views.crearaporte, name="CrearAporte"),
    path("Crud/EditarAporte/<id>", views.editaraporte, name="EditarAporte"),
    path("Crud/EliminarAporte/<id>", views.eliminaraporte, name="EliminarAporte"),
    path("PorSocioA/", views.aporteporsocio, name="PorSocioA"),
    path("PorSocioPeso/", views.aporteporsociopeso, name="PorSocioPeso"),
    path("PorSocioDolar/", views.aporteporsociodolar, name="PorSocioDolar"),
]
