from django.shortcuts import render

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


def flot(request, pk):

    flot = None
    for i in flots:
        if i['id'] == int(pk):
            flot = i
    context = {'flot': flot}

    return render(request, 'base/flotacion.html', context )

def lix(request, pk):

    lix = None
    for i in lixs:
        if i['id'] == int(pk):
            lix = i
    context = {'lix': lix}

    return render(request, 'base/lixiviacion.html', context)