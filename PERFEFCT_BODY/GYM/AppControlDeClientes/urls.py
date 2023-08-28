from . import views
from django.urls import path

urlpatterns = [
    path('prueba/',views.prueba, name='prueba'),
    
    path('Miembro/CrearMiembro/',views.CreateMiembro.as_view(), name='crear_miembro'),
]