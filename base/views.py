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
    {'id':1, 'name':'Proceso de lixiviacion'},
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
    datos=[]
    form = forms.FormLixiviacion()
    excelForm = forms.excelFormLixiviacion
    
    if request.method == 'GET':
        render(request, 'base/lixiviacion.html', {'form': form, 'excelForm': excelForm})
    
    elif request.method == 'POST':
        if 'submit_input' in request.POST:
            form = forms.FormLixiviacion(request.POST)
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    datos.append(value)
                context = {'datos':randomForestLix(datos)}
                return render(request, 'base/lixResult.html', context)
        elif 'submit_excel' in request.POST:
            excelForm = forms.excelFormLixiviacion(request.POST, request.FILES)
            
            try:
                datosExcelDf = pandas.read_excel(request.FILES['archivo'], sheet_name = 'Hoja1', usecols =['Granulometria','RatioIrrigacion','AcidoTotalAñadido', 'AlturaPila', 'LeyCuTotal', 'LeyCO3', 'RatioLixiviado', 'DiasOperacion', 'CuSoluble'])
                for i in range(8):
                    if np.isnan(datosExcelDf.iat[0,i]):
                        return render(request, 'base/lixiviacion.html', {'excelError': 'Excel con valores'})
                for i in range(8):
                    datos.append(datosExcelDf.iat[0,i])
                context = {'datos': randomForestLix(datos)}
                return render(request, 'base/lixResult.html', context)
            except:
                excelForm = forms.excelFormLixiviacion()
                return render(request, 'base/lixiviacion.html', {'excelError': 'Excel inválido o no seleccionado', 'form': form, 'excelForm': excelForm})

    return render(request, 'base/lixiviacion.html', {'form': form, 'excelForm': excelForm})

def downloadLix(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['X1','X2','X3','X4','X5','X6','X7','X8','X9'])
    response['Content-Disposition']='attachment; filename="LixExample.csv"'
    return response

def lix_Prediction(request):
    
    return render(request, 'base/lixResult.html')

def randomForestLix(datos):
    recomendacion = ""

    if(datos[0] > 13.250 and datos[0] < 13.866):
        if(datos[7] > 73.500):
            if(datos[6] < 2.604):
                recomendacion += "Según estos datos se puede alcanzar valores de recolección alta si se aumenta X7 en: " + str(2.604 - datos[6]) + " unidades. \n"
            elif(datos[6] > 4.370):
                recomendacion += "Se puede bajar X7 un poco para ahorrar ácido, habría que disminuirlo " +str(datos[6] - 4.370) + " unidades. \n"
            else:
                recomendacion += "No hay que modificar ningún valor, la pila va en camino a una recuperacion alta."
        
        elif(datos[7] < 73.500):
            if(datos[6] < 2.604):
                recomendacion += "Según estos datos se puede alcanzar valores de recolección alta si se aumenta X7 en: " + str(2.604 - datos[6]) + " unidades al llegar al día 74. \n"
            if(datos[6] > 4.370):
                recomendacion += "Se puede bajar X7 un poco para ahorrar ácido, habría que disminuirlo " +str(datos[6] - 4.370) + " unidades al llegar al día 74. \n"
            else:
                recomendacion += "No hay que modificar ningún valor, solo hay que esperar al día 74 y la recuperación empezará a ser alta"
    else:
        if(datos[7] < 73.500 and datos[7] > 40):
            if(datos[6] < 2.032):
                recomendacion += "Es complicado tener recuperaciones altas debido a los pocos días de operación, pero si aumentamos X7 en " + str(2.032 - datos[6]) + " unidades se tendrá una recuperacion media y a partir del día 74 hay que aumentar x7 en " + str(2.604 - (2.032 + (2.032 - datos[6]))) + " unidades \n"
            if(datos[6] > 2.032 and datos[6] < 2.604): 
                recomendacion += "Con estas características se obtendrán valores medios, lo ideal es que cuando se esté llegando al día 74 se aumente x7 en " + str(2.604 - datos[6]) + " y llegar hasta un máximo de 4.370 de x7 \n"
            if(datos[6] > 2.604 and datos[6] < 4.370): 
                recomendacion += "Con estas características se podría perder mucho ácido, la pila está en días de recuperación media, sería mejor bajar el valor un " + str(datos[6] - 2.604) + " unidades y retomar ese nivel de x7 en el día 74 de operación. \n"
            else:
                recomendacion += "Con estas características lo mejor sería bajar x7 un " + str(datos[6] - 2.604) + " unidades"

        if (datos[7] < 40):
            if(datos[6] < 2.032):
                recomendacion += "Con estos valores se tendrá una recuperación baja, si sube x7 en: " + str(2.032 - datos[6]) + " unidades obtendrá una recuperación media después al día 40 de operación y a partir del día 74 hay que aumentar x7 en " + str(2.604 - (2.032 + (datos[6] - 2.032))) + " unidades \n" 


        if(datos[7] > 73.500):
            if(datos[6] < 2.604):
                recomendacion += "Según estos datos se puede alcanzar valores de recolección alta si se aumenta X7 en: " + str(2.604 - datos[6]) + " unidades. \n"
            elif(datos[6] > 4.370):
                recomendacion += "Se puede bajar X7 un poco para ahorrar ácido, habría que disminuirlo " +str(datos[6] - 4.370) + " unidades. \n"
            else:
                recomendacion += "No hay que modificar ningún valor, la pila va en camino a una recuperacion alta."
    return recomendacion

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