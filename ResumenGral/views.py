from django.shortcuts import render
from django.contrib import messages
from ResumenGral.models import Crianza, DetalleDeCrianza

# Create your views here.


def resumen(request):
    crianzas = Crianza.objects.all()
    return render(request, "ResumenGral/resumen.html", {"crianzas": crianzas})


def detallexcrianza(request, idcrianza):
    detalles = DetalleDeCrianza.objects.filter(crianza_id=idcrianza)
    if detalles:
        crianza = Crianza.objects.get(idcrianza=idcrianza)
    else:
        messages.info(request, "Esta Crianza no posee detalles por galpón")
        crianza = {"idcrianza": idcrianza}
    return render(request, "ResumenGral/detalle.html", {"detalles": detalles, "crianza": crianza})


def imagen(request, idcrianza):
    imagen = Crianza.objects.get(idcrianza=idcrianza)
    return render(request, "ResumenGral/imagen.html", {"imagen": imagen})
