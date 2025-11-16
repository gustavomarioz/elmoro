from django.db import models
from ResumenGral.models import Crianza

# Create your models here.


class Reparto(models.Model):
    idreparto = models.AutoField(primary_key=True)
    idcrianza = models.ForeignKey(
        Crianza,
        verbose_name="Crianza",
        on_delete=models.CASCADE,
    )
    fecha = models.DateField(verbose_name="Fecha")
    importe = models.FloatField(verbose_name="Importe", default=0)
    cot_usd_ofi = models.FloatField(verbose_name="Cotización U$S oficial", default=0)
    cot_usd_par = models.FloatField(verbose_name="Cotización U$S blue", default=0)
    cuota = models.FloatField(verbose_name="Cuota de participación Reparto", default=0)

    class Meta:
        verbose_name = "reparto"
        verbose_name_plural = "repartos"
        db_table = "reparto"
        ordering = ["-idcrianza"]

    def total_usds_oficiales(self):
        if self.cot_usd_ofi > 0.0:
            return round(self.importe / self.cot_usd_ofi, 2)
        else:
            return 0

    def total_usds_paralelos(self):
        if self.cot_usd_par > 0.0:
            return round(self.importe / self.cot_usd_par, 2)
        else:
            return 0

    def total_usds_promedio(self):
        if self.cot_usd_ofi > 0.0:
            if self.cot_usd_par > 0.0:
                return round(
                    self.importe / ((self.cot_usd_ofi + self.cot_usd_par) / 2), 2
                )
            else:
                return 0
        else:
            return 0

    def __str__(self):
        return (
            "Crianza: "
            + str(self.idcrianza)
            + "-"
            + "Fecha: "
            + str(self.fecha)
            + "-"
            + "Importe $: "
            + str(self.importe)
            + "-"
            + "Cotiz. u$s oficial: "
            + str(self.cot_usd_ofi)
            + "-"
            + "Cotiz. u$s blue: "
            + str(self.cot_usd_par)
        )


class Socio(models.Model):
    idsocio = models.AutoField(primary_key=True)
    socio = models.CharField(verbose_name="Socio", max_length=10)
    porcentaje = models.FloatField(verbose_name="Porcentaje")

    class Meta:
        verbose_name = "socio"
        verbose_name_plural = "socios"
        db_table = "socio"
        ordering = ["-porcentaje"]

    def __str__(self):
        return str(self.socio)
