from django.db.models import F, ExpressionWrapper, fields
from AppInventario.models import Compra, Producto

def listar_productos_con_cantidad_baja():
    productos_bajos = Producto.objects.annotate(cantidad_diferencia=ExpressionWrapper(F('nivel_bajo') - F('cantidad'), output_field=fields.IntegerField())).filter(cantidad_diferencia__gt=0)
    
    # Obtener la cuenta total de productos bajos sin aplicar el límite
    count_productos_bajos_total = Producto.objects.annotate(cantidad_diferencia=ExpressionWrapper(F('nivel_bajo') - F('cantidad'), output_field=fields.IntegerField())).filter(cantidad_diferencia__gt=0).count()
    
    # Crear una lista de diccionarios con los detalles de cada producto bajo
    productos_bajos_detalles = [
        {
            'nombre': producto.nombre,
            'cantidad': producto.cantidad,
            'nivel_bajo': producto.nivel_bajo,
            'cantidad_diferencia': producto.cantidad_diferencia
        }
        for producto in productos_bajos
    ]

    return {'productos_bajos': productos_bajos_detalles, 'count_productos_bajos_total': count_productos_bajos_total}

from django.utils import timezone

def obtener_compras_proximas_a_vencer():
    # Obtener la fecha actual
    fecha_actual = timezone.now().date()

    # Calcular la fecha límite (fecha actual + 10 días)
    fecha_limite = fecha_actual + timezone.timedelta(days=10)

    # Filtrar las compras cuya fecha de vencimiento esté dentro de los próximos 10 días y obtener solo los primeros 3 registros
    compras_proximas_a_vencer = Compra.objects.filter(fecha_vec__lte=fecha_limite)

    # Obtener la cantidad total de registros sin aplicar el límite
    cantidad_registros_total = Compra.objects.filter(fecha_vec__lte=fecha_limite).count()

    # Crear una lista de diccionarios con los detalles de cada compra
    compras_detalles = [
        {
            'id': compra.id,
            'cantidad': compra.cantidad,
            'precio_unitario': compra.precio_unitario,
            'total': compra.total,
            'fecha_vec': compra.fecha_vec,
            'fecha_compra': compra.fecha_compra,
            'producto': compra.producto.nombre,
            'proveedor': compra.proveedor.nombre
        }
        for compra in compras_proximas_a_vencer
    ]

    return {'compras_proximas_a_vencer': compras_detalles, 'cantidad_registros_total': cantidad_registros_total}
