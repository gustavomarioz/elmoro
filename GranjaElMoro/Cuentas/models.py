from django.db import models

# Create your models here.


class Cuenta(models.Model):
    idcuenta = models.CharField(verbose_name="Cuenta", max_length=5, primary_key=True)
    cuenta = models.CharField(verbose_name="Descripcion", max_length=50)

    class Meta:
        verbose_name = "cuenta"
        verbose_name_plural = "cuentas"
        db_table = "cuenta"
        ordering = ["idcuenta"]

    def __str__(self):
        return self.idcuenta
