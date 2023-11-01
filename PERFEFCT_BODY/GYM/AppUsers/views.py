from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from AppUsers.models import User
from django.contrib.auth.forms import UserCreationForm
from AppUsers.forms import RegistroUsuarioForm,FormEmpresa
from django.contrib.auth.views import LoginView
from django.views.generic import  UpdateView,ListView
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from AppUsers.models import Empresa
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from AppControlDeClientes.models import Miembro
from GYM.settings import STATIC_URL
# Create your views here.
def inicioMiembro(request):
    try:
        data = {
            'empresa': Empresa.objects.first(),
            'titulo':"Inicio",
            'modulo':"Home",
            'miembro_datos': Miembro.objects.get(user=request.user),
            }
    except Empresa.DoesNotExist:
        data = {
                    'empresa':{'nombre':'Perfect Body',
                               'logo': '{}{}'.format(STATIC_URL,'assets/img/logo-dark.png')},
                               
        }

    return render(request, "layout/userUI/index.html",data) 
# Create your views here.
class RegistroUsuario(CreateView):
    model = User
    template_name = "AppUsers/User/signIn.html"
    form_class= RegistroUsuarioForm
    success_url = reverse_lazy('registrar_empresa')
    def form_valid(self, form):
        # Registra al usuario y luego inicia sesión
        response = super().form_valid(form)
        user = form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
        return response
    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)

class LoginFormView(LoginView):
    template_name='AppUsers/User/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.rol == 3:
                return redirect('inicio_miembro')
            else:
                return redirect('prueba')
        
        if User.objects.count()==0:
            return redirect('registrar')
        return super().dispatch(request, *args, **kwargs)
    def form_invalid(self, form):
        messages.error(self.request, "Usuario no encontrado. Por favor, verifique sus credenciales e inténtelo de nuevo.")
        return super().form_invalid(form)
    def form_valid(self, form):
        # Realizar la autenticación del usuario
        self.user = form.get_user()
        login(self.request, self.user)

        # Verificar el rol del usuario y redirigir en consecuencia
        if self.user.rol == 3:  # Comprobar si el rol es igual a 3 (miembro)
            return redirect('inicio_miembro')  # Reemplaza 'vista_miembro' con el nombre de la vista a la que deseas redirigir a los miembros
        else:
            return redirect('prueba')  # Reemplaza 'otra_vista' con el nombre de la vista a la que deseas redirigir a otros usuarios autenticados

    
    
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
            return '/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except Empresa.DoesNotExist:
            data['empresa'] = 'Error'
        data['titulo'] = 'Actualizar empresa'
        data['modulo'] = 'Empresa'
        return data
    
