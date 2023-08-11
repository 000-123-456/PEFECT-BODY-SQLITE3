from django.db import models
from django.contrib.auth.models import AbstractUser
from AppUsers.opciones import opRol
# Create your models here.

class User(AbstractUser):
    rol = models.PositiveIntegerField(null=True, blank=True, choices=opRol, name='rol', verbose_name='Rol')
    

