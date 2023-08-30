from . import views
from django.urls import path
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('',login_required(views.prueba), name='prueba'),
    
    path('Miembro/CrearMiembro/',views.CreateMiembro.as_view(), name='crear_miembro'),
]