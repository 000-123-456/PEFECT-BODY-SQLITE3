from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from AppUsers.forms import RegistroUsuarioForm
# Create your views here.

class RegistroUsuario(CreateView):
    model = User
    template_name = "AppUsers/signIn.html"
    form_class= RegistroUsuarioForm
    success_url = reverse_lazy('AppControlDeClientes: prueba')