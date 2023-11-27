
from django.db import models
import datetime


class Afectacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    afectado = models.TextField(blank=True, null=True)  # This field type is a guess.
    prestaciondeservicio = models.ForeignKey('PrestacionDeServicio', models.DO_NOTHING, db_column='prestacionDeServicio_id', blank=True, null=True)  # Field name made lowercase.
    membresia = models.ForeignKey('Membresia', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'afectacion'


class Comunidad(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    notificador = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comunidad'


class ComunidadPrestacionDeServicio(models.Model):
    comunidad = models.OneToOneField(Comunidad, models.DO_NOTHING, db_column='Comunidad_id', primary_key=True)  # Field name made lowercase.
    serviciosdeinteres = models.ForeignKey('PrestacionDeServicio', models.DO_NOTHING, db_column='serviciosDeInteres_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'comunidad_prestacion_de_servicio'
        unique_together = (('comunidad', 'serviciosdeinteres'),)


class ConfiguracionDeNotificaciones(models.Model):
    id = models.BigAutoField(primary_key=True)
    medio_preferido = models.CharField(max_length=255, blank=True, null=True)
    estrategiadenotificacion = models.ForeignKey('Estrategiadenotificacion', models.DO_NOTHING, db_column='estrategiaDeNotificacion_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'configuracion_de_notificaciones'


class Entidad(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    localizacion = models.ForeignKey('Localizacion', models.DO_NOTHING, blank=True, null=True)
    entidad_prestadora = models.ForeignKey('EntidadPrestadora', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'entidad'


class EntidadPrestadora(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    personadesignada = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='personaDesignada_id', blank=True, null=True)  # Field name made lowercase.
    organismo_de_control = models.ForeignKey('OrganismoDeControl', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entidad_prestadora'


class Establecimiento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    localizacion = models.ForeignKey('Localizacion', models.DO_NOTHING, blank=True, null=True)
    entidad = models.ForeignKey(Entidad, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'establecimiento'


class Estrategiadenotificacion(models.Model):
    dtype = models.CharField(db_column='DTYPE', max_length=31)  # Field name made lowercase.
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'estrategiadenotificacion'


class EstrategiadenotificacionNotificacion(models.Model):
    sinapuros = models.ForeignKey(Estrategiadenotificacion, models.DO_NOTHING, db_column='SinApuros_id')  # Field name made lowercase.
    anotificar = models.OneToOneField('Notificacion', models.DO_NOTHING, db_column='aNotificar_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'estrategiadenotificacion_notificacion'


class FechasDeCierre(models.Model):
    incidente = models.ForeignKey('Incidente', models.DO_NOTHING)
    fechasdecierre = models.DateTimeField(db_column='fechasDeCierre', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fechas_de_cierre'

# models.py


class Fusion(models.Model):
    id = models.BigAutoField(primary_key=True)
    estado = models.CharField(max_length=255, blank=True, null=True)
    fecha_creada = models.DateTimeField(blank=True, null=True)
    comunidad1 = models.ForeignKey('Comunidad', models.DO_NOTHING, related_name='fusion_comunidad1', blank=True, null=True)
    comunidad2 = models.ForeignKey('Comunidad', models.DO_NOTHING, related_name='fusion_comunidad2', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fusion'


class Horarios(models.Model):
    sinapuros = models.ForeignKey(Estrategiadenotificacion, models.DO_NOTHING, db_column='sinApuros_id')  # Field name made lowercase.
    horario = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'horarios'


class Incidente(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_de_apertura = models.DateTimeField(blank=True, null=True)
    notificador = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    abiertopor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='abiertoPor_id', blank=True, null=True)  # Field name made lowercase.
    prestacion_de_servicio = models.ForeignKey('PrestacionDeServicio', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'incidente'

    def abierto(self):
        return not FechasDeCierre.objects.filter(incidente_id=self.id).exists()
    
    def abiertoPor(self):
        return Usuario.objects.get(id=self.abiertopor_id)
    
    def cerradoPor(self):
        return IncidenteDeComunidad.objects.all().filter(incidente_id=self.id).first().cerradopor

    def fechaDeCierre(self):
        return IncidenteDeComunidad.objects.all().filter(incidente_id=self.id).first().fecha_de_cierre

    def cerrar(self):
        incidente = IncidenteDeComunidad.objects.all().filter(incidente_id=self.id).first()
        incidente.cerrar()
    
    

class IncidenteDeComunidad(models.Model):
    id = models.BigAutoField(primary_key=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    fecha_de_cierre = models.DateTimeField(blank=True, null=True)
    cerradopor = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='cerradoPor_id', blank=True, null=True)  # Field name made lowercase.
    incidente = models.ForeignKey(Incidente, models.DO_NOTHING, blank=True, null=True)
    comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'incidente_de_comunidad'

    def cerrar(self):
        self.estado = False
        self.fecha_de_cierre = datetime.datetime.now()
        self.cerradopor = Usuario.objects.get(id=1)
        self.save()


class Informe(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField()
    nombre = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'informe'


class Interes(models.Model):
    id = models.BigAutoField(primary_key=True)
    entidad = models.ForeignKey(Entidad, models.DO_NOTHING, blank=True, null=True)
    servicio = models.ForeignKey('Servicio', models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'interes'


class Localidad(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING, blank=True, null=True)
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localidad'


class Localizacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    localidad = models.ForeignKey(Localidad, models.DO_NOTHING, blank=True, null=True)
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING, blank=True, null=True)
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'localizacion'


class Membresia(models.Model):
    id = models.BigAutoField(primary_key=True)
    comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, blank=True, null=True)
    rol = models.ForeignKey('Rol', models.DO_NOTHING, blank=True, null=True)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'membresia'


class Municipio(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    provincia = models.ForeignKey('Provincia', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'municipio'


class Notificacion(models.Model):
    id = models.BigAutoField(primary_key=True)
    asunto = models.CharField(max_length=255, blank=True, null=True)
    cuerpo = models.CharField(max_length=255, blank=True, null=True)
    estrategia_de_notificacion = models.CharField(max_length=255, blank=True, null=True)
    destinatario = models.ForeignKey('Usuario', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notificacion'


class OrganismoDeControl(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    personadesignada = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='personaDesignada_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'organismo_de_control'


class Permiso(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    nombreinterno = models.CharField(db_column='nombreInterno', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'permiso'


class PrestacionDeServicio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    servicio = models.ForeignKey('Servicio', models.DO_NOTHING)
    ubicacionexacta = models.ForeignKey('UbicacionExacta', models.DO_NOTHING, db_column='ubicacionExacta_id', blank=True, null=True)  # Field name made lowercase.
    establecimiento = models.ForeignKey(Establecimiento, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'prestacion_de_servicio'


class Provincia(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provincia'


class RevisionDeIncidentes(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'revision_de_incidentes'


class Rol(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rol'


class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, models.DO_NOTHING)
    permiso = models.ForeignKey(Permiso, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'rol_permiso'


class Servicio(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'servicio'


class UbicacionExacta(models.Model):
    id = models.BigAutoField(primary_key=True)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ubicacion_exacta'


class Usuario(models.Model):
    id = models.BigAutoField(primary_key=True)
    apellido = models.CharField(max_length=255)
    contrasenia = models.CharField(max_length=255)
    correo_electronico = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    configuraciondenotificaciones = models.ForeignKey(ConfiguracionDeNotificaciones, models.DO_NOTHING, db_column='configuracionDeNotificaciones_id', blank=True, null=True)  # Field name made lowercase.
    rol = models.ForeignKey(Rol, models.DO_NOTHING, blank=True, null=True)
    ubicacionexacta = models.ForeignKey(UbicacionExacta, models.DO_NOTHING, db_column='ubicacionExacta_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'


class UsuarioIncidente(models.Model):
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='Usuario_id')  # Field name made lowercase.
    revisiondeincidentes = models.ForeignKey(Incidente, models.DO_NOTHING, db_column='revisionDeIncidentes_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario_incidente'
