from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
urlpatterns = [

    path('Maquinaria/Añadir/',login_required(views.CreateMaquinaria.as_view()), name='añadir_maquina'),
    path('Maquinaria/Listado/',login_required(views.ListMaquinaria.as_view()), name='listar_maquina'),
    path('Maquinaria/ListadoEliminadas/',login_required(views.ListBajaMaquinaria.as_view()), name='listar_baja_maquina'),

    path('Maquinaria/Eliminar/<int:pk>/',login_required(views.EliminarMaquinaria), name='eliminar_maquina'),
    path('Maquinaria/Alta/<int:pk>/',login_required(views.AltaMaquinaria), name='alta_maquina'),
    path('Maquinaria/AltaTodas/',login_required(views.AltaTodasMaquinaria), name='alta_todas_maquina'),

    path('Maquinaria/Editar/<int:pk>/',login_required(views.UpdateMaquinaria.as_view()), name='editar_maquina'),

    path('HistorialMaquinaria/Agregar/', login_required(views.agregar_historial_maquinaria), name='agregar_historial_maquinaria'),
    path('HistorialMaquinaria/Terminar/', login_required(views.terminar_historial_maquinaria), name='terminar_historial_maquinaria'),
    path('HistorialMaquinaria/Ultimo/<int:id_maquina>/', login_required(views.obtener_ultimo_historial), name='obtener_ultimo_historial'),
    path('Maquinaria/Historial/Lista/<int:maquina_id>/', login_required(views.ListHistorialMaquina.as_view()), name='lista_historial'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
