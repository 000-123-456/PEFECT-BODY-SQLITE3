from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('usuario/registrar/',views.RegistroUsuario.as_view(), name='registrar'),
    path('usuario/login/',views.LoginFormView.as_view(), name='login'),
    path('usuario/logout/',LogoutView.as_view(), name='logout'),
    path('Empresa/registrar/',login_required(views.CrearEmpresa.as_view()), name='registrar_empresa'),
    path('Empresa/ActualizarEmpresas/<int:pk>/', login_required(views.UpdateEmpresa.as_view()), name='actualizar_empresa'),
    
    
    
    #USER UI
    path('userUI/',login_required(views.inicioMiembro.as_view()), name='inicio_miembro'),
    #URL DE PERMISOS
    path('permisos/',login_required(views.SinPermisoView.as_view()), name='sin_permiso'),
    #Notificaciones
    path('notificaciones/',login_required(views.NotificacionesView.as_view()), name='notificaciones'),

    #USUARIOS QUE CREA EL ADMINISTRADOR(EMPLEADOS Y ADMINISTRADORES)
    path('usuarios/crear/',login_required(views.CrearUsuario.as_view()), name='crear_usuario'),
    path('usuarios/',login_required(views.ListUsuarios.as_view()), name='lista_usuario'),
    path('usuarios/actualizar/<int:pk>/',login_required(views.UpdateUsuario.as_view()), name='actualizar_usuario'),
    path('usuarios/baja/<int:pk>/',login_required(views.BajaUsuario), name='baja_usuario'),
    path('usuarios/papelera/alta/<int:pk>/',login_required(views.AltaUsuario), name='alta_usuario'),
    path('usuarios/papelera/',login_required(views.ListBajasUsuarios.as_view()), name='papelera_usuario'),
    path('usuarios/primera-clave/',login_required(views.CambioClave.as_view()), name='primera_clave'),
    path('usuarios/olvido-clave/',views.OlvidoClave.as_view(), name='olvido_clave'),
    
    #Bitacora
    path('historial/venta_membresias/',login_required(views.BitacoraVentaMembresiaView.as_view()), name='bitacora_venta_membresia'),
    path('historial/asistencias/',login_required(views.BitacoraAsistenciaView.as_view()), name='bitacora_asistencias'),
     path('historial/ventas/',login_required(views.BitacoraVentasView.as_view()), name='bitacora_ventas'),
    path('backup/descargar/', views.backup_view, name='backup'),
    path('backup/', views.template_backup_view.as_view(), name='backup_vista'),
    path('restore/', views.RestoreView.as_view(), name='restore'),
]
