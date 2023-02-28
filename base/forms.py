from django import forms
from django.core.validators import FileExtensionValidator
import pandas
import numpy as np
from django.core.exceptions import ValidationError
class FormLixiviacion(forms.Form):
    Granulometría = forms.FloatField(min_value=5, max_value=20)
    Tasa_de_Riego = forms.FloatField(min_value=5,max_value=20)
    Ácido_Total_Añadido = forms.FloatField(min_value=2, max_value=30)
    Altura_Pila = forms.FloatField(min_value=1,max_value=5)
    Ley_Cu_Total = forms.FloatField(min_value=0.5,max_value=2)
    Ley_CO3 = forms.FloatField(min_value=0.1, max_value=10)
    Ratio_Lixiviado = forms.FloatField(min_value=0, max_value=5)
    Dias_Operación = forms.FloatField(min_value=1)
    Cu_Soluble = forms.FloatField(min_value=50, max_value=90)

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
    jg = forms.FloatField(min_value=0.1, max_value=3)
    d32 = forms.FloatField(min_value=0.2, max_value=5)
    eg = forms.FloatField(min_value=2, max_value=30)
    jl = forms.FloatField(min_value=0, max_value=2)
    diámetro_Columna = forms.FloatField(min_value=3, max_value=50)
    densidad_Pulpa = forms.FloatField(min_value=0.9, max_value=1.2)
    densidad_Burbuja = forms.FloatField(min_value=0.0009, max_value=0.0015)
    viscosidad = forms.FloatField(min_value=0.0008, max_value=0.002)
    espumante = forms.ChoiceField(choices=espumantes)
    ppm = forms.FloatField(min_value=2, max_value=150)

class excelFlotationForm(forms.Form):
    archivo = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=["xlsx"])] , required=True)
    #validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
