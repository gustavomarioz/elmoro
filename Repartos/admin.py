from django.contrib import admin
from .models import Reparto, Socio
import requests
import datetime


class RepartoAdmin(admin.ModelAdmin):
    list_display = [
        "idcrianza_id",
        "fecha",
        "importe",
        "cot_usd_ofi",
        "cot_usd_par",
    ]
    actions = ["actualizar_cotizacion_dolar_blue"]

    def actualizar_cotizacion_dolar_blue(self, request, queryset):
        repartos_sin_cotizacion = queryset.filter(cot_usd_par=0)
        for reparto_sin_cotizacion in repartos_sin_cotizacion:
            hasta_mas_uno = reparto_sin_cotizacion.fecha + datetime.timedelta(days=1)
            url = (
                "https://mercados.ambito.com//dolar/informal/historico-general/"
                + str(reparto_sin_cotizacion.fecha)
                + "/"
                + str(hasta_mas_uno)
            )
            respuesta = requests.get(url)
            if len(respuesta.json()) > 1:
                cot_usd = respuesta.json()[1][2].replace(",", ".")
                reparto_sin_cotizacion.cot_usd_par = float(cot_usd)
                reparto_sin_cotizacion.save()


class SocioAdmin(admin.ModelAdmin):
    list_display = [
        "idsocio",
        "socio",
        "porcentaje",
    ]


# Register your models here.
admin.site.register(Reparto, RepartoAdmin)
admin.site.register(Socio, SocioAdmin)
