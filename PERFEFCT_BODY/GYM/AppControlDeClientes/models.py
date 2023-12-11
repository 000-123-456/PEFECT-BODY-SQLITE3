from datetime import datetime
from django.db import models
from django.forms import model_to_dict
from AppUsers.models import User
from AppControlDeClientes.op import *
from GYM.settings import MEDIA_URL,STATIC_URL
from datetime import datetime, timedelta,date

class Membresia(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    precio = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Precio")
    duracion = models.PositiveIntegerField(verbose_name='Duracion')
    estado = models.BooleanField(default=False, verbose_name='Estado')
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = 'membresia'
        verbose_name = 'Membresia'
        verbose_name_plural = 'Membresias'
        ordering = ['id']

class Miembro(models.Model):
    fecha_nac =  models.DateField(verbose_name='Fecha de nacimiento', null=False)
    telefono = models.CharField(max_length=9, null=True,blank=True, verbose_name='Teléfono') 
    direcccion = models.CharField(max_length=100, null=True,blank=True, verbose_name='Dirección')
    nombreContact = models.CharField(max_length=50, null=True,blank=True, verbose_name='Nombre de contacto')
    telefonoContact = models.CharField(max_length=9, null=True,blank=True, verbose_name='Teléfono de contacto')
    estado_membresia = models.PositiveIntegerField(default=0,verbose_name='Estado membresia')
    foto = models.ImageField(upload_to='Miembro/%Y/%m/%d',null=True,blank=True)
    genero = models.PositiveIntegerField(null=False, choices=opGenero, name='genero', verbose_name='Genero')
    estado = models.BooleanField(default=False, verbose_name='Estado')
    ## ---- EL MIEMBRO ES EL QUE SE DESACTIVA O SE ACTIVA DEPEDIENDO LA FECHA ----
    fecha_inicio = models.DateField(null=True,blank=True)
    fecha_fin = models.DateField(null=True,blank=True)
    ###----- CLAVES FORANEAS --------
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='user', null=True, blank=True)
    venta_activa = models.PositiveBigIntegerField(  verbose_name='venta_activa', null=True, blank=True, unique=True)
    def __str__(self) -> str:
        return self.id
    def get_image(self):
        if self.foto and not ("assets/img/avatares/" in str(self.foto)):
            return '{}{}'.format(MEDIA_URL,self.foto)
        elif "assets/img/avatares/" in str(self.foto):
            return str(self.foto)
        else:
            return '{}{}'.format(STATIC_URL,'assets/img/no-photo.jpg')
    class Meta:
        db_table = 'miembro'
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'
        ordering = ['id']
    def toJSON(self):
        item = model_to_dict(self, exclude=['foto'])
        return item 
    def calcular_edad(self):
        # Obtén la fecha de nacimiento del miembro
        fecha_nacimiento = self.fecha_nac
        # Obtiene la fecha actual
        fecha_actual = datetime.now().date()
        # Calcula la diferencia entre la fecha actual y la fecha de nacimiento
        edad = fecha_actual.year - fecha_nacimiento.year - ((fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        return edad
    def calcular_fecha_final(self):
        # Convierte la fecha de inicio en un objeto date
        fecha_inicio = datetime.strptime(self.fecha_inicio, '%Y-%m-%d')

        # Obtiene el primer día del mes siguiente
        primer_dia_del_mes_siguiente = date(
            fecha_inicio.year + (fecha_inicio.month // 12),
            (fecha_inicio.month % 12) + 1,
            1
        )

        # Calcula el último día del mes siguiente
        fecha_final = date(
            primer_dia_del_mes_siguiente.year + (primer_dia_del_mes_siguiente.month // 12),
            (primer_dia_del_mes_siguiente.month % 12) + 1,
            1
        ) - timedelta(days=1)
        self.fecha_fin = fecha_final.strftime('%Y-%m-%d')
        return fecha_final.strftime('%Y-%m-%d')


 


class HistorialMiembro(models.Model):
    peso = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Peso")
    altura = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Altura")
    imc = models.CharField(max_length=50, null=False, verbose_name='IMC')
    fecha_registro = models.DateField(auto_now=True)
    descripcion = models.CharField(max_length=100, null=True, verbose_name='Descripcion')
    ###----- CLAVES FORANEAS --------
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro')
    def __str__(self) -> str:
        return self.id
        
    class Meta:
        db_table = 'historialmiembro'
        verbose_name = 'HistorialMiembro'
        verbose_name_plural = 'HistorialMiembros'
        ordering = ['id']


class VentaMembresia(models.Model):
    fecha = models.DateField(auto_now=True)
    monto_pagado = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Total pagado")
    ###----- CLAVES FORANEAS --------
    empleado = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Empleado')
    membresia = models.ForeignKey(Membresia, on_delete=models.PROTECT, verbose_name='Membresia')
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro',null=True, blank=True)
    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'ventaMembresia'
        verbose_name = 'VentaMembresia'
        verbose_name_plural = 'VentasMembresia'
        ordering = ['id']

class Asistencia(models.Model):
    tipo = models.PositiveIntegerField(null=True, blank=True, choices=opTipo, verbose_name='Tipo')
    monto_pagado = models.DecimalField(max_digits=15,decimal_places=2,null=True,verbose_name="Total pagado")
    fecha = models.DateField(auto_now=True)
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    fecha_created = models.DateTimeField(auto_now=True)
    ###----- CLAVES FORANEAS --------
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro', null=True, blank=True)
    empleado = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Empleado')
  
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
    ##Campo Caloria
    ##Porciones
    tiempo_comida = models.PositiveIntegerField(null=True, blank=True, choices=opTiempo, verbose_name='Tiempo de comida')
    ###----- CLAVES FORANEAS --------
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro', null=True, blank=True)
    ##Que tome una agua
    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'dieta'
        verbose_name = 'Dieta'
        verbose_name_plural = 'Dietas'
        ordering = ['id']



class RutinaEjercicio(models.Model):
    dia = models.CharField(max_length=50, null=False, verbose_name='Dia')
    tipo_ejercicio = models.CharField(max_length=50, null=False, verbose_name='Tipo_ejercicio')
    links_video = models.CharField(max_length=50, null=False, verbose_name='Links_video')
    detalle_ejercicio = models.CharField(max_length=100, null=True, verbose_name='Detalle_Ejercicio')
    recomendacion = models.CharField(max_length=100, null=True, verbose_name='Recomendacion')
    ###----- CLAVES FORANEAS --------
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, verbose_name='Miembro', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.id
        
    class Meta:
        db_table = 'rutinaejercicio'
        verbose_name = 'Rutinaejercicio'
        verbose_name_plural = 'Rutinaejercicios'
        ordering = ['id']
#Registro de dieta
class Dieta(models.Model):
    nombre = models.CharField(max_length=100, null=True, verbose_name='nombre')
    rango = models.PositiveIntegerField(null=True, blank=True, choices=opRango, verbose_name='rango')
    class Meta:
        db_table = 'dieta'
        verbose_name = 'dieta'
        verbose_name_plural = 'dietas'
        ordering = ['id']
    

#Este es es la tabla que llevará cada comida de una dieta determinada
class Comida(models.Model):
    nombre = models.CharField(max_length=100, null=True, verbose_name='nombre')
    tiempo = models.PositiveIntegerField(null=True, blank=True, choices=opTiempo, verbose_name='tiempo')
    #Este campo lleva todos los ingredientes con su respectiva porcion que contiene la comida
    detalle = models.CharField(max_length=500, null=True, verbose_name='detalle')
    #Campo que indica a que dieta pertenece este plato de comida
    dieta = models.ForeignKey(Dieta, on_delete=models.CASCADE, verbose_name='Dieta')
    class Meta:
        db_table = 'comida'
        verbose_name = 'comida'
        verbose_name_plural = 'comidas'
        ordering = ['id']

