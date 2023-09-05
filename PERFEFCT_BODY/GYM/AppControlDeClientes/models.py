from django.db import models
from AppUsers.models import User
from AppControlDeClientes.op import *


class Membresia(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    precio = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Precio")
    duracion = models.PositiveIntegerField(default=0, verbose_name='Duracion')
    estado = models.BooleanField(default=False, verbose_name='Estado')
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = 'membresia'
        verbose_name = 'Membresia'
        verbose_name_plural = 'Membresias'
        ordering = ['id']

class Miembro(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombres')
    fecha_nac =  models.DateField(verbose_name='Fecha de nacimiento')
    telefono = models.CharField(max_length=9, null=True, verbose_name='Teléfono') 
    direcccion = models.CharField(max_length=100, null=False, verbose_name='Dirección')
    nombreContact = models.CharField(max_length=50, null=False, verbose_name='Nombre de contacto')
    telefonoContact = models.CharField(max_length=9, null=True, verbose_name='Teléfono de contacto')
    estado = models.BooleanField(default=False, verbose_name='Estado')
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = 'miembro'
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'
        ordering = ['id']  


class HistorialMiembro(models.Model):
    peso = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Peso")
    altura = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Altura")
    imc = models.CharField(max_length=50, null=False, verbose_name='IMC')
    fecha_registro = models.DateField(auto_now=True)
    descripcion = models.CharField(max_length=100, null=True, verbose_name='Descripcion')

    def __str__(self) -> str:
        return self.id
        
    class Meta:
        db_table = 'historialmiembro'
        verbose_name = 'HistorialMiembro'
        verbose_name_plural = 'HistorialMiembros'
        ordering = ['id']


class VentaMembresia(models.Model):
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto_pagado = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Total pagado")
    empleado = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Empleado')
    membresia = models.ForeignKey(Membresia, on_delete=models.PROTECT, verbose_name='Membresia')
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro')
    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'ventaMembresia'
        verbose_name = 'VentaMembresia'
        verbose_name_plural = 'VentasMembresia'
        ordering = ['id']

class Asistencia(models.Model):
    tipo = models.PositiveIntegerField(null=True, blank=True, choices=opTipo, verbose_name='Tipo')
    monto_pagado = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Total pagado")
    fecha_asistencia = models.DateField(auto_now=True)
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro', null=True, blank=True)
    empleado = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Empleado')
    fecha_created = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['id']

class Dieta(models.Model):
    dia = models.PositiveIntegerField(null=True, blank=True, choices=opDia, verbose_name='Dia')
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    imagen = models.ImageField(upload_to='Plato/%Y/%m/%d',null=True,blank=True)
    detalle_alimento = models.CharField(max_length=100, null=True, verbose_name='Detalle_Alimento')
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro', null=True, blank=True)
    tiempo_comida = models.CharField(max_length=100, null=True, verbose_name='Tiempo_Comida')
  
    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'dieta'
        verbose_name = 'Dieta'
        verbose_name_plural = 'Dietas'
        ordering = ['id']



class Rutinaejercicio(models.Model):
    dia = models.CharField(max_length=50, null=False, verbose_name='Dia')
    tipo_ejercicio = models.CharField(max_length=50, null=False, verbose_name='Tipo_ejercicio')
    links_video = models.CharField(max_length=50, null=False, verbose_name='Links_video')
    detalle_ejercicio = models.CharField(max_length=100, null=True, verbose_name='Detalle_Ejercicio')
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro', null=True, blank=True)
    recomendacion = models.CharField(max_length=100, null=True, verbose_name='Recomendacion')
    
  
    def __str__(self) -> str:
        return self.id
        
    class Meta:
        db_table = 'rutinaejercicio'
        verbose_name = 'Rutinaejercicio'
        verbose_name_plural = 'Rutinaejercicios'
        ordering = ['id']
