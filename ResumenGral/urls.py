from django.urls import path
from . import views

urlpatterns = [
    path("", views.resumen, name="Resumen"),
    path("imagen/<idcrianza>/", views.imagen, name="imagen"),
]
