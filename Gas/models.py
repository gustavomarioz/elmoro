from django.db import models
from ResumenGral.models import Crianza

# Create your models here.


class Gas(models.Model):
    idcrianza = models.OneToOneField(
        Crianza, verbose_name="Crianza", on_delete=models.CASCADE, primary_key=True
    )
    m3_medidor = models.IntegerField(verbose_name="M3 del medidor")
    m3_9300_cal = models.FloatField(verbose_name="M3 de 9300 calorías", default=0)
    total_pesos = models.FloatField(verbose_name="Total pesos crianza", default=0)
    cot_usd_par = models.FloatField(verbose_name="Cotización U$S blue", default=0)

    class Meta:
        verbose_name = "gas"
        verbose_name_plural = "gas"
        db_table = "gas"
        ordering = ["idcrianza"]

    def total_usds_paralelos(self):
        if self.cot_usd_par > 0.0:
            return round(self.total_pesos / self.cot_usd_par, 2)
        else:
            return 0

    def relacion(self):
        return round(self.m3_9300_cal / self.m3_medidor, 2)

    def pesos_m3_medidor(self):
        return round(self.total_pesos / self.m3_medidor, 2)

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
