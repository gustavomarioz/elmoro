from django.urls import path
from . import views

urlpatterns = [
    path("<str:tipo>", views.cobranzas, name="Cobranzas"),
    path(
        "CobrosXCrianza/<int:id>",
        views.cobrosxcrianza,
        name="CobrosXCrianza",
    ),
    path(
        "CobrosXCrianza/CobrosXCuenta/<str:idcuenta>",
        views.cobrosxcuenta,
        name="CobrosXCuenta",
    ),
]
