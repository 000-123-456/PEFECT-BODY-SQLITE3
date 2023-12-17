from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #------------------------------------LOGIN---------------------------------------------------------------------------
    path('',login_required(views.prueba), name='prueba'),




    #------------------------------INICIO DE LAS VISTAS DE MIEMBRO-------------------------------------------------------
    path('Miembro/',login_required(views.ListMiembro.as_view()), name='lista_miembros'),
    path('Miembro/CrearMiembro/',login_required(views.RegistroMiembroView.as_view()), name='crear_miembro'),
    path('Miembro/ActualizarMiembro/<int:pk>/',login_required(views.ActualizarMiembroView.as_view()), name='actualizar_miembro'),
    path('Miembro/get_miembro/<str:username>/',login_required(views.get_miembro), name='get_miembro'),
    path('Miembro/eliminarMiembro/<int:pk>/',login_required(views.baja_miembro), name='baja_miembro'),
    path('Miembro/MiembrosEliminados/',login_required(views.ListMiembroEliminados.as_view()), name='bajas_miembros'),
    path('Miembro/MiembrosEliminados/get_miembro/<str:username>/',login_required(views.get_miembro), name='get_miembro_bajas'),
    path('Miembro/MiembrosEliminados/restaurarMiembro/<int:pk>/',login_required(views.alta_miembro), name='alta_miembro'),
    path('Miembro/MiembrosEliminados/restaurarTodosMiembro/',login_required(views.alta_todos_miembros), name='alta_todos_miembro'),
    #------------------------------FIN DE LAS VISTAS DE MIEMBRO-------------------------------------------------------

    #------------------------------INICIO DE LAS VISTAS DE VENTA MEMBRESIA-------------------------------------------------------
    path('Miembro/CrearVentaMembresia/<str:username>/<int:idmember>/', login_required(views.create_venta_membresia), name='create_venta_membresia'),
    path('VentaMembresia/', login_required(views.ListVentaMembresia.as_view()), name='list_venta_membresia'),
    path('VentaMembresia/estadisticas/', login_required(views.EstadisticasVentaMembresia.as_view()), name='estadisticas_venta_membresia'),
    path('VentaMembresia/EliminarVentaMembresia/<int:pk>/', login_required(views.DeleteVentaMembresia), name='delete_venta_membresia'),
    #------------------------------INICIO DE LAS VISTAS DE VENTA MEMBRESIA-------------------------------------------------------

    #----------------------------INICIO DE LAS VISTAS DE MEMBRESIA --------------------------------------------------------
    path('Membresia/CrearMembresia/',login_required(views.CreateMembresia.as_view()), name='crear_membresia'),
    path('Membresia/',login_required(views.ListMembresia.as_view()), name='lista_membresias'),
    path('Membresia/MembresiaEliminadas/',login_required(views.ListMembresiaBajas.as_view()), name='lista_bajas_membresias'),
    path('Membresia/MembresiaEliminadas/AltaMembresia/<int:pk>/',login_required(views.AltaMembresia), name='alta_membresia'),
    path('Membresia/MembresiaEliminadas/AltaTodos/',login_required(views.AltaTodosMembresia), name='alta_todas_membresias'),
    path('Membresia/ActualizarMembresias/<int:pk>/', login_required(views.UpdateMembresia.as_view()), name='actualizar_membresia'),
    path('Membresia/EliminarMembresia/<int:pk>/', login_required(views.DeleteMembresia), name='eliminar_membresia'),



    #--------------------------------------------HISTORIAL DE MIEMBRO-------------------------------------------------------
    path('HistorialMiembro/CreateHistorialMiembro/',login_required(views.CreateHistorialMiembro.as_view()), name='crear_historialmiembro'),
    path('HistorialMiembro/',login_required(views.ListHistorialMiembro.as_view()), name='lista_historialmiembros'),
    path('HistorialMiembro/ActualizarHistorialMiembros/<int:pk>/', login_required(views.UpdateHistorialMiembro.as_view()), name='actualizar_historialmiembro'),
    path('HistorialMiembro/EliminarHistorialMiembros/<int:pk>/', login_required(views.DeleteHistorialMiembro), name='eliminar_historialmiembros'),


    #--------------------------------------------ASISTENCIA DE MIEMBRO-------------------------------------------------------
    path('Asistencia/Registro/',login_required(views.CreateAsistenciaMiembro.as_view()), name='registro_asistencia'),
    path('Asistencia/listaMiembros/',login_required(views.lista_miembros), name='lista_miembros_asistencia'),
    path('Asistencia/marcar_asistencia/',login_required(views.registrar_asistencia), name='registrar_asistencia'),
    path('Asistencia/Listado/',login_required(views.ListHistorialAsistencias.as_view()), name='lista_asistencia'),
    path('Asistencia/eliminarAsistencia/<int:pk>/',login_required(views.eliminarHistorial), name='eliminar_asistencia'),


     #--------------------------------------------DIETAS DE MIEMBRO-------------------------------------------------------
    path('Dietas',login_required(views.ListDietas.as_view()), name='dietas'),    

     #--------------------------------------------RECOMENDACIONES DIETAS-------------------------------------------------------
    path('Recomendaciones/Dietas/registro/',login_required(views.CreateRecomendacionDieta.as_view()), name='registro_recomendaciones_dieta'),
    path('Recomendaciones/Dietas/',login_required(views.ListRecomendacionDieta.as_view()), name='lista_recomendaciones_dieta'), 
    #--------------------------------------------RECOMENDACIONES DE COMIDAS-------------------------------------------------------
    path('Recomendaciones/Dietas/comida/registro/<int:pk>/',login_required(views.CreateRecomendacionComida.as_view()), name='registro_recomendaciones_comida'),
    path('Recomendaciones/Dietas/comida/lista/<int:pk>/',login_required(views.ListRecomendacionComida.as_view()), name='lista_recomendaciones_comida'),       
    
]