from django.shortcuts import render
from ResumenGral.models import Crianza
from RegistroContable.models import RegistroContable
from Cuentas.models import Cuenta
from django.db.models import Q

# Create your views here.


def resultados(request, tipo):

    request.session["tipo"] = tipo

    resultados = {}
    crianzas = Crianza.objects.filter(idcrianza__gt=16)
    for crianza in crianzas:
        total_costo_pesos = 0.0
        total_costo_usd = 0.0
        total_cobro_pesos = 0.0
        total_cobro_usd = 0.0

        filtro = armar_filtro1(tipo, crianza.fechainicio, crianza.fechahasta)
        registros = RegistroContable.objects.filter(
            (
                (Q(idcuenta__gt="00.00") & Q(idcuenta__lt="00.04"))
                | (
                    (Q(idcuenta__gt="01.00") & Q(idcuenta__lt="06.00"))
                    & (~Q(idcuenta="03.05") & ~Q(idcuenta="03.98"))
                )
            )
        ).filter(filtro)
        for registro in registros:

            if tipo == "d":
                dias = calculo_dias(
                    registro.aplicadesde,
                    registro.aplicahasta,
                    crianza.fechainicio,
                    crianza.fechahasta,
                )
                aplicadias = (registro.aplicahasta - registro.aplicadesde).days + 1
                subtotalpesos = dias / aplicadias * registro.importe
                subtotalusd = subtotalpesos / registro.cot_usd_par
                if registro.idcuenta_id[:2] == "00":
                    total_cobro_pesos += subtotalpesos
                    total_cobro_usd += subtotalusd
                else:
                    total_costo_pesos += subtotalpesos
                    total_costo_usd += subtotalusd
            else:
                if registro.idcuenta_id[:2] == "00":
                    total_cobro_pesos += registro.importe
                    total_cobro_usd += registro.importe / registro.cot_usd_par
                else:
                    total_costo_pesos += registro.importe
                    total_costo_usd += registro.importe / registro.cot_usd_par

        resultado_pesos = total_cobro_pesos - total_costo_pesos
        resutado_usd = total_cobro_usd - total_costo_usd
        utilidad = resultado_pesos / total_cobro_pesos * 100

        d = {
            str(crianza.idcrianza): {
                "fini": crianza.fechainicio,
                "ffin": crianza.fechahasta,
                "dias": (crianza.fechahasta - crianza.fechainicio).days + 1,
                "faenado": crianza.faenado,
                "totalpesos": resultado_pesos,
                "totalusd": resutado_usd,
                "utilidad": utilidad,
                "precioxpollo_pesos": total_cobro_pesos / crianza.faenado,
                "costoxpollo_pesos": total_costo_pesos / crianza.faenado,
            }
        }
        resultados.update(d)

    modo = (
        "RESULTADOS por lo DEVENGADO" if tipo == "d" else "RESULTADOS por lo PERCIBIDO"
    )
    total = {"modo": modo}

    return render(
        request,
        "Resultados/resultados.html",
        {"resultados": resultados, "total": total},
    )


def resultadosxcrianza(request, id):

    request.session["idcrianza"] = id
    tipo = request.session.get("tipo")
    modo = (
        "RESULTADOS por lo DEVENGADO" if tipo == "d" else "RESULTADOS por lo PERCIBIDO"
    )

    crianza = Crianza.objects.get(pk=id)
    filtro = armar_filtro1(tipo, crianza.fechainicio, crianza.fechahasta)
    registros = RegistroContable.objects.filter(
        (
            (Q(idcuenta__gt="00.00") & Q(idcuenta__lt="00.04"))
            |
            (
                (Q(idcuenta__gt="01.00") & Q(idcuenta__lt="06.00"))
                & (~Q(idcuenta="03.05") & ~Q(idcuenta="03.98"))
            )
            |
            (Q(idcuenta__gt="06.00") & Q(idcuenta__lt="07.00"))

        )
    ).filter(filtro)

    ingresospesos = 0.0
    ingresosusd = 0.0
    egresospesos = 0.0
    egresosusd = 0.0
    inversionespesos = 0.0
    inversionesusd = 0.0
    ctas = []

    for registro in registros:
        if tipo == "d":
            dias = calculo_dias(
                registro.aplicadesde,
                registro.aplicahasta,
                crianza.fechainicio,
                crianza.fechahasta,
            )
            aplicadias = (registro.aplicahasta - registro.aplicadesde).days + 1
            subtotalpesos = dias / aplicadias * registro.importe
        else:
            subtotalpesos = registro.importe

        if str(registro.idcuenta)[:2] > "05":
            inversionespesos += subtotalpesos
            inversionesusd += subtotalpesos / registro.cot_usd_par
            cta = str(registro.idcuenta)
        elif str(registro.idcuenta)[:2] > "00":
            egresospesos += subtotalpesos
            egresosusd += subtotalpesos / registro.cot_usd_par
            cta = str(registro.idcuenta)[:2] + ".00"
        else:
            ingresospesos += subtotalpesos
            ingresosusd += subtotalpesos / registro.cot_usd_par
            cta = str(registro.idcuenta)

        columna = [fila[0] for fila in ctas]
        if cta in columna:
            idxc = columna.index(cta)
            ctas[idxc][2] += subtotalpesos
            ctas[idxc][3] += subtotalpesos / registro.cot_usd_par
        else:
            cuenta = Cuenta.objects.get(pk=cta)
            ctas.append(
                [
                    str(cuenta.idcuenta),
                    cuenta.cuenta,
                    subtotalpesos,
                    subtotalpesos / registro.cot_usd_par,
                ]
            )

    ctas.sort()

    dicingreso = {}
    dicctas = {}
    dicinversion = {}
    for cta in ctas:
        if str(cta[0])[:2] > "05":
            importe = inversionespesos
        elif str(cta[0])[:2] > "00":
            importe = egresospesos
        else:
            importe = ingresospesos
        d = {
            cta[1]: {
                "imppesos": cta[2],
                "impusd": cta[3],
                "porcparti": cta[2] / importe * 100,
            }
        }
        if str(cta[0])[:2] > "05":
            dicinversion.update(d)
        elif str(cta[0])[:2] > "00":
            dicctas.update(d)
        else:
            dicingreso.update(d)

    resultado = {
        "tipo": tipo,
        "modo": modo,
        "crianza": id,
        "fini": crianza.fechainicio,
        "ffin": crianza.fechahasta,
        "dias": (crianza.fechahasta - crianza.fechainicio).days + 1,
        "faenado": crianza.faenado,
        "ingrpesos": ingresospesos,
        "ingrusd": ingresosusd,
        "preciopesos": ingresospesos / crianza.faenado,
        "preciousd": ingresosusd / crianza.faenado,
        "egrepesos": egresospesos,
        "egreusd": egresosusd,
        "costopesos": egresospesos / crianza.faenado,
        "costousd": egresosusd / crianza.faenado,
        "resupesos": ingresospesos - egresospesos,
        "resuusd": ingresosusd - egresosusd,
        "porcutil": (ingresospesos - egresospesos) / ingresospesos * 100,
        "invpesos": inversionespesos,
        "invusd": inversionesusd,
    }

    return render(
        request,
        "Resultados/resultadosxcrianza.html",
        {
            "dicingreso": dicingreso,
            "dicctas": dicctas,
            "dicinversion": dicinversion,
            "resultado": resultado,
        },
    )


def armar_filtro1(tipo, fechainicio, fechahasta):

    query = Q()
    if tipo == "d":
        query &= (
            (Q(aplicadesde__lt=fechainicio) & Q(aplicahasta__gt=fechahasta))
            | (Q(aplicadesde__gte=fechainicio) & Q(aplicadesde__lte=fechahasta))
            | (Q(aplicahasta__gte=fechainicio) & Q(aplicahasta__lte=fechahasta))
        )
    else:
        query &= Q(fecha__gte=fechainicio) & Q(fecha__lte=fechahasta)

    return query


def calculo_dias(aplicadesde, aplicahasta, fechainicio, fechahasta):

    if aplicahasta > fechahasta:
        f1 = fechahasta
    else:
        f1 = aplicahasta
    if aplicadesde < fechainicio:
        f2 = fechainicio
    else:
        f2 = aplicadesde

    return (f1 - f2).days + 1
