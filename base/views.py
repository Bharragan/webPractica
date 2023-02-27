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




def lix(request):
    datos=[]
    form = forms.FormLixiviacion()
    excelForm = forms.excelFormLixiviacion()
    
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
                for i in range(9):
                    if np.isnan(datosExcelDf.iat[0,i]):
                        return render(request, 'base/lixiviacion.html', {'excelError': 'Excel con valores'})
                for i in range(9):
                    datos.append(datosExcelDf.iat[0,i])
                context = {'datos': randomForestLix(datos)}
                return render(request, 'base/lixResult.html', context)
            except:
                excelForm = forms.excelFormLixiviacion()
                return render(request, 'base/lixiviacion.html', {'excelError': 'Excel inválido o no seleccionado', 'form': form, 'excelForm': excelForm})

    return render(request, 'base/lixiviacion.html', {'form': form, 'excelForm': excelForm})


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
            elif(datos[6] > 4.370):
                recomendacion += "Se puede bajar X7 un poco para ahorrar ácido, habría que disminuirlo " +str(datos[6] - 4.370) + " unidades al llegar al día 74. \n"
            else:
                recomendacion += "No hay que modificar ningún valor, solo hay que esperar al día 74 y la recuperación empezará a ser alta"
    else:
        if(datos[7] < 73.500 and datos[7] > 40):
            if(datos[6] < 2.032):
                recomendacion += "Es complicado tener recuperaciones altas debido a los pocos días de operación, pero si aumentamos X7 en " + str(2.032 - datos[6]) + " unidades se tendrá una recuperacion media y a partir del día 74 hay que aumentar x7 en " + str(2.604 - datos[6]) + " unidades \n"
            elif(datos[6] > 2.032 and datos[6] < 2.604): 
                recomendacion += "Con estas características se obtendrán valores medios, lo ideal es que cuando se esté llegando al día 74 se aumente x7 en " + str(2.604 - datos[6]) + " y llegar hasta un máximo de 4.370 de x7 \n"
            elif(datos[6] > 2.604 and datos[6] < 4.370): 
                recomendacion += "Con estas características se podría perder mucho ácido, la pila está en días de recuperación media, sería mejor bajar el valor un " + str(datos[6] - 2.604) + " unidades y retomar ese nivel de x7 en el día 74 de operación. \n"
            else:
                recomendacion += "Con estas características lo mejor sería bajar x7 un " + str(datos[6] - 2.604) + " unidades"

        elif (datos[7] < 40):
            if(datos[6] < 2.032):
                recomendacion += "Con estos valores se tendrá una recuperación baja, si sube x7 en: " + str(2.032 - datos[6]) + " unidades obtendrá una recuperación media después al día 40 de operación y a partir del día 74 hay que aumentar x7 en " + str(2.604 - datos[6]) + " unidades \n" 
            elif(datos[6] > 2.032 and datos[6] < 2.604):
                recomendacion += "Lo ideal sería bajar x7 un " + str(datos[6] - 2.032) + " hasta el día 40, a partir del día 40 devolver el valor a como estaba inicialmente y se obtendrá una recuperación media, luego al día 74 hay que mantener el valor de x7 por sobre " + str(2.604 - datos[6]) + " respecto al valor inicial"
            elif(datos[6] == 2.032):
                recomendación += "Mantener este valor hasta el día 74, luego aumentarlo en " + str(2.604 - datos[6])
            elif(datos[6] > 4.370):
                recomendacion += "Bajar el valor de x7 en " + str(datos[6] - 2.032) + " para los días previos al 74, luego en el día 74 lo ideal para una recuperación alta sería bajar el valor en " + str(datos[6] - 4.370) + " respecto al valor inicial"
            else:
                recomendacion += "Bajar el valor de x7 en " +str(datos[6] - 2.032) + " para los días previos al 74, luego en el día 74 lo ideal para una recuperación alta lo ideal sería bajar el valor de x7 en " + str(datos[6] - 3.5) + " respecto al valor inicial"

        else:
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
    recDict = {"inc":[],"dec":[],"keep":[],"k":"kappa"}
    #Bloque X1
    if(data[0] < 0.748):
        recDict['inc'].append("Aumentar el valor de Jg en " + str(0.748 - data[0]) + " unidades.")
        recomendacion += "Aumentar el valor de Jg en " + str(0.748 - data[0]) + " unidades. \n"
    else:
        recDict['keep'].append("Mantener este valor de Jg para una recuperacion alta.")
        recomendacion += "Mantener este valor de Jg para una recuperacion alta.\n"
    #Bloque X2
    if(data[1] >= 1.016 and data[1] <= 1.307):
        recDict['keep'].append("Mantener este valor de D32 para una recomendacion alta.")
        recomendacion += "Mantener este valor de D32 para una recomendacion alta.\n"
    elif(data[1] > 0.669 and data[1] < 1.016):
        recDict['inc'].append("Aumentar el valor de D32 en " + str(1.016 - data[1]) + " unidades. ")
        recomendacion += "Aumentar el valor de D32 en " + str(1.016 - data[1]) + " unidades. \n"
    else:
        if(data[1]>1.307):
            recDict['dec'].append("Disminuir el valor de D32 en" + str(data[1]-1.307) + " unidades.")
            recomendacion += "Disminuir el valor de D32 en" + str(data[1]-1.307) + " unidades. \n"
        else:
            recDict['inc'].append("Aumentar el valor de D32 en " + str(1.016 - data[1]) + " unidades.")
            recomendacion += "Aumentar el valor de D32 en " + str(1.016 - data[1]) + " unidades. \n"

    #Bloque X3
    if(data[2] >= 12.045):
        recDict['keep'].append("Mantener este valor de Eg para una recuperacion alta.")
        recomendacion += "Mantener este valor de Eg para una recuperacion alta. \n"
    else:
        recDict['inc'].append("Aumentar el valor de Eg en " + str(12.045 - data[2]) + " unidades.")
        recomendacion += "Aumentar el valor de Eg en " + str(12.045 - data[2]) + " unidades. \n"

    #Bloque X4
    if(data[3] >= 0.935):
        recDict['keep'].append("Mantener este valor de Jl para una recuperacion alta.")
        recomendacion += "Mantener este valor de Jl para una recuperacion alta. \n"
    else:
        recDict['inc'].append("Aumentar el valor de Jl en" + str(0.935 - data[3]) + " unidades.")
        recomendacion += "Aumentar el valor de Jl en" + str(0.935 - data[3]) + " unidades. \n"

    if(data[8] in [5,8,3,2]):
        recDict['keep'].append("Este espumante a resultado en recuperaciones altas se recomienda continuar con su uso.")
        recomendacion += "Este espumante a resultado en recuperaciones altas se recomienda continuar con su uso \n"
    else:
        recDict['inc'].append("Se recomienda cambiar el espumante a uno de los siguientes: F150, F160-13, MIBC, TEB.")
        recomendacion += "Se recomienda cambiar el espumante a uno de los siguientes: F150, F160-13, MIBC, TEB"

    #Bloque X10
    if(data[9] >= 12.500):
        recDict['keep'].append("Mantener este valor de Ppm para una recuperacion alta.")
        recomendacion += "Mantener este valor de Ppm para una recuperacion alta. \n"
    else:
        recDict['inc'].append("Aumentar el valor de Ppm en " + str(12.5-data[9]) + " unidades.")
        recomendacion += "Aumentar el valor de Ppm en " + str(12.5-data[9]) + " unidades. \n"
    return 