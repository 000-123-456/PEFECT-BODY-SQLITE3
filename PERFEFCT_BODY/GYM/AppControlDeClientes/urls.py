from . import views
from django.urls import path

urlpatterns = [
    path('prueba/',views.prueba, name='prueba'),
    path('login/',views.LoginFormView.as_view(), name='login'),
    path('Miembro/CrearMiembro/',views.CreateMiembro.as_view(), name='crear_miembro'),
]