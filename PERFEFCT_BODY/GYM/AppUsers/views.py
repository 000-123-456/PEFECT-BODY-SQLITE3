from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from AppUsers.forms import RegistroUsuarioForm,FormEmpresa
from django.contrib.auth.views import LoginView
from django.views.generic import  UpdateView,ListView
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from AppUsers.models import Empresa
from django.contrib import messages
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


class ListEmpresa(ListView):
    model = Empresa
    template_name = 'AppUsers/listEmpresa.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Lista de empresas'
        data['modulo'] = 'Empresa'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['empresas'] = Empresa.objects.filter
        return data
   





class UpdateEmpresa(UpdateView):
    model = Empresa
    form_class = FormEmpresa
    success_url= reverse_lazy('lista_empresas')
    template_name = 'AppUsers/Empresa/updateEmpresa.html'
    success_message = "¡Registro actualizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Actualizar empresa'
        data['modulo'] = 'Empresa'
        return data
    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        messages.success(request,'Empresa actualizada correctamente!')
        return super().post(request, *args, **kwargs)