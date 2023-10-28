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



]