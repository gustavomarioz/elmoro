from django import forms
from ResumenGral.models import Crianza


class RepartoForm(forms.Form):

    idcrianza = forms.ModelChoiceField(
        label="Crianza",
        queryset=Crianza.objects.filter(idcrianza__gte=17).order_by("-idcrianza"),
    )
    fecha = forms.DateField(label="Fecha")
    importe = forms.FloatField(label="Importe", min_value=0.01, max_value=999999999.99)
    cot_usd_ofi = forms.FloatField(
        label="Cotización U$S oficial", min_value=0.001, max_value=99999.99
    )
    cot_usd_par = forms.FloatField(
        label="Cotización U$S paralelo", min_value=0.001, max_value=99999.99
    )
