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
    path('userUI/',login_required(views.inicioMiembro), name='inicio_miembro'),
    #URL DE PERMISOS
    path('permisos/',login_required(views.SinPermisoView.as_view()), name='sin_permiso'),
    #Notificaciones
    path('notificaciones/',login_required(views.NotificacionesView.as_view()), name='notificaciones'),

    #USUARIOS QUE CREA EL ADMINISTRADOR(EMPLEADOS Y ADMINISTRADORES)
    path('usuarios/crear/',login_required(views.CrearUsuario.as_view()), name='crear_usuario'),
    path('usuarios/',login_required(views.ListUsuarios.as_view()), name='lista_usuario'),
     path('usuarios/actualizar/<int:pk>/',login_required(views.UpdateUsuario.as_view()), name='actualizar_usuario'),



]
