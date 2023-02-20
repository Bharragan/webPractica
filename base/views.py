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
            print(excelForm.is_valid())
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

    print("ta bien")
