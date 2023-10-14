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


from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

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





#class UpdateEmpresa(UpdateView):
 #   model = Empresa
  #  form_class = FormEmpresa
   # success_url= reverse_lazy('lista_empresas')
    #template_name = 'AppUsers/Empresa/updateEmpresa.html'
    #success_message = "¡Registro actualizado con éxito!"
    #def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
     #   return super().dispatch(request, *args, **kwargs)  
    #def get_context_data(self, **kwargs):
     #   data = super().get_context_data(**kwargs)
      #  data['empresa'] = Empresa.objects.first()
       # data['titulo'] = 'Actualizar empresa'
        #data['modulo'] = 'Empresa'
        #return data
    #def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        #messages.success(request,'Empresa actualizada correctamente!')
        #return super().post(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class UpdateEmpresa(UpdateView):
    model = Empresa
    form_class = FormEmpresa
    template_name = 'AppUsers/Empresa/updateEmpresa.html'
    success_message = "¡Registro actualizado con éxito!"

    def get_success_url(self):
        try:
            emp = Empresa.objects.first()
            url = '/Empresa/ActualizarEmpresas/' + str(emp.id) + '/'
            return url
        except Empresa.DoesNotExist:
            # En caso de que no se encuentre una empresa, redirigir a otra URL
            return '/otra_url/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except Empresa.DoesNotExist:
            data['empresa'] = 'Error'
        data['titulo'] = 'Actualizar empresa'
        data['modulo'] = 'Empresa'
        return data
    
