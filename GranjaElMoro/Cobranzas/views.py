from django.shortcuts import render
from ResumenGral.models import Crianza
from RegistroContable.models import RegistroContable, Cuenta
from django.db.models import Q

# Create your views here.


def cobranzas(request, tipo):

    request.session["tipo"] = tipo

    cobros = {}
    crianzas = Crianza.objects.filter(idcrianza__gt=16)

    for crianza in crianzas:
        totalpesos = 0.0
        totalusd = 0.0

        filtro = armar_filtro(tipo, crianza.fechainicio, crianza.fechahasta)

        registros = RegistroContable.objects.filter(
            (Q(idcuenta__gt="00.00") & Q(idcuenta__lt="00.04"))
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
                totalpesos += subtotalpesos
                subtotalusd = subtotalpesos / registro.cot_usd_par
                totalusd += subtotalusd
            else:
                totalpesos += registro.importe
                totalusd += registro.importe / registro.cot_usd_par

        cobroxpollopesos = totalpesos / crianza.faenado
        cobroxpollousd = totalusd / crianza.faenado

        d = {
            str(crianza.idcrianza): {
                "fini": crianza.fechainicio,
                "ffin": crianza.fechahasta,
                "faenado": crianza.faenado,
                "totalpesos": totalpesos,
                "totalusd": totalusd,
                "cobroxpollopesos": cobroxpollopesos,
                "cobroxpollousd": cobroxpollousd,
            }
        }
        cobros.update(d)

        modo = (
            "COBRANZAS por lo DEVENGADO"
            if tipo == "d"
            else "COBRANZAS por lo PERCIBIDO"
        )
        total = {"modo": modo}

    return render(
        request, "Cobranzas/cobranzas.html", {"cobros": cobros, "total": total}
    )


def cobrosxcrianza(request, id):

    tipo = request.session.get("tipo")
    modo = "COBRANZAS por lo DEVENGADO" if tipo == "d" else "COBRANZAS por lo PERCIBIDO"

    request.session["idcrianza"] = id

    crianza = Crianza.objects.get(pk=id)

    filtro = armar_filtro(tipo, crianza.fechainicio, crianza.fechahasta)

    registros = RegistroContable.objects.filter(
        ((Q(idcuenta__gt="00.00") & Q(idcuenta__lt="00.04")))
    ).filter(filtro)

    cuentashija = []
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

        encontre = False
        for cuentahija in cuentashija:
            if cuentahija[0] == str(registro.idcuenta):
                cuentahija[2] += subtotalpesos
                cuentahija[3] += subtotalpesos / registro.cot_usd_par
                encontre = True

        if not encontre:
            cuenta = Cuenta.objects.get(pk=registro.idcuenta)
            cuentashija.append(
                [
                    str(registro.idcuenta),
                    cuenta.cuenta,
                    subtotalpesos,
                    subtotalpesos / registro.cot_usd_par,
                ]
            )
    cuentashija.sort()

    ctashija = {}
    totalctamadrepesos = 0.0
    totalctamadreusd = 0.0
    for cuentahija in cuentashija:
        totalctamadrepesos += cuentahija[2]
        totalctamadreusd += cuentahija[3]
        d = {
            cuentahija[1]: {
                "idcuenta": cuentahija[0],
                "importepesos": cuentahija[2],
                "cobroxpollopesos": cuentahija[2] / crianza.faenado,
                "importeusd": cuentahija[3],
                "cobroxpollousd": cuentahija[3] / crianza.faenado,
            }
        }
        ctashija.update(d)

    totalcobroxpollopesos = totalctamadrepesos / crianza.faenado
    totalcobroxpollousd = totalctamadreusd / crianza.faenado

    total = {
        "tipo": tipo,
        "modo": modo,
        "crianza": id,
        "totalpesos": totalctamadrepesos,
        "totalcobroxpollopesos": totalcobroxpollopesos,
        "totalusd": totalctamadreusd,
        "totalcobroxpollousd": totalcobroxpollousd,
    }

    return render(
        request,
        "Cobranzas/cobrosxcrianza.html",
        {"ctashija": ctashija, "total": total},
    )


def cobrosxcuenta(request, idcuenta):

    tipo = request.session.get("tipo")
    modo = "COBRANZAS por lo DEVENGADO" if tipo == "d" else "COBRANZAS por lo PERCIBIDO"

    cuenta = Cuenta.objects.get(pk=idcuenta)
    cuentahija = cuenta.cuenta

    idcrianza = request.session.get("idcrianza")
    crianza = Crianza.objects.get(pk=idcrianza)

    filtro = armar_filtro(tipo, crianza.fechainicio, crianza.fechahasta)

    registros = (
        RegistroContable.objects.filter(idcuenta_id=idcuenta)
        .filter(filtro)
        .order_by("fecha")
    )

    cuentas = {}
    totalcuentapesos = 0
    totalcuentausd = 0

    for registro in registros:
        subtotalpesos = registro.importe
        totalcuentapesos += subtotalpesos
        totalcuentausd += subtotalpesos / registro.cot_usd_par

        d = {
            registro.idregistro: {
                "fecha": registro.fecha,
                "descri": registro.descripcion,
                "totpesos": subtotalpesos,
                "totusd": subtotalpesos / registro.cot_usd_par,
            }
        }
        cuentas.update(d)

    total = {
        "tipo": tipo,
        "modo": modo,
        "crianza": idcrianza,
        "cuentahija": cuentahija,
        "totalpesos": totalcuentapesos,
        "totalusd": totalcuentausd,
    }

    return render(
        request,
        "Cobranzas/cobrosxcuenta.html",
        {"cuentas": cuentas, "total": total},
    )


def armar_filtro(tipo, fechainicio, fechahasta):

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
