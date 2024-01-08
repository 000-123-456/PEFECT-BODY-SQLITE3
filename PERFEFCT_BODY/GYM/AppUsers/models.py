from django.db import models
from django.contrib.auth.models import AbstractUser
from AppUsers.opciones import opRol
from GYM.settings import MEDIA_URL,STATIC_URL
# Create your models here.

class Empresa(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    tarifa = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Tarifa")
    logo = models.ImageField(upload_to='Empresa/',null=True,blank=True)
    telefono = models.CharField(max_length=9, null=True, verbose_name='Teléfono') 
    direcccion = models.CharField(max_length=100, null=False, verbose_name='Dirección')
    def __str__(self) -> str:
        return self.nombre
    class Meta:
        db_table = 'empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['id']
    def get_image(self):
        if self.logo:
            return '{}{}'.format(MEDIA_URL,self.logo)
        return '{}{}'.format(STATIC_URL,'assets/img/no-photo.jpg')
class User(AbstractUser):
    rol = models.PositiveIntegerField(null=True, blank=True, choices=opRol, name='rol', verbose_name='Rol')
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, verbose_name='Empresa', null=True, blank=True)
    primer_ingreso = models.BooleanField(default=True)




