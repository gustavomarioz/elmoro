from django.urls import path
from . import views

urlpatterns = [
    path(
        "<str:tipo>",
        views.resultados,
        name="Resultados",
    ),
    path(
        "ResultadosXCrianza/<int:id>",
        views.resultadosxcrianza,
        name="ResutadosXCrianza",
    ),
]
