from django.urls import path
from . import views

urlpatterns = [
    path("<str:tipo>", views.costos, name="Costos"),
    path(
        "CostosXCrianza/<int:id>",
        views.costosxcrianza,
        name="CostosXCrianza",
    ),
    path(
        "CostosXCrianza/CostosXCuenta/<str:idcuentamadre>",
        views.costosxcuenta,
        name="CostosXCuenta",
    ),
    path(
        "CostosXCrianza/CostosXCuenta/CostosXsubCuenta/<str:idcuenta>",
        views.costosxsubcuenta,
        name="CostosXsubCuenta",
    ),
]
