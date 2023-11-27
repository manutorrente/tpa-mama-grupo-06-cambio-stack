from django.shortcuts import render
from . import models

def lista_incidentes(request):
    context = {"incidentes": models.Incidente.objects.all()} 
    return render(request, "incidentes.html", context)

def incidente(request, id):
    context = {"incidente": models.Incidente.objects.get(id=id)}
    return render(request, "incidente.html", context)

def cerrar_incidente(request, id):
    incidente = models.Incidente.objects.get(id=id)
    incidente.cerrar()
    return incidente(request, id)
