from django.db import models
from ResumenGral.models import Crianza

# Create your models here.


class Electricidad(models.Model):
    idcrianza = models.OneToOneField(
        Crianza, verbose_name="Crianza", on_delete=models.CASCADE, primary_key=True
    )
    activa_kwxh = models.FloatField(verbose_name="Energía Activa-Kw x H ")
    reactiva_kvar = models.FloatField(
        verbose_name="Energía ReActiva-Kvar", blank=True, null=True, default=0
    )
    perdida_kw = models.IntegerField(verbose_name="Pérdida en Kw")
    total_pesos = models.FloatField(verbose_name="Total pesos crianza", default=0)
    cot_usd_par = models.FloatField(verbose_name="Cotización U$S blue", default=0)

    class Meta:
        verbose_name = "electricidad"
        verbose_name_plural = "electricidad"
        db_table = "electricidad"
        ordering = ["idcrianza"]

    def total_usds_paralelos(self):
        if self.cot_usd_par > 0.0:
            return round(self.total_pesos / self.cot_usd_par, 2)
        else:
            return 0

    def __str__(self):
        return (
            "Crianza: "
            + str(self.idcrianza)
            + "-"
            + "Total $: "
            + str(self.total_pesos)
            + "-"
            + "Cotiz. u$s blue: "
            + str(self.cot_usd_par)
        )
