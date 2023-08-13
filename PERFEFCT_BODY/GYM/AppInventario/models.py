from django.db import models

from GYM import settings


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
    nombre = models.CharField(max_length=50, null=False, verbose_name='Nombre')
    
    def __str__(self) -> str:
        return self.nombre
    
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
    img = models.ImageField(upload_to='avatar/%Y/%m/%d',null=True,blank=True) 
    def __str__(self) -> str:
        return self.nombre
    
    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['id']

class Compra(models.Model):
    cantidad = models.PositiveIntegerField(verbose_name='Cantidad', null=False)
    total = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Total de compra")
    fecha_vec = models.DateField()
    fecha_compra = models.DateField(auto_now=True)
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

    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'ventas'
        ordering = ['id']

class LineaVenta(models.Model):
    cantidad = models.PositiveIntegerField(default=0, verbose_name='Cantidad')
    precio = models.DecimalField(max_digits=15,decimal_places=2,null=False,verbose_name="Precio")
    producto = models.ForeignKey(Producto,null=False,verbose_name='Producto',on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return self.id
    
    class Meta:
        db_table = 'lineaventa'
        verbose_name = 'LineaVenta'
        verbose_name_plural = 'LineasVentas'
        ordering = ['id']

