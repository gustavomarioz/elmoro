from django.shortcuts import render
from ResumenGral.models import Crianza

# Create your views here.


def resumen(request):
    crianzas = Crianza.objects.all()
    return render(request, "ResumenGral/resumen.html", {"crianzas": crianzas})


def imagen(request, idcrianza):
    imagen = Crianza.objects.get(idcrianza=idcrianza)
    return render(request, "ResumenGral/imagen.html", {"imagen": imagen})
