from django.urls import path
from . import views

urlpatterns = [
    path("Crud/", views.repartocrud, name="Rcrud"),
    path("Crud/GestionarReparto/<id>", views.repartogestion, name="GestionarReparto"),
    path(
        "Crud/GestionarReparto/GuardarReparto/<id>",
        views.guardarreparto,
        name="GuardarReparto",
    ),
    path("Crud/EliminarReparto/<id>", views.eliminarreparto, name="EliminarReparto"),
    path("PorAnio/", views.repartoporanio, name="PorAnio"),
    path("PorCrianza/", views.repartoporcrianza, name="PorCrianza"),
    path("PorSocioR/", views.repartoporsocio, name="PorSocioR"),
    path("PorImpteUS/", views.repartoporimpteusd, name="PorImpteUS"),
]
