from django import forms
from .models import Electricidad


class LuzForm(forms.ModelForm):

    class Meta:
        model = Electricidad
        fields = [
            "idcrianza",
            "activa_kwxh",
            "reactiva_kvar",
            "perdida_kw",
            "total_pesos",
            "cot_usd_par",
        ]

    def __init__(self, *args, **kwargs):
        super(LuzForm, self).__init__(*args, **kwargs)
        self.fields["idcrianza"].widget.attrs.update({"class": "form-control"})
        self.fields["activa_kwxh"].widget.attrs.update({"class": "form-control"})
        self.fields["reactiva_kvar"].widget.attrs.update({"class": "form-control"})
        self.fields["perdida_kw"].widget.attrs.update({"class": "form-control"})
        self.fields["total_pesos"].widget.attrs.update({"class": "form-control"})
        self.fields["cot_usd_par"].widget.attrs.update({"class": "form-control"})
