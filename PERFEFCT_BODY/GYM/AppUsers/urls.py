from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('usuario/registrar/',views.RegistroUsuario.as_view(), name='registrar'),
    path('usuario/login/',views.LoginFormView.as_view(), name='login'),
    path('Empresa/registrar/',views.CrearEmpresa.as_view(), name='registrar_empresa'),
    path('Empresa/ActualizarEmpresas/<int:pk>/', login_required(views.UpdateEmpresa.as_view()), name='actualizar_empresa'),

]
