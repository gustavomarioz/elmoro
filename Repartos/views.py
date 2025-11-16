from django.shortcuts import render, redirect
from Repartos.models import Reparto, Socio
from django.db.models import Sum, F
from django.contrib import messages
from ResumenGral.models import Crianza
import Crianzas.static.Crianzas.py.granjaelmoro

# Create your views here.


def repartocrud(request):
    repartoscrud = Reparto.objects.all().order_by("-idcrianza_id", "-fecha")

    return render(
        request,
        "Repartos/repartocrud.html",
        {"repartoscrud": repartoscrud},
    )


def repartogestion(request, id):
    if id != "0":
        reparto = Reparto.objects.get(idreparto=id)
    else:
        reparto = {}

    return render(
        request,
        "Repartos/repartogestion.html",
        {"reparto": reparto},
    )


def guardarreparto(request, id):
    if not Crianzas.static.Crianzas.py.granjaelmoro.crianzavalida(
        request.POST["numidcrianza"]
    ):
        messages.error(request, "Error en el ingreso del número de crianza")
        return redirect("/Repartos/Crud/GestionarReparto/" + id)

    if not Crianza.objects.filter(idcrianza=int(request.POST["numidcrianza"])).exists():
        messages.error(request, "El número de crianza ingresado no existe")
        return redirect("/Repartos/Crud/GestionarReparto/" + id)

    if not Crianzas.static.Crianzas.py.granjaelmoro.importevalido(
        request.POST["floimporte"]
    ):
        messages.error(request, "Error en el ingreso del importe del reparto")
        return redirect("/Repartos/Crud/GestionarReparto/" + id)

    if not Crianzas.static.Crianzas.py.granjaelmoro.importevalido(
        request.POST["flocot_ofi"]
    ):
        messages.error(
            request, "Error en el ingreso de la cotizacion del dolar oficial"
        )
        return redirect("/Repartos/Crud/GestionarReparto/" + id)

    if not Crianzas.static.Crianzas.py.granjaelmoro.importevalido(
        request.POST["flocot_par"]
    ):
        messages.error(
            request, "Error en el ingreso de la cotizacion del dolar paralelo"
        )
        return redirect("/Repartos/Crud/GestionarReparto/" + id)

    idreparto = int(id)
    idcrianza = int(request.POST["numidcrianza"])
    fecha = request.POST["fecfecha"]
    importe = float(
        Crianzas.static.Crianzas.py.granjaelmoro.stringadouble(
            request.POST["floimporte"]
        )
    )
    cot_usd_ofi = float(
        Crianzas.static.Crianzas.py.granjaelmoro.stringadouble(
            request.POST["flocot_ofi"]
        )
    )
    cot_usd_par = float(
        Crianzas.static.Crianzas.py.granjaelmoro.stringadouble(
            request.POST["flocot_par"]
        )
    )
    cuota = float(
        Crianzas.static.Crianzas.py.granjaelmoro.stringadouble(
            request.POST["flocuota"]
        )
    )

    if idreparto != 0:
        reparto = Reparto.objects.get(idreparto=idreparto)
        reparto.idcrianza_id = idcrianza
        reparto.fecha = fecha
        reparto.importe = importe
        reparto.cot_usd_ofi = cot_usd_ofi
        reparto.cot_usd_par = cot_usd_par
        reparto.cuota = cuota
        reparto.save()
    else:
        reparto = Reparto.objects.create(
            idcrianza_id=idcrianza,
            fecha=fecha,
            importe=importe,
            cot_usd_ofi=cot_usd_ofi,
            cot_usd_par=cot_usd_par,
            cuota=cuota,
        )

    return redirect("/Repartos/Crud/")


def eliminarreparto(request, id):
    reparto = Reparto.objects.get(idreparto=id)
    reparto.delete()

    return redirect("/Repartos/Crud")


def repartoporanio(request):
    repartosporanio = (
        Reparto.objects.values("fecha__year")
        .annotate(
            Crianzas=Sum("cuota"),
            Total_Pesos=Sum("importe"),
            Pesos_x_Crianza=(Sum("importe")) / (Sum("cuota")),
            Total_US_Oficial=Sum(F("importe") / F("cot_usd_ofi")),
            USOf_x_Crianza=(Sum(F("importe") / F("cot_usd_ofi"))) / (Sum(F("cuota"))),
            Total_US_Blue=Sum(F("importe") / F("cot_usd_par")),
            USBlue_x_Crianza=(Sum(F("importe") / F("cot_usd_par"))) / (Sum(F("cuota"))),
            Total_US_Promedio=Sum(
                F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
            ),
            USProm_x_Crianza=(Sum(
                F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
            )) / (Sum(F("cuota"))),
        ).order_by("-fecha__year")
    )

    repartostotal = Reparto.objects.aggregate(
        Crianzas=Sum("cuota"),
        Total_Pesos=Sum("importe"),
        Pesos_x_Crianza=(Sum("importe")) / (Sum("cuota")),
        Total_US_Oficial=Sum(F("importe") / F("cot_usd_ofi")),
        USOf_x_Crianza=(Sum(F("importe") / F("cot_usd_ofi"))) / (Sum(F("cuota"))),
        Total_US_Blue=Sum(F("importe") / F("cot_usd_par")),
        USBlue_x_Crianza=(Sum(F("importe") / F("cot_usd_par"))) / (Sum(F("cuota"))),
        Total_US_Promedio=Sum(
            F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
        ),
        USProm_x_Crianza=(Sum(
            F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
        )) / (Sum(F("cuota"))),
    )

    return render(
        request,
        "Repartos/repartoporanio.html",
        {"repartosporanio": repartosporanio, "repartostotal": repartostotal},
    )


def repartoporcrianza(request):
    repartosporcrianza = (
        Reparto.objects.values("idcrianza_id")
        .annotate(
            Total_Pesos=Sum("importe"),
            Total_US_Oficial=Sum(F("importe") / F("cot_usd_ofi")),
            Total_US_Blue=Sum(F("importe") / F("cot_usd_par")),
            Total_US_Promedio=Sum(
                F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
            ),
        )
        .order_by("-idcrianza_id")
    )

    repartostotal = Reparto.objects.aggregate(
        Total_Pesos=Sum("importe"),
        Total_US_Oficial=Sum(F("importe") / F("cot_usd_ofi")),
        Total_US_Blue=Sum(F("importe") / F("cot_usd_par")),
        Total_US_Promedio=Sum(
            F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
        ),
    )

    return render(
        request,
        "Repartos/repartoporcrianza.html",
        {"repartosporcrianza": repartosporcrianza, "repartostotal": repartostotal},
    )


def repartoporsocio(request):
    repartosporsocio = Reparto.objects.aggregate(
        Total_Pesos=Sum("importe"),
        Total_US_Oficial=Sum(F("importe") / F("cot_usd_ofi")),
        Total_US_Blue=Sum(F("importe") / F("cot_usd_par")),
        Total_US_Promedio=Sum(
            F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
        ),
    )

    sociodic = {}
    socios = Socio.objects.filter(porcentaje__gt=0).order_by("socio")
    for socio in socios:
        d = {
            socio.socio: {
                "impte_pesos": repartosporsocio["Total_Pesos"] * socio.porcentaje / 100,
                "impte_usofi": repartosporsocio["Total_US_Oficial"]
                * socio.porcentaje
                / 100,
                "impte_usblue": repartosporsocio["Total_US_Blue"]
                * socio.porcentaje
                / 100,
                "impte_usprom": repartosporsocio["Total_US_Promedio"]
                * socio.porcentaje
                / 100,
            }
        }
        sociodic.update(d)

    return render(
        request,
        "Repartos/repartoporsocio.html",
        {"sociodic": sociodic, "repartosporsocio": repartosporsocio},
    )


def repartoporimpteusd(request):
    repartosporimpteusd = (
        Reparto.objects.values("idcrianza_id")
        .annotate(
            Total_Pesos=Sum("importe"),
            Total_US_Oficial=Sum(F("importe") / F("cot_usd_ofi")),
            Total_US_Blue=Sum(F("importe") / F("cot_usd_par")),
            Total_US_Promedio=Sum(
                F("importe") / ((F("cot_usd_ofi") + F("cot_usd_par")) / 2)
            ),
        )
        .order_by("idcrianza_id")
    )

    crianzas = 0
    totalpesos = 0
    totalusdofi = 0
    totalusdblue = 0
    totalusdprom = 0
    impteusd = {}
    for repartoporimpteusd in repartosporimpteusd:
        crianzas += 1
        totalpesos += repartoporimpteusd["Total_Pesos"]
        totalusdofi += repartoporimpteusd["Total_US_Oficial"]
        totalusdblue += repartoporimpteusd["Total_US_Blue"]
        totalusdprom += repartoporimpteusd["Total_US_Promedio"]
        d = {
            crianzas: {
                "impte_pesos": totalpesos,
                "impte_usofi": totalusdofi,
                "impte_usblue": totalusdblue,
                "impte_usprom": totalusdprom,
                "impte_usofi_prom": totalusdofi / crianzas,
                "impte_usblue_prom": totalusdblue / crianzas,
                "impte_usprom_prom": totalusdprom / crianzas,
            }
        }
        impteusd.update(d)
        impteusd_dic = dict(sorted(impteusd.items(), reverse=True))

    return render(
        request,
        "Repartos/repartoporimpteusd.html",
        {"repartosporimpteusd": impteusd_dic},
    )
