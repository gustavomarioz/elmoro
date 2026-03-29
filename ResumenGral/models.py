from django.db import models
from decimal import Decimal

# Create your models here.

temporada_choices = {
    "I": "Invierno",
    "V": "Verano",
    "O": "Otoño/Prim.",
}


class Crianza(models.Model):
    idcrianza = models.IntegerField(
        verbose_name="Crianza", primary_key=True, unique=True, blank=False
    )
    temporada = models.CharField(
        verbose_name="Temporada",
        max_length=1,
        choices=temporada_choices,
        blank=True,
        null=True,
    )
    fechainicio = models.DateField(verbose_name="Fecha de Inicio")
    fechadesde = models.DateField(verbose_name="Fecha Desde")
    fechahasta = models.DateField(verbose_name="Fecha Hasta")
    metros2 = models.IntegerField(verbose_name="M2")
    ingresado = models.IntegerField(verbose_name="Total Ingresado")
    dias = models.FloatField(verbose_name="Duración", max_length=4)
    kgsalimento = models.IntegerField(verbose_name="kgs Alimento Consumido")
    faenado = models.IntegerField(verbose_name="Total Faenado")
    kgsfaenados = models.IntegerField(verbose_name="kgs Faenados")
    muertosfaena = models.IntegerField(verbose_name="Muertos en Faena")
    muertosgranja = models.IntegerField(verbose_name="Muertos en Granja")
    granjero = models.CharField(verbose_name="Granjero", max_length=20)
    fechafactura = models.DateField(verbose_name="Fecha Factura", blank=True, null=True)
    imagen = models.ImageField(
        verbose_name="Imagen",
        blank=True,
        null=True,
        upload_to="ResumenGral",
    )

    class Meta:
        verbose_name = "crianza"
        verbose_name_plural = "crianzas"
        db_table = "crianza"
        ordering = ["-idcrianza"]

    def temporada_crianza(self):
        return temporada_choices[self.temporada]

    def pollosxm2(self):
        pxm2 = self.ingresado / self.metros2
        return pxm2

    def peso(self):
        pesaje = self.kgsfaenados / self.faenado
        return pesaje

    def mortandad(self):
        porcmortandad = self.muertosfaena / self.ingresado * 100
        return porcmortandad

    def indicreci(self):
        pesoengs = self.kgsfaenados / self.faenado * 1000
        indice = pesoengs / self.dias
        return round(indice)

    def conversion(self):
        convers = self.kgsalimento / self.kgsfaenados
        return convers

    def fep(self):
        porcmortandad = self.muertosfaena / self.ingresado * 100
        pesaje = self.kgsfaenados / self.faenado
        convers = self.kgsalimento / self.kgsfaenados
        indice = (100 - porcmortandad) * pesaje / (convers * self.dias) * 100
        return indice

    def __str__(self):
        return str(self.idcrianza)


class DetalleDeCrianza(models.Model):
    iddetalle = models.AutoField(primary_key=True)
    crianza = models.ForeignKey(
        Crianza,
        verbose_name="Crianza",
        on_delete=models.CASCADE,
    )
    galpon = models.IntegerField(verbose_name="Galpón")
    fechadesdepromedio = models.DateField(verbose_name="Fecha Desde Promedio")
    ingresado = models.IntegerField(verbose_name="Neto Ingresado")
    fechahastapromedio = models.DateField(verbose_name="Fecha Hasta Promedio")
    faenado = models.IntegerField(verbose_name="Faenado")
    pollosxmetro2 = models.DecimalField(verbose_name="Pollos por m2", max_digits=3, decimal_places=1)
    dias = models.DecimalField(verbose_name="Edad", max_digits=3, decimal_places=1)
    totalagua = models.IntegerField(verbose_name="lts de Agua Consumida", default=0)
    kgsalimento = models.DecimalField(verbose_name="kgs de Alimento Consumido", max_digits=8, decimal_places=2)
    kgsfaenados = models.IntegerField(verbose_name="kgs Faenado")
    muertosgranja = models.IntegerField(verbose_name="Muertos en Granja")
    muertosfaena = models.IntegerField(verbose_name="Muertos en Faena")

    class Meta:
        verbose_name = "detalle de crianza"
        verbose_name_plural = "detalle de crianzas"
        db_table = "detalledecrianza"
        ordering = ["-crianza", "galpon"]

    def pesoxgalpon(self):
        pesaje = self.kgsfaenados / self.faenado
        return pesaje

    def mortandadfaenaxgalpon(self):
        porcmortandad = self.muertosfaena / self.ingresado * 100
        return porcmortandad

    def indicrecixgalpon(self):
        pesoengs = self.kgsfaenados / self.faenado * 1000
        indice = Decimal(str(pesoengs)) / self.dias
        return round(indice)

    def conversionxgalpon(self):
        convers = self.kgsalimento / self.kgsfaenados
        return convers

    def fepxgalpon(self):
        porcmortandad = self.muertosfaena / self.ingresado * 100
        pesaje = self.kgsfaenados / self.faenado
        convers = self.kgsalimento / self.kgsfaenados
        indice = Decimal(str((100 - porcmortandad) * pesaje)) / (convers * self.dias) * 100
        return indice

    def __str__(self):
        return "Crianza: " + str(self.crianza) + " Galpón: " + str(self.galpon)
