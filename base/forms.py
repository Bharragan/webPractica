from django import forms
from django.core.validators import FileExtensionValidator

class FormLixiviacion(forms.Form):
    Granulometria = forms.FloatField()
    Ratio_Irrigacion = forms.FloatField()
    Acido_Total_Añadido = forms.FloatField()
    Altura_Pila = forms.FloatField()
    Ley_Cu_Total = forms.FloatField()
    Ley_CO3 = forms.FloatField()
    Ratio_Lixiviado = forms.FloatField()
    Dias_Operacion = forms.FloatField()
    Cu_Soluble = forms.FloatField()

class excelFormLixiviacion(forms.Form):
    archivo = forms.FileField(validators = [FileExtensionValidator(allowed_extensions=["xlsx"])])
    