from django import forms
from django.core.validators import FileExtensionValidator
import pandas
import numpy as np
from django.core.exceptions import ValidationError
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
    
#De esta forma lo que se muestra sera el nombre del espumante y lo que se guardara es el valor numerico del mismo

espumantes = (
    (1, "DOW"),
    (2, "TEB"),
    (3, "MIBC"),
    (4, "F140"),
    (5, "F150"),
    (6, "F160-05"),
    (7, "F160-10"),
    (8, "F160-13"),
    (9, "F173"),
)

class FlotationForm(forms.Form):
    jg = forms.FloatField()
    d32 = forms.FloatField()
    eg = forms.FloatField()
    jl = forms.FloatField()
    diametro_Columna = forms.FloatField()
    densidad_Pulpa = forms.FloatField()
    densidad_Burbuja = forms.FloatField()
    viscosidad = forms.FloatField()
    espumante = forms.ChoiceField(choices=espumantes)
    ppm = forms.FloatField()

class excelFlotationForm(forms.Form):
    archivo = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=["xlsx"])] , required=True)
    #validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
