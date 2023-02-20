from django import forms
from django.core.validators import FileExtensionValidator

class FormLixiviacion(forms.Form):
    Granulometria = forms.FloatField()
    RatioIrrigacion = forms.FloatField()
    AcidoTotalAnadido = forms.FloatField()
    AlturaPila = forms.FloatField()
    LeyCuTotal = forms.FloatField()
    LeyCO3 = forms.FloatField()
    RL = forms.FloatField()
    DiasOperacion = forms.FloatField()
    CuSoluble = forms.FloatField()

class excelFormLixiviacion(forms.Form):
    archivo = forms.FileField(validators = [FileExtensionValidator(allowed_extensions=["xlsx"])])
    