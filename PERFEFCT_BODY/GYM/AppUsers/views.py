from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from AppUsers.forms import RegistroUsuarioForm
from django.contrib.auth.views import LoginView
# Create your views here.
class RegistroUsuario(CreateView):
    model = User
    template_name = "AppUsers/signIn.html"
    form_class= RegistroUsuarioForm
    success_url = reverse_lazy('AppControlDeClientes: prueba')

class LoginFormView(LoginView):
    template_name='AppUsers/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('prueba')
        return super().dispatch(request, *args, **kwargs)
    