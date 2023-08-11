from . import views
from django.urls import path

urlpatterns = [
    path('usuarios/registrar/',views.RegistroUsuario.as_view(), name='registrar'),
]