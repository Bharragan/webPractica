from django.shortcuts import render
from django.http import HttpResponse
import csv
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
    data= {}
    try:
        if request.method=="POST":
            x1 = float(request.POST.get('jg'))
            x2 = float(request.POST.get('d32'))
            x3 = float(request.POST.get('eg'))
            x4 = float(request.POST.get('jl'))
            x5 = float(request.POST.get('dcolumna'))
            x6 = float(request.POST.get('dpulpa'))
            x7 = float(request.POST.get('dburbuja'))
            x9 = float(request.POST.get('dviscosidad'))
            x8 = request.POST.get('froth')
            x10 = float(request.POST.get('ppm'))
            data = {
                'x1':x1,
                'x2':x2,
            }
            
    except:
        pass

    return render(request, 'base/flotacion.html', data)

def downloadFlotation(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['x1','x2'])
    response['Content-Disposition']='attachment; filename="flotExample.csv"'
    return response

def lix(request, pk):

    lix = None
    for i in lixs:
        if i['id'] == int(pk):
            lix = i
    context = {'lix': lix}

    return render(request, 'base/lixiviacion.html', context)