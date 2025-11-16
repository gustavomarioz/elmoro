from django.contrib import admin
from .models import RegistroContable
import os
import json

class RegistroContableAdmin(admin.ModelAdmin):

    def admin_fecha(self, obj):
        return obj.fecha.strftime("%d/%m/%Y")

    def admin_aplicadesde(self, obj):
        return obj.aplicadesde.strftime("%d/%m/%Y")

    def admin_aplicahasta(self, obj):
        return obj.aplicahasta.strftime("%d/%m/%Y")

    list_display = [
        "periodo",
        "naturaleza",
        "transaccion",
        "idregistro",
        "idcuenta",
        "admin_fecha",
        "cot_usd_par",
        "descripcion",
        "importe",
        "admin_aplicadesde",
        "admin_aplicahasta",
        "tipo",
    ]

    actions = [
        "actualizar_cotizacion_dolar_blue",
    ]

    def actualizar_cotizacion_dolar_blue(self, request, queryset):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_json = os.path.join(BASE_DIR, 'dolar', 'blue.json')
        with open(ruta_json, 'r') as blue:
            datos = json.load(blue)

        registroscontables_sin_cotizacion = queryset.filter(cot_usd_par=0)
        for registrocontable_sin_cotizacion in registroscontables_sin_cotizacion:
            cot_dolar = 0
            encontre = False
            for dato in datos:
                fecha_inversa = ordenar_fecha(dato[0], "I")
                if fecha_inversa == registrocontable_sin_cotizacion.fecha.strftime(
                    "%Y-%m-%d"
                ):
                    cot_dolar = dato[2].replace(",", ".")
                    encontre = True
                    break
                elif fecha_inversa < registrocontable_sin_cotizacion.fecha.strftime(
                    "%Y-%m-%d"
                ):
                    cot_dolar = dato[2].replace(",", ".")
                    break

            registrocontable_sin_cotizacion.cot_usd_par = float(cot_dolar)
            registrocontable_sin_cotizacion.save()
            if not encontre:
                print(
                    "No se encontró cotización del "
                    + registrocontable_sin_cotizacion.fecha.strftime("%d-%m-%Y")
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
admin.site.register(RegistroContable, RegistroContableAdmin)
