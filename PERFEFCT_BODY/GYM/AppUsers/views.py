from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from AppUsers.forms import RegistroUsuarioForm,FormEmpresa
from django.contrib.auth.views import LoginView
from AppUsers.models import Empresa
# Create your views here.
class RegistroUsuario(CreateView):
    model = User
    template_name = "AppUsers/User/signIn.html"
    form_class= RegistroUsuarioForm
    success_url = reverse_lazy('prueba')

class LoginFormView(LoginView):
    template_name='AppUsers/User/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('prueba')
        return super().dispatch(request, *args, **kwargs)
    
#-------------------------------------------------EMPRESA-----------------------------

class CrearEmpresa(CreateView):
    model = Empresa
    template_name = 'AppUsers/Empresa/createEmpresa.html'
    form_class= FormEmpresa
    success_url = reverse_lazy('prueba')