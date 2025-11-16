from django.contrib import admin
from .models import Aporte
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class AporteAdmin(admin.ModelAdmin):
    list_display = [
        "idsocio",
        "fecha",
        "importe",
        "moneda",
        "cot_usd_ofi",
        "cot_usd_par",
    ]
    actions = [
        "actualizar_cotizacion_dolar_blue",
        "actualizar_cotizacion_dolar_oficial",
    ]

    def actualizar_cotizacion_dolar_blue(self, request, queryset):
        ruta_json = os.path.join(BASE_DIR, 'dolar', 'blue.json')
        with open(ruta_json, 'r') as blue:
            datos = json.load(blue)

        aportes_sin_cotizacion = queryset.filter(cot_usd_par=0)
        for aporte_sin_cotizacion in aportes_sin_cotizacion:
            cot_dolar = 0
            encontre = False
            for dato in datos:
                if ordenar_fecha(dato[0], "I") == aporte_sin_cotizacion.fecha.strftime(
                    "%Y-%m-%d"
                ):
                    if aporte_sin_cotizacion.moneda == "D":
                        cot_dolar = dato[2].replace(",", ".")
                    else:
                        cot_dolar = dato[1].replace(",", ".")
                    encontre = True
                    break
                elif ordenar_fecha(dato[0], "I") < aporte_sin_cotizacion.fecha.strftime(
                    "%Y-%m-%d"
                ):
                    if aporte_sin_cotizacion.moneda == "D":
                        cot_dolar = dato[2].replace(",", ".")
                    else:
                        cot_dolar = dato[1].replace(",", ".")
                    break

            aporte_sin_cotizacion.cot_usd_par = float(cot_dolar)
            aporte_sin_cotizacion.save()
            if not encontre:
                print(
                    "No se encontró cotización del "
                    + aporte_sin_cotizacion.fecha.strftime("%d-%m-%Y")
                )

    def actualizar_cotizacion_dolar_oficial(self, request, queryset):
        ruta_json = os.path.join(BASE_DIR, 'dolar', 'oficial.json')
        with open(ruta_json, 'r') as oficial:
            datos = json.load(oficial)

        aportes_sin_cotizacion = queryset.filter(cot_usd_ofi=0)
        for aporte_sin_cotizacion in aportes_sin_cotizacion:
            cot_dolar = 0
            encontre = False
            for dato in datos:
                if ordenar_fecha(dato[0], "I") == aporte_sin_cotizacion.fecha.strftime(
                    "%Y-%m-%d"
                ):
                    if aporte_sin_cotizacion.moneda == "D":
                        cot_dolar = dato[2].replace(",", ".")
                    else:
                        cot_dolar = dato[1].replace(",", ".")
                    encontre = True
                    break
                elif ordenar_fecha(dato[0], "I") < aporte_sin_cotizacion.fecha.strftime(
                    "%Y-%m-%d"
                ):
                    if aporte_sin_cotizacion.moneda == "D":
                        cot_dolar = dato[2].replace(",", ".")
                    else:
                        cot_dolar = dato[1].replace(",", ".")
                    break

            aporte_sin_cotizacion.cot_usd_ofi = float(cot_dolar)
            aporte_sin_cotizacion.save()
            if not encontre:
                print(
                    "No se encontró cotización del "
                    + aporte_sin_cotizacion.fecha.strftime("%d-%m-%Y")
                )


def ordenar_fecha(f, orden):
    fin = f.find("/", 0)
    dia = f[:fin]
    if len(dia) < 2:
        dia = "0" + dia
    inicio = fin + 1
    fin = f.find("/", inicio)
    mes = f[inicio:fin]
    if len(mes) < 2:
        mes = "0" + mes
    inicio = fin + 1
    año = f[inicio:]
    if orden == "N":
        return dia + "/" + mes + "/" + año
    else:
        return año + "-" + mes + "-" + dia


# Register your models here.
admin.site.register(Aporte, AporteAdmin)
