from django.shortcuts import render
from django.http import HttpResponse
import csv
import pandas
import numpy as np
from . import forms
# Create your views here.

flots = [
    {'id':1, 'name':'Proceso de flotacion parte 1'},
    {'id':2, 'name':'Proceso de flotacion parte 2'},
]
lixs = [
    {'id':1, 'name':'Proceso de lixiviacion parte 1'},
    {'id':2, 'name':'Proceso de lixiviacion parte 2'},
]

"""
procesos = [
    {'id':1, 'name':'Proceso de Flotación'},
    {'id':2, 'name':'Proceso de Lixiviación'},
]
"""

def home(request):
    context =  {'flots': flots, 'lixs':lixs}
    #context = {'procesos', proceso}
    return render(request, 'base/home.html', context)

def flot(request):
    data=[]
    form = forms.FlotationForm()
    excelForm = forms.excelFlotationForm()
    if request.method == 'GET':
            render(request, 'base/flotacion.html' ,{'form': form, 'excelForm':excelForm})
    elif request.method == 'POST':
        if 'submit_input' in request.POST:
            form = forms.FlotationForm(request.POST)
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    data.append(value)
                context = {'data':randomForestPrediction(data)}
                return render(request,'base/flotationResult.html',context)
        elif 'submit_excel' in request.POST:
            excelForm = forms.excelFlotationForm(request.POST, request.FILES)
            try:
                excel_data_df = pandas.read_excel(request.FILES['archivo'], sheet_name='Hoja1', usecols=['Jg', 'D32_medido','Eg','Jl','Dcolumna','Densidad pulpa','Densidad burbuja','Viscosidad','Espumante','ppm'])
                
                for i in range(10):
                    if np.isnan(excel_data_df.iat[0,i]):
                        return render(request, 'base/flotacion.html', {'excelError':'Excel con valores nulos','form': form, 'excelForm':excelForm})
                for i in range(10):
                    data.append(excel_data_df.iat[0, i])
                context = {'data':randomForestPrediction(data)}
                return render(request,'base/flotationResult.html',context)
            except:
                excelForm = forms.excelFlotationForm()
                return render(request, 'base/flotacion.html', {'excelError':'Excel Invalido o no seleccionado','form': form, 'excelForm':excelForm})
    return render(request, 'base/flotacion.html', {'form': form, 'excelForm':excelForm})


def lix(request, pk):

    lix = None
    for i in lixs:
        if i['id'] == int(pk):
            lix = i
    context = {'lix': lix}

    return render(request, 'base/lixiviacion.html', context)

def flotation_prediction(request):

    return render(request,'base/flotationResult')

def randomForestPrediction(data):
    recomendacion = ""
    #Bloque X1
    if(data[0] < 0.748):
        recomendacion += "Aumentar el valor de X1 en " + str(0.748 - data[0]) + " unidades. \n"
    else:
        recomendacion += "Mantener este valor de X1 para una recuperacion alta.\n"

    #Bloque X2
    if(data[1] >= 1.016 and data[1] <= 1.307):
        recomendacion += "Mantener este valor de X2 para una recomendacion alta.\n"
    elif(data[1] > 0.669 and data[1] < 1.016):
        recomendacion += "Aumentar el valor de X2 en " + str(1.016 - data[1]) + " unidades. \n"
    else:
        if(data[1]>1.307):
            recomendacion += "Disminuir el valor de X2 en" + str(data[1]-1.307) + " unidades. \n"
        else:
            recomendacion += "Aumentar el valor de X2 en " + str(1.016 - data[1]) + " unidades. \n"

    #Bloque X3
    if(data[2] >= 12.045):
        recomendacion += "Mantener este valor de X3 para una recuperacion alta. \n"
    else:
        recomendacion += "Aumentar el valor de X3 en " + str(12.045 - data[2]) + " unidades. \n"

    #Bloque X4
    if(data[3] >= 0.935):
        recomendacion += "Mantener este valor de X4 para una recuperacion alta. \n"
    else:
        recomendacion += "Aumentar el valor de X4 en" + str(0.935 - data[3]) + " unidades. \n"

    #Bloque X10
    if(data[9] >= 12.500):
        recomendacion += "Mantener este valor de X10 para una recuperacion alta. \n"
    else:
        recomendacion += "Aumentar el valor de X10 en " + str(12.5-data[9]) + " unidades. \n"
    return recomendacion