import models
import datetime

def getAllIncidentes():
    return models.Incidente.objects.all()

def getIncidente(id):
    return models.Incidente.objects.get(id=id)

def cerrarIncidente(id):
    models.FechasDeCierre.objects.create(incidente_id=id, fecha_cierre=datetime.now())

def abierto(id):
    return not models.FechasDeCierre.objects.filter(incidente_id=id).exists()

def getPrestacion(id_incidente):
    models.PrestacionDeServicio.objects.get(incidente_id=id_incidente)

