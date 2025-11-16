from django import forms
from .models import Gas


class GasForm(forms.ModelForm):

    class Meta:
        model = Gas
        fields = [
            "idcrianza",
            "m3_medidor",
            "m3_9300_cal",
            "total_pesos",
            "cot_usd_par",
        ]

    def __init__(self, *args, **kwargs):
        super(GasForm, self).__init__(*args, **kwargs)
        self.fields["idcrianza"].widget.attrs.update({"class": "form-control"})
        self.fields["m3_medidor"].widget.attrs.update({"class": "form-control"})
        self.fields["m3_9300_cal"].widget.attrs.update({"class": "form-control"})
        self.fields["total_pesos"].widget.attrs.update({"class": "form-control"})
        self.fields["cot_usd_par"].widget.attrs.update({"class": "form-control"})
