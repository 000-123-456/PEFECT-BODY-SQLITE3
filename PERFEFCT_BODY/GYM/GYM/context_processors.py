from AppInventario.funciones import listar_productos_con_cantidad_baja, obtener_compras_proximas_a_vencer
from AppUsers.models import Empresa


def site_settings(request):
    return {
        'notications':{
            'count':listar_productos_con_cantidad_baja()['count_productos_bajos_total']+obtener_compras_proximas_a_vencer()['cantidad_registros_total'],
            'notification_producto_bajos': listar_productos_con_cantidad_baja(),
            'notification_producto_vencimiento':obtener_compras_proximas_a_vencer(),

        },
        'empresa':Empresa.objects.first()
        
    }