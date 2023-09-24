from django.db import models
from django.core.files.storage import FileSystemStorage
from django.forms import model_to_dict
from GYM.settings import MEDIA_URL,STATIC_URL
from AppUsers.models import User,Empresa
from AppInventarioMaquinaria.opciones import *

class Maquinaria(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    descripcion = models.CharField(max_length=100, null=True, verbose_name='Descripcion')
    foto = models.ImageField(upload_to='maquinaria/',null=True,blank=True)
    categoriaM = models.CharField(max_length=50, null=False, choices=opCategoriaM, verbose_name='Categoria')
    estado_maquina = models.CharField(max_length=50, null=True, choices=opEstadoM, verbose_name='Estado de Maquina')
    ## CLAVES FORANEAS
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, verbose_name='Empresa', null=True, blank=True)
    ## FIN CLAVES FOREANEAS
    def __str__(self) -> str:
        return self.nombre
    class Meta:
        app_label = 'AppInventarioMaquinaria'
        db_table = 'maquinaria'
        verbose_name = 'Maquinaria'
        verbose_name_plural = 'Maquinarias'
        ordering = ['id']
    def get_image(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL,self.foto)
        return '{}{}'.format(STATIC_URL,'assets/img/no-photo.jpg')
    
class HistorialMaquinaria(models.Model):
    tipo = models.CharField(max_length=50, null=True, choices=opTipoM, verbose_name='Tipo') ##preventivo o correctivo 
    detalle = models.CharField(max_length=100, null=True, verbose_name='Detalle')
    fecha_fin = models.DateField(verbose_name='Fecha final')
    fecha_ini = models.DateField(verbose_name='Fecha de inicio')
    ## CLAVES FORANEAS
    maquinaria = models.ForeignKey(Maquinaria,null=False,verbose_name='Maquinaria',on_delete=models.PROTECT)
    def __str__(self) -> str:
        return self.id
    class Meta:
        app_label = 'AppInventarioMaquinaria'
        db_table = 'historialmaquinaria'
        verbose_name = 'HistorialMaquinaria'
        verbose_name_plural = 'HistorialMaquinarias'
        ordering = ['id']