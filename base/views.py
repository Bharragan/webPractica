from django.shortcuts import render
from django.http import HttpResponse
import csv
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


def flot(request, pk):

    flot = None
    for i in flots:
        if i['id'] == int(pk):
            flot = i
    context = {'flot': flot}

    return render(request, 'base/flotacion.html', context )



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
                recomendacion += "Con estos valores se tendrá una recuperación baja, si sube x7 en: " + str(2.032 - datos[6]) + " unidades obtendrá una recuperación media después al día 40 de operación y a partir del día 74 hay que aumentar x7 en " + str(2.604 - (2.032 + (2.032 - datos[6]))) + " unidades \n" 


        if(datos[7] > 73.500):
            if(datos[6] < 2.604):
                recomendacion += "Según estos datos se puede alcanzar valores de recolección alta si se aumenta X7 en: " + str(2.604 - datos[6]) + " unidades. \n"
            elif(datos[6] > 4.370):
                recomendacion += "Se puede bajar X7 un poco para ahorrar ácido, habría que disminuirlo " +str(datos[6] - 4.370) + " unidades. \n"
            else:
                recomendacion += "No hay que modificar ningún valor, la pila va en camino a una recuperacion alta."
    return recomendacion