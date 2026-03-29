from django.urls import path
from . import views

urlpatterns = [
    path("", views.resumen, name="Resumen"),
    path(
        "DetalleXCrianza/<int:idcrianza>",
        views.detallexcrianza,
        name="DetalleXCrianza",
    ),
    path("imagen/<idcrianza>/", views.imagen, name="imagen"),
]
