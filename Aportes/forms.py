from django import forms
from .models import Aporte


class AporteForm(forms.ModelForm):

    class Meta:
        model = Aporte
        fields = [
            "fecha",
            "idsocio",
            "importe",
            "moneda",
            "cot_usd_ofi",
            "cot_usd_par",
        ]

    def __init__(self, *args, **kwargs):
        super(AporteForm, self).__init__(*args, **kwargs)
        self.fields["idsocio"].widget.attrs.update({"class": "form-control"})
        self.fields["fecha"].widget = forms.DateInput(
            attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
        )
        self.fields["importe"].widget.attrs.update({"class": "form-control"})
        self.fields["moneda"].widget = forms.Select(
            attrs={"class": "form-control"}, choices={"D": "U$S", "P": "$"}
        )
        self.fields["cot_usd_ofi"].widget.attrs.update({"class": "form-control"})
        self.fields["cot_usd_par"].widget.attrs.update({"class": "form-control"})
