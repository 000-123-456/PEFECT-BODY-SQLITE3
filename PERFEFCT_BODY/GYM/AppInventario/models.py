from django.db import models
from django.core.files.storage import FileSystemStorage
from django.forms import model_to_dict
from GYM.settings import MEDIA_URL,STATIC_URL
from AppUsers.models import User,Empresa
from AppInventario.opciones import *

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    telefono = models.CharField(max_length=9, null=True, verbose_name='Teléfono')
    correo = models.EmailField(max_length=254, verbose_name='Correo')
    direcccion = models.CharField(max_length=100, null=False, verbose_name='Dirección')
    # -----Estado sirve para dar de baja a los proveedores-------
    estado = models.BooleanField(default=False, verbose_name='Estado')
    
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = 'proveedor'
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['id']

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre', unique=True)
    # -----Perecedero es para saber si los productos de esta categoria perecen o tiene fecha de caducidad-------
    perecedero = models.BooleanField(default=False, verbose_name='Perecedero')
    estado = models.BooleanField(default=False, verbose_name='Estado')
    def __str__(self) -> str:
        return self.nombre
    def toJSON(self):
        item = model_to_dict(self)
        return item
    class Meta:
        db_table = 'categoria'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

class Producto(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    descripcion = models.CharField(max_length=100, null=True, verbose_name='Descripcion')
    cantidad = models.PositiveIntegerField(default=0, verbose_name='Cantidad')
    precio_venta = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Precio de venta")
    estado = models.BooleanField(default=False, verbose_name='Estado')
    fecha_created = models.DateTimeField(auto_now_add=True)
    fecha_updated = models.DateTimeField(auto_now_add=True)
    categoriaP = models.ForeignKey(Categoria, null=False, verbose_name='Categoria', on_delete=models.PROTECT)
    img = models.ImageField(upload_to='productos/',null=True,blank=True)
    nivel_bajo = models.PositiveIntegerField(verbose_name='Nivel bajo de producto')
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']
    def get_image(self):
        if self.img:
            return '{}{}'.format(MEDIA_URL,self.img)
        return '{}{}'.format(STATIC_URL,'assets/img/no-photo.jpg')

class Compra(models.Model):
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad', null=False)
    precio_unitario = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Precio unitario")
    total = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Total de compra")
    fecha_vec = models.DateField(verbose_name='Fecha de vencimiento')
    fecha_compra = models.DateField(auto_now=True)
    fecha_created = models.DateTimeField(auto_now_add=True)
    fecha_updated = models.DateTimeField(auto_now_add=True)
    ## CLAVES FORANEAS
    producto = models.ForeignKey(Producto,null=False,verbose_name='Producto',on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor,null=False,verbose_name='Proveedor',on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'compra'
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['id']

class Venta(models.Model):
    total = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Total")
    fecha_venta = models.DateField(auto_now=True)
    fecha_created = models.DateTimeField(auto_now=True)
    ## CLAVES FORANEAS
    empleado = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Empleado')
    
    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'ventas'
        ordering = ['id']

class LineaVenta(models.Model):
    cantidad = models.PositiveIntegerField(default=0, verbose_name='Cantidad')
    precio_vendido = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Precio vendido")
    subtotal = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Subtotal")
    ## CLAVES FORANEAS
    producto = models.ForeignKey(Producto,null=False,verbose_name='Producto',on_delete=models.PROTECT)
    venta = models.ForeignKey(Venta,null=False,verbose_name='Venta',on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'lineaventa'
        verbose_name = 'LineaVenta'
        verbose_name_plural = 'LineasVentas'
        ordering = ['id']

class Maquinaria(models.Model):
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    descripcion = models.CharField(max_length=100, null=True, verbose_name='Descripcion')
    foto = models.ImageField(upload_to='maquinaria/',null=True,blank=True)
    categoria = models.CharField(max_length=50, null=False, verbose_name='Categoria')
    estado_maquina = models.CharField(max_length=50, null=True, choices=opEstadoM, verbose_name='Estado de Maquina')
    ## CLAVES FORANEAS
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, verbose_name='Empresa', null=True, blank=True)
    ## FIN CLAVES FOREANEAS
    def __str__(self) -> str:
        return self.nombre
    class Meta:
        db_table = 'maquinaria'
        verbose_name = 'Maquinaria'
        verbose_name_plural = 'Maquinarias'
        ordering = ['id']
    def get_image(self):
        if self.foto:
            return '{}{}'.format(MEDIA_URL,self.foto)
        return '{}{}'.format(STATIC_URL,'assets/img/no-photo.jpg')
    
class HistorialMaquinaria(models.Model):
    tipo = models.CharField(max_length=50, null=True, verbose_name='Tipo') ##preventivo o correctivo 
    detalle = models.CharField(max_length=100, null=True, verbose_name='Detalle')
    fecha_fin = models.DateField(verbose_name='Fecha final')
    fecha_ini = models.DateField(verbose_name='Fecha de inicio')
    ## CLAVES FORANEAS
    maquinaria = models.ForeignKey(Maquinaria,null=False,verbose_name='Maquinaria',on_delete=models.PROTECT)
    def __str__(self) -> str:
        return self.id
    class Meta:
        db_table = 'historialmaquinaria'
        verbose_name = 'HistorialMaquinaria'
        verbose_name_plural = 'HistorialMaquinarias'
        ordering = ['id']


