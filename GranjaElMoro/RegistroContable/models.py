from django.db import models
from Cuentas.models import Cuenta

# Create your models here.

naturaleza_choices = {
    0: "Eectivo",
    2: "Tarjeta de Crédito",
    4: "BAPRO",
}


class RegistroContable(models.Model):
    periodo = models.CharField(verbose_name="Período", max_length=6)
    naturaleza = models.IntegerField(
        verbose_name="Naturaleza", choices=naturaleza_choices
    )
    transaccion = models.IntegerField(verbose_name="Transacción")
    idregistro = models.AutoField(primary_key=True)
    idcuenta = models.ForeignKey(
        Cuenta, verbose_name="Cuenta", on_delete=models.CASCADE
    )
    fecha = models.DateField(verbose_name="Fecha")
    descripcion = models.CharField(verbose_name="Descripción", max_length=255)
    importe = models.FloatField(verbose_name="Importe")
    aplicadesde = models.DateField(verbose_name="Fecha Desde")
    aplicahasta = models.DateField(verbose_name="Fecha Hasta")
    tipo = models.CharField(verbose_name="Tipo", max_length=1)
    cot_usd_par = models.FloatField(verbose_name="Cotización U$S", default=0)

    class Meta:
        verbose_name = "registrocontable"
        verbose_name_plural = "registroscontable"
        db_table = "registrocontable"
        constraints = [
            models.UniqueConstraint(
                fields=["periodo", "naturaleza", "transaccion", "idregistro"],
                name="registro_contable_unico",
            )
        ]
        ordering = ["-periodo", "naturaleza", "transaccion", "idregistro"]

    def naturaleza_mvto(self):
        return naturaleza_choices[self.naturaleza]

    def __str__(self):
        return (
            self.periodo
            + "-"
            + self.naturaleza_mvto()
            + "-"
            + str(self.fecha)
            + "-"
            + str(self.idregistro)
            + "-"
            + str(self.idcuenta)
        )
