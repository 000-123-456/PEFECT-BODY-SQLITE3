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
]
