from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect

# Create your models here.
class HorariosLaboratorios(models.Model):
    nombre                 = models.TextField(max_length=255, null= True, blank=True)
    lunes                  = models.TextField(max_length=255, null= True, blank=True)
    martes                 = models.TextField(max_length=255, null= True, blank=True)
    miercoles              = models.TextField(max_length=255, null= True, blank=True)
    jueves                 = models.TextField(max_length=255, null= True, blank=True)
    viernes                = models.TextField(max_length=255, null= True, blank=True)
    sabado                 = models.TextField(max_length=255, null= True, blank=True)
    domingo                = models.TextField(max_length=255, null= True, blank=True)
    ultimaModificacion     = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.nombre)
#        return str(self.nombre) + ' | ' + str(self.ultimaModificacion)
        print(self)



class HorariosProfesores(models.Model):
    nombre                 = models.TextField(max_length=255, null= False, blank=False, default='Nombre')
    lunes                  = models.TextField(max_length=255, null= True, blank=True)
    martes                 = models.TextField(max_length=255, null= True, blank=True)
    miercoles              = models.TextField(max_length=255, null= True, blank=True)
    jueves                 = models.TextField(max_length=255, null= True, blank=True)
    viernes                = models.TextField(max_length=255, null= True, blank=True)
    sabado                 = models.TextField(max_length=255, null= True, blank=True)
    domingo                = models.TextField(max_length=255, null= True, blank=True)
    ultimaModificacion     = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.nombre)
        print(self)

class Ubicaciones(models.Model):
    nombre                 = models.TextField(max_length=255, null= False, blank=False)
    latitud                = models.DecimalField(max_digits=20, null= False, blank=True, decimal_places=15)
    longitud               = models.DecimalField(max_digits=20, null= False, blank=True, decimal_places=15)
    ultimaModificacion     = models.DateTimeField(auto_now=True)



    def __str__(self):
        return str(self.nombre)
        print(self)
    #def get_absolute_url(self):
    #       self.save()
    #      return reverse('respuesta-detalle', args=(self.pk,))

class ArchivoExcel(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Actualizaciones de Horarios de profesores/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.documento)
        print(self)

class ArchivoExcelHorariosLaboratorios(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Actualizaciones de Horarios de Laboratorios/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.documento)
        print(self)

class ArchivoExcelUbicaciones(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Actualizaciones de Ubicaciones/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.documento)
        print(self)

class Calendario(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Calendario estudiantil/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.documento)
        print(self)


class Pensum(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Pensum/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.documento)
        print(self)

class Reglamento(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Reglamento/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.documento)
        print(self)

class AsignacionCasilleros(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Asignacion Casilleros/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.documento)
        print(self)



class ActividadesExtra(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Actividades Extracuriculares/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.documento)
        print(self)

class Normatividad(models.Model):
    intent                 = models.TextField(max_length=255, null= False, blank=False)
    pregunta               = models.TextField(max_length=255, null= True, blank=False)
    respuesta              = models.TextField(max_length=255, null= True, blank=False)
    complemento            = models.TextField(max_length=255, null= True, blank=True)
    ejemplo1               = models.TextField(max_length=255, null= True, blank=False, default='¿Como preguntarían los usuarios por esta intención?')
    ejemplo2               = models.TextField(max_length=255, null= True, blank=False, default='¿Como preguntarían los usuarios por esta intención?')
    ejemplo3               = models.TextField(max_length=255, null= True, blank=False, default='¿Como preguntarían los usuarios por esta intención?')
    ejemplo4               = models.TextField(max_length=255, null= True, blank=True)
    ejemplo5               = models.TextField(max_length=255, null= True, blank=True)
    ejemplo6               = models.TextField(max_length=255, null= True, blank=True)
    ejemplo7               = models.TextField(max_length=255, null= True, blank=True)
    ejemplo8               = models.TextField(max_length=255, null= True, blank=True)
    ejemplo9               = models.TextField(max_length=255, null= True, blank=True)
    ejemplo10              = models.TextField(max_length=255, null= True, blank=True)
    ejemplo11              = models.TextField(max_length=255, null= True, blank=True)
    ejemplo12              = models.TextField(max_length=255, null= True, blank=True)
    ejemplo13              = models.TextField(max_length=255, null= True, blank=True)
    ejemplo14              = models.TextField(max_length=255, null= True, blank=True)
    ejemplo15              = models.TextField(max_length=255, null= True, blank=True)
    ultimaModificacion     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.intent)
        print(self)

class NormatividadArchivo(models.Model):
    nombre                 = models.CharField(max_length=255, null= True, blank=True)
    documento              = models.FileField(upload_to='Normatividad/')
    ultimaModificacion     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.documento)
        print(self)


class MensajeMasivo(models.Model):
    tema                = models.CharField(max_length=255, null= True, blank=True)
    mensaje              = models.TextField(null= True, blank=True)
    ultimaModificacion     = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tema)
        print(self)
    #def get_absolute_url(self):
    #       self.save()
    #      return reverse('respuesta-detalle', args=(self.pk,))
