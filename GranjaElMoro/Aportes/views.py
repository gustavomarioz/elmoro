from django.shortcuts import render, redirect
from django.db.models import Sum, F, Q
from django.contrib import messages
from Aportes.models import Aporte
from Repartos.models import Socio
from .forms import AporteForm


def aportecrud(request):
    aportesenpesos = Aporte.objects.select_related("idsocio").filter(moneda="P")
    aportesendolar = Aporte.objects.select_related("idsocio").filter(moneda="D")
    aportes = aportesenpesos | aportesendolar

    aportescrud = {}
    totald = 0
    totalp = 0
    for aporte in aportes:
        imported = 0
        importep = 0
        if aporte.moneda == "P":
            importep = aporte.importe
            totalp += aporte.importe
        else:
            imported = aporte.importe
            totald += aporte.importe
        d = {
            aporte.idaporte: {
                "fecha": aporte.fecha,
                "socio": aporte.idsocio.socio,
                "importe_p": importep,
                "importe_d": imported,
                "cot_ofi": aporte.cot_usd_ofi,
                "cot_par": aporte.cot_usd_par,
            }
        }
        aportescrud.update(d)

    aportestotal = {
        "total_pesos": totalp,
        "total_dolar": totald,
    }

    return render(
        request,
        "Aportes/aportecrud.html",
        {"aportescrud": aportescrud, "aportestotal": aportestotal},
    )


def crearaporte(request):
    if request.method == "POST":
        aporte_form = AporteForm(request.POST)
        if aporte_form.is_valid():
            aporte_form.save()
            return redirect("/Aportes/Crud/CrearAporte/")
        else:
            messages.error(request, "Error en el ingreso de datos")
            return redirect("/Aportes/Crud/CrearAporte/")
    else:
        aporte_form = AporteForm()

    return render(request, "Aportes/crearaporte.html", {"form": aporte_form})


def editaraporte(request, id):
    try:
        aporte = Aporte.objects.get(idaporte=id)
    except Aporte.DoesNotExist:
        messages.error(request, "No existe el Aporte")
        return redirect("/Aportes/Crud/EditarAporte/")

    if request.method == "POST":
        print("aporte=", aporte)
        aporte_form = AporteForm(request.POST, instance=aporte)
        if aporte_form.is_valid():
            aporte_form.save()
            return redirect("/Aportes/Crud/")
    else:
        aporte_form = AporteForm(instance=aporte)

    return render(request, "Aportes/editaraporte.html", {"form": aporte_form})


def eliminaraporte(request, id):
    aporte = Aporte.objects.get(idaporte=id)
    aporte.delete()

    return redirect("/Aportes/Crud")


def aporteporsocio(request):
    aportesporidsocio = (
        Aporte.objects.select_related("idsocio")
        .values("idsocio")
        .annotate(
            Total_Pesos_Socio=Sum("importe", filter=Q(moneda="P")),
            Total_Dolares_Socio=Sum("importe", filter=Q(moneda="D")),
        )
        .order_by("-Total_Pesos_Socio")
    )

    aportesporsocio = {}
    total_pesos = 0
    total_dolar = 0

    for aporteporidsocio in aportesporidsocio:
        socio = Socio.objects.get(idsocio=aporteporidsocio["idsocio"])
        d = {
            socio.socio: {
                "impte_pesos": aporteporidsocio["Total_Pesos_Socio"],
                "impte_dolar": aporteporidsocio["Total_Dolares_Socio"],
            }
        }
        aportesporsocio.update(d)
        total_pesos += aporteporidsocio["Total_Pesos_Socio"]
        total_dolar += aporteporidsocio["Total_Dolares_Socio"]

    aportespormoneda = {
        "total_pesos": total_pesos,
        "total_dolar": total_dolar,
    }

    return render(
        request,
        "Aportes/aporteporsocio.html",
        {"aportesporsocio": aportesporsocio, "aportespormoneda": aportespormoneda},
    )


def aporteporsociopeso(request):
    aportesporsociopeso = (
        Aporte.objects.filter(moneda="P")
        .values("idsocio")
        .annotate(
            Total_Pesos=Sum("importe"),
            Total_US_Oficial=Sum(F("importe") / F("cot_usd_ofi")),
            Total_US_Blue=Sum(F("importe") / F("cot_usd_par")),
            Total_US_Promedio=Sum(
                F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
            ),
        )
        .order_by("-Total_Pesos")
    )

    aportesconsocios = {}
    total_pesos = 0
    total_dolofi = 0
    total_dolpar = 0
    total_dolprom = 0
    for aporteporsociopeso in aportesporsociopeso:
        socio = Socio.objects.get(idsocio=aporteporsociopeso["idsocio"])
        d = {
            socio.socio: {
                "impte_pesos": aporteporsociopeso["Total_Pesos"],
                "impte_usofi": aporteporsociopeso["Total_US_Oficial"],
                "impte_usblue": aporteporsociopeso["Total_US_Blue"],
                "impte_usprom": aporteporsociopeso["Total_US_Promedio"],
            }
        }
        aportesconsocios.update(d)
        total_pesos += aporteporsociopeso["Total_Pesos"]
        total_dolofi += aporteporsociopeso["Total_US_Oficial"]
        total_dolpar += aporteporsociopeso["Total_US_Blue"]
        total_dolprom += aporteporsociopeso["Total_US_Promedio"]

    totales = {
        "total_pesos": total_pesos,
        "total_dolofi": total_dolofi,
        "total_dolpar": total_dolpar,
        "total_dolprom": total_dolprom,
    }

    return render(
        request,
        "Aportes/aporteporsociopeso.html",
        {"aportesconsocios": aportesconsocios, "totales": totales},
    )


def aporteporsociodolar(request):
    aportesporsociodolar = (
        Aporte.objects.filter(moneda="D")
        .values("idsocio")
        .annotate(
            Total_Dolares=Sum("importe"),
            Total_Pesos_Ofi=Sum(F("importe") * F("cot_usd_ofi")),
            Total_Pesos_Blue=Sum(F("importe") * F("cot_usd_par")),
            Total_Pesos_Promedio=Sum(
                F("importe") * ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
            ),
        )
        .order_by("-Total_Dolares")
    )

    aportesconsocios = {}
    total_dolares = 0
    total_pesosofi = 0
    total_pesospar = 0
    total_pesosprom = 0
    for aporteporsociodolar in aportesporsociodolar:
        socio = Socio.objects.get(idsocio=aporteporsociodolar["idsocio"])
        d = {
            socio.socio: {
                "impte_dols": aporteporsociodolar["Total_Dolares"],
                "impte_pesofi": aporteporsociodolar["Total_Pesos_Ofi"],
                "impte_pesblue": aporteporsociodolar["Total_Pesos_Blue"],
                "impte_pesprom": aporteporsociodolar["Total_Pesos_Promedio"],
            }
        }
        aportesconsocios.update(d)
        total_dolares += aporteporsociodolar["Total_Dolares"]
        total_pesosofi += aporteporsociodolar["Total_Pesos_Ofi"]
        total_pesospar += aporteporsociodolar["Total_Pesos_Blue"]
        total_pesosprom += aporteporsociodolar["Total_Pesos_Promedio"]

    totales = {
        "total_dolares": total_dolares,
        "total_pesosofi": total_pesosofi,
        "total_pesospar": total_pesospar,
        "total_pesosprom": total_pesosprom,
    }

    return render(
        request,
        "Aportes/aporteporsociodolar.html",
        {"aportesconsocios": aportesconsocios, "totales": totales},
    )
