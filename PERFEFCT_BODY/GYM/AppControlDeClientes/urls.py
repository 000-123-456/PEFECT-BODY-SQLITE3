from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #------------------------------------LOGIN---------------------------------------------------------------------------
    path('',login_required(views.prueba), name='prueba'),




    #------------------------------INICIO DE LAS VISTAS DE MIEMBRO-------------------------------------------------------
    path('Miembro/CrearMiembro/',views.CreateMiembro.as_view(), name='crear_miembro'),


    #----------------------------INICIO DE LAS VISTAS DE MEMBRESIA --------------------------------------------------------
    path('Membresia/CrearMembresia/',login_required(views.CreateMembresia.as_view()), name='crear_membresia'),
    path('Membresia/',login_required(views.ListMembresia.as_view()), name='lista_membresias'),
    path('Membresia/MembresiaEliminadas/',login_required(views.ListMembresiaBajas.as_view()), name='lista_bajas_membresias'),
    path('Membresia/MembresiaEliminadas/AltaMembresia/<int:pk>/',login_required(views.AltaMembresia), name='alta_membresia'),
    path('Membresia/MembresiaEliminadas/AltaTodos/',login_required(views.AltaTodosMembresia), name='alta_todas_membresias'),
    path('Membresia/ActualizarMembresias/<int:pk>/', login_required(views.UpdateMembresia.as_view()), name='actualizar_membresia'),
    path('Membresia/EliminarMembresia/<int:pk>/', login_required(views.DeleteMembresia), name='eliminar_membresia'),


]