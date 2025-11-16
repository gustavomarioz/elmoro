from django.db import models
from Repartos.models import Socio

# Create your models here.

tipo_choices = {
    "D": "U$S",
    "P": "$",
}


class Aporte(models.Model):
    idaporte = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(
        Socio,
        verbose_name="Socio",
        on_delete=models.CASCADE,
    )
    fecha = models.DateField(verbose_name="Fecha")
    importe = models.FloatField(verbose_name="Importe", default=0)
    moneda = models.CharField(
        verbose_name="Moneda", max_length=1, choices=tipo_choices, default="P"
    )
    cot_usd_ofi = models.FloatField(verbose_name="U$S oficial", default=0)
    cot_usd_par = models.FloatField(verbose_name="U$S blue", default=0)

    class Meta:
        verbose_name = "aporte"
        verbose_name_plural = "aportes"
        db_table = "aporte"
        ordering = ["-fecha"]

    def __str__(self):
        return (
            "Fecha: "
            + str(self.fecha)
            + "-"
            + "Socio: "
            + str(self.idsocio.socio)
            + "-"
            + "Importe: "
            + self.moneda
            + " "
            + str(self.importe)
            + "-"
            + "Cotiz. u$s oficial: "
            + str(self.cot_usd_ofi)
            + "-"
            + "Cotiz. u$s blue: "
            + str(self.cot_usd_par)
        )
