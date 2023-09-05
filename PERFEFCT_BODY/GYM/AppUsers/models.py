from django.db import models
from django.contrib.auth.models import AbstractUser
from AppUsers.opciones import opRol
# Create your models here.

class Empresa(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    tarifa = models.PositiveIntegerField(verbose_name='Tarifa', null=False)
    logo = models.ImageField(upload_to='Empresa/%Y/%m/%d',null=True,blank=True)
    telefono = models.CharField(max_length=9, null=True, verbose_name='Teléfono') 
    direcccion = models.CharField(max_length=100, null=False, verbose_name='Dirección')
    
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = 'empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['id']

class User(AbstractUser):
    rol = models.PositiveIntegerField(null=True, blank=True, choices=opRol, name='rol', verbose_name='Rol')
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, verbose_name='Empresa', null=True, blank=True)





