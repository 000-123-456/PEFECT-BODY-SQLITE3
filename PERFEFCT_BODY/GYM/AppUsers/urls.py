from . import views
from django.urls import path

urlpatterns = [
    path('usuario/registrar/',views.RegistroUsuario.as_view(), name='registrar'),
    path('usuario/login/',views.LoginFormView.as_view(), name='login'),
    path('Empresa/registrar/',views.CrearEmpresa.as_view(), name='registrar_empresa'),
]