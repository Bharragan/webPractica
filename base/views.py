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

rangosFlotacion = {
    "value":[0,1,2,3,4,5,6,7,8,9],
    "min":[0.1,0.2,2,0,3,0.90,0.0009,0.0008,0,2],
    "max":[3,5,30,2,50,1.2,0.0015,0.002,11,150]
}


def home(request):
    context =  {'flots': flots, 'lixs':lixs}
    return render(request, 'base/home.html', context)

def flot(request):
    data=[]     #Inicializa un array donde iran las variables operacionales
    form = forms.FlotationForm()        #Se crean formularios vacios en caso de cargar la pagina por primera vez
    excelForm = forms.excelFlotationForm()
    if request.method == 'GET':
            render(request, 'base/flotacion.html' ,{'form': form, 'excelForm':excelForm}) #Si el metodo es GET se renderiza la pagina de forma normal
    elif request.method == 'POST':  
        if 'submit_input' in request.POST:      #Si el metodo es POST y el boton seleccionado contiene el nombre submit input entonces se asume que el formulario es el de ingreso manual
            form = forms.FlotationForm(request.POST)        #Se validan los datos obtenidos desde el formulario
            if form.is_valid():
                for key, value in form.cleaned_data.items():
                    data.append(value)                          #Se agregan los valores obtenidos del formulario al array de valores
                context = randomForestPrediction(data)          
                return render(request,'base/flotationResult.html',context)          #Se redirecciona a la vista resultados en conjunto de los datos obtenidos del analisis
        elif 'submit_excel' in request.POST:    #Si el metodo es POST y el boton contiene el nombre submit_excel se asuem que el formulario es de ingreso por archivo
            excelForm = forms.excelFlotationForm(request.POST, request.FILES)
            try:
                #Se intenta leer y obtener los datos desde excel , en caso de fallar se retorna un error.
                excel_data_df = pandas.read_excel(request.FILES['archivo'], sheet_name='Hoja1', usecols=['Jg', 'D32_medido','Eg','Jl','Dcolumna','Densidad pulpa','Densidad burbuja','Viscosidad','Espumante','ppm'])
                
                for i in range(10):
                    if np.isnan(excel_data_df.iat[0,i]):
                        return render(request, 'base/flotacion.html', {'excelError':'Excel con valores nulos.','form': form, 'excelForm':excelForm})
                for i in range(10):
                    if excel_data_df.iat[0, i]>rangosFlotacion['max'][i] or excel_data_df.iat[0, i]<rangosFlotacion['min'][i]:
                        return render(request,'base/flotacion.html', {'excelError':'Excel con valores fuera de rango.','form': form, 'excelForm':excelForm})
                    data.append(excel_data_df.iat[0, i])
                context = randomForestPrediction(data)
                return render(request,'base/flotationResult.html',context)
            except:
                excelForm = forms.excelFlotationForm()
                return render(request, 'base/flotacion.html', {'excelError':'Excel Inv??lido o no seleccionado.','form': form, 'excelForm':excelForm})
    return render(request, 'base/flotacion.html', {'form': form, 'excelForm':excelForm})




def lix(request):
    datos=[]    #Arreglo en donde se guardar??n las variables a utilizar
    rangos={    #Diccionario con los rangos para validaci??n con el Excel
        'value':[0,1,2,3,4,5,6,7,8],    #aqu?? estan las posiciones de las variables (0 es granulometr??a y sus valores min y max son 5 y 20 respectivamente)
        'min':[5,5,2,1,0.5,0.1,0,1,50],     #valores minimos de las variables
        'max':[20,20,30,5,2,10,5,150,90],    #valores m??ximos de las variables
    }
    form = forms.FormLixiviacion()  #Creaci??n de un formulario vac??o 
    excelForm = forms.excelFormLixiviacion()     #creaci??n de un formulario de excel vac??o 
    
    if request.method == 'GET':     #si el m??todo es un 'GET' esto va a mostrar la p??gina de forma normal con formularios vac??os
        render(request, 'base/lixiviacion.html', {'form': form, 'excelForm': excelForm})
    
    elif request.method == 'POST':      #si el m??todo es un 'POST' y hay un 'submit_input' esto indica que se ingresaron datos por teclado
        if 'submit_input' in request.POST:
            form = forms.FormLixiviacion(request.POST)      #Aqu?? se hacen las validaciones de min y max que est??n en el m??todo FomrLixiviacion dentro de forms.py
            if form.is_valid():     #Si se cumplieron las condiciones
                for key, value in form.cleaned_data.items():
                    datos.append(value)     #se agregan los valores al arreglo de variables 'datos' creado al inicio del m??todo
                context = {'datos':randomForestLix(datos)}   
                return render(request, 'base/lixResult.html', context)
        elif 'submit_excel' in request.POST:    #si el m??todo 'POST' tiene un 'submit_excel' esto indica que se ingresaron datos por el excel
            excelForm = forms.excelFormLixiviacion(request.POST, request.FILES)
            
            try:
                #Se leen los valores del excel y se guardan en un df, si por alg??n motivo no se puede leer, se retorna un error.
                datosExcelDf = pandas.read_excel(request.FILES['archivo'], sheet_name = 'Hoja1', usecols =['Granulometria','RatioIrrigacion','AcidoTotalA??adido', 'AlturaPila', 'LeyCuTotal', 'LeyCO3', 'RatioLixiviado', 'DiasOperacion', 'CuSoluble'])
                #Este for verifica que no hayan valores nulos
                for i in range(9):
                    if np.isnan(datosExcelDf.iat[0,i]):
                        return render(request, 'base/lixiviacion.html', {'excelError': 'Excel con valores inv??lidos o nulos', 'form': form, 'excelForm': excelForm})
                #Este for hace uso del diccionario para verificar que el excel cumpla con los rangos.
                for i in range(9):
                    if(datosExcelDf.iat[0,i] >= rangos['min'][i] and datosExcelDf.iat[0,i] <= rangos['max'][i]):
                        datos.append(datosExcelDf.iat[0,i])
                    else:
                        #Si no se cumple estas validaciones se recarga la p??gina mmostrando un mensaje de error
                        return render(request, 'base/lixiviacion.html', {'excelError': 'Uno de los valores est?? fuera de rango', 'form': form, 'excelForm': excelForm})
                
                context = {'datos': randomForestLix(datos)}
                return render(request, 'base/lixResult.html', context)
            except:
                excelForm = forms.excelFormLixiviacion()
                return render(request, 'base/lixiviacion.html', {'excelError': 'Excel inv??lido o no seleccionado', 'form': form, 'excelForm': excelForm})

    return render(request, 'base/lixiviacion.html', {'form': form, 'excelForm': excelForm})

def lix_Prediction(request):
    
    return render(request, 'base/lixResult.html')

"""
El sistema de recomendaci??n de lixiviaci??n funciona de tal forma que en base a algunas caracter??sticas dentro de la pila
se tendr??n recuperaciones bajas, altas o medias, las pilas de lixiviaci??n si bien tienen bastantes variables (9) muchas de 
estas no se pueden modificar y hay que aceptar que tienen ese valor, y si llegan a cambiar es por algo que est?? un poco fuera
de nuestro control, la granulometr??a, la altura de la pila, el carbonato, la ley de cobre total no se pueden cambiar, las dosis
de ??cido que circula por la pila y el a??adido como extra si se pueden, pero esto crea la proporci??n de lixiviado, por ende las 
recomendaciones est??n sujetas a ver bajo que condiciones renta tener un rango de esta proporci??n de lixiviado al ser el ??nico
valor real que se puede modificar y que afecta en gran medida. 

Las variables que afectan y que est??n siendo consideradas son las que m??s peso tienen en la predicci??n y son las siguientes:

datos[0] = granulometr??a
datos[6] = proporci??n de lixiviado
datos[7] = d??as de operaci??n
"""
def randomForestLix(datos):
    recomendacion = ""
    if(datos[0] > 13.250 and datos[0] < 13.866):
        if(datos[7] >= 73.500):
            if(datos[6] < 2.604):
                recomendacion += "Seg??n estos datos se puede alcanzar valores de recolecci??n alta si se aumenta la proporci??n de lixiviado en: " + str(round(2.604 - datos[6], 3)) + " unidades. \n"
            elif(datos[6] > 4.370):
                recomendacion += "Se puede bajar la proporci??n de lixiviado un poco para ahorrar ??cido, habr??a que disminuirlo en " +str(round(datos[6] - 4.370, 3)) + " unidades. \n"
            else:
                recomendacion += "No hay que modificar ning??n valor, la pila va en camino a una recuperacion alta."
        
        elif(datos[7] < 73.500):
            if(datos[6] < 2.604):
                recomendacion += "Seg??n estos datos se puede alcanzar valores de recolecci??n alta si se aumenta la proporci??n de lixiviado en: " + str(round(2.604 - datos[6], 3)) + " unidades al llegar al d??a 74. \n"
            elif(datos[6] > 4.370):
                recomendacion += "Se puede bajar la proporci??n de lixiviado un poco para ahorrar ??cido, habr??a que disminuirlo " +str(round(datos[6] - 4.370, 3)) + " unidades al llegar al d??a 74. \n"
            else:
                recomendacion += "No hay que modificar ning??n valor, solo hay que esperar al d??a 74 y la recuperaci??n empezar?? a ser alta"
    else:
        if(datos[7] < 73.500 and datos[7] >= 40):
            if(datos[6] < 2.032):
                recomendacion += "Es complicado tener recuperaciones altas debido a los pocos d??as de operaci??n, pero si aumentamos la proporci??n de lixiviado en " + str(round(2.032 - datos[6], 3)) + " unidades se tendr?? una recuperacion media y a partir del d??a 74 hay que aumentar la proporci??n de lixiviado en " + str(round(2.604 - datos[6], 3)) + " unidades \n"
            elif(datos[6] > 2.032 and datos[6] < 2.604): 
                recomendacion += "Con estas caracter??sticas se obtendr??n valores medios, lo ideal es que cuando se est?? llegando al d??a 74 se aumente la proporci??n de lixiviado en " + str(round(2.604 - datos[6], 3)) + " y llegar hasta un m??ximo de 4.370 de la proporci??n de lixiviado \n"
            elif(datos[6] > 2.604 and datos[6] < 4.370): 
                recomendacion += "Con estas caracter??sticas se podr??a perder mucho ??cido, la pila est?? en d??as de recuperaci??n media, ser??a mejor bajar el valor un " + str(round(datos[6] - 2.604, 3)) + " unidades y retomar ese nivel de la proporci??n de lixiviado en el d??a 74 de operaci??n. \n"
            else:
                recomendacion += "Con estas caracter??sticas lo mejor ser??a bajar la proporci??n de lixiviado un " + str(round(datos[6] - 2.604, 3)) + " unidades"

        elif (datos[7] < 40):
            if(datos[6] < 2.032):
                recomendacion += "Con estos valores se tendr?? una recuperaci??n baja, si sube la proporci??n de lixiviado en: " + str(round(2.032 - datos[6], 3)) + " unidades obtendr?? una recuperaci??n media despu??s al d??a 40 de operaci??n y a partir del d??a 74 hay que aumentar la proporci??n de lixiviado en " + str(round(2.604 - datos[6], 3)) + " unidades \n" 
            elif(datos[6] > 2.032 and datos[6] < 2.604):
                recomendacion += "Lo ideal ser??a bajar proporci??n de lixiviado un " + str(round(datos[6] - 2.032, 3)) + " hasta el d??a 40, a partir del d??a 40 devolver el valor a como estaba inicialmente y se obtendr?? una recuperaci??n media, luego al d??a 74 hay que mantener el valor de la proporci??n de lixiviado por sobre " + str(round(2.604 - datos[6], 3)) + " respecto al valor inicial"
            elif(datos[6] == 2.032):
                recomendaci??n += "Mantener este valor hasta el d??a 74, luego aumentarlo en " + str(round(2.604 - datos[6], 3))
            elif(datos[6] > 4.370):
                recomendacion += "Bajar el valor de la proporci??n de lixiviado en " + str(round(datos[6] - 2.032, 3)) + " para los d??as previos al 74, luego en el d??a 74 lo ideal para una recuperaci??n alta ser??a bajar el valor en " + str(round(datos[6] - 4.370, 3)) + " respecto al valor inicial"
            else:
                recomendacion += "Bajar el valor de la proporci??n de lixiviado en " +str(round(datos[6] - 2.032, 3)) + " para los d??as previos al 74, luego en el d??a 74 lo ideal para una recuperaci??n alta lo ideal ser??a bajar el valor de la proporci??n de lixiviado en " + str(round(datos[6] - 3.5, 3)) + " respecto al valor inicial"

        else:
            if(datos[6] < 2.604):
                recomendacion += "Seg??n estos datos se puede alcanzar valores de recolecci??n alta si se aumenta la proporci??n de lixiviado en: " + str(round(2.604 - datos[6], 3)) + " unidades. \n"
            elif(datos[6] > 4.370):
                recomendacion += "Se puede bajar la proporci??n de lixiviado un poco para ahorrar ??cido, habr??a que disminuirlo " +str(round(datos[6] - 4.370, 3)) + " unidades. \n"
            else:
                recomendacion += "No hay que modificar ning??n valor, la pila va en camino a una recuperacion alta."
    return recomendacion

def flotation_prediction(request):

    return render(request,'base/flotationResult')
#Metodo para crear recomendaciones en base a valores obtenidos en forma de array como parametro.
#Retorna un diccionario de arrays donde se tienen las recomendaciones separadas por categoria
def randomForestPrediction(data):
    recDict = {"inc":[],"dec":[],"keep":[]}
    #Bloque X1
    if(data[0] < 0.748):
        recDict['inc'].append("Aumentar el valor de Jg en " + str(round((0.748 - data[0]),4)) + " unidades.")
    else:
        recDict['keep'].append("Mantener este valor de Jg para una recuperaci??n alta.")
    #Bloque X2
    if(data[1] >= 1.016 and data[1] <= 1.307):
        recDict['keep'].append("Mantener este valor de D32 para una recomendaci??n alta.")
    elif(data[1] > 0.669 and data[1] < 1.016):
        recDict['inc'].append("Aumentar el valor de D32 en " + str(round((1.016 - data[1]),4)) + " unidades. ")
    else:
        if(data[1]>1.307):
            recDict['dec'].append("Disminuir el valor de D32 en " + str(round((data[1]-1.307),4)) + " unidades.")
        else:
            recDict['inc'].append("Aumentar el valor de D32 en " + str(round((1.016 - data[1]),4)) + " unidades.")

    #Bloque X3
    if(data[2] >= 12.045):
        recDict['keep'].append("Mantener este valor de Eg para una recuperaci??n alta.")
    else:
        recDict['inc'].append("Aumentar el valor de Eg en " + str(round((12.045 - data[2]),4)) + " unidades.")

    #Bloque X4
    if(data[3] >= 0.935):
        recDict['keep'].append("Mantener este valor de Jl para una recuperaci??n alta.")
    else:
        recDict['inc'].append("Aumentar el valor de Jl en" + str(round((0.935 - data[3]),4)) + " unidades.")

    if(data[8] in [5,8,3,2]):
        recDict['keep'].append("Este espumante ha resultado en recuperaciones altas, se recomienda continuar con su uso.")
    else:
        recDict['inc'].append("Se recomienda cambiar el espumante a uno de los siguientes: F150, F160-13, MIBC, TEB.")

    #Bloque X10
    if(data[9] >= 12.500):
        recDict['keep'].append("Mantener este valor de Ppm para una recuperaci??n alta.")
    else:
        recDict['inc'].append("Aumentar el valor de Ppm en " + str(round((12.5-data[9]),4)) + " unidades.")
    return recDict
