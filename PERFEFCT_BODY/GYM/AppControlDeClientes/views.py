from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from AppControlDeClientes.models import Miembro
from AppControlDeClientes.forms import FormMiembro
from django.contrib import messages
# Create your views here.
def prueba(request):
     return render(request, "layout/index.html")

class LoginFormView(LoginView):
    template_name='AppUsers/pages-login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('prueba')
        return super().dispatch(request, *args, **kwargs)
    


class CreateMiembro(CreateView):
    model = Miembro
    form_class = FormMiembro
    template_name = 'layout/form.html'
    success_url= reverse_lazy('crear_miembro')
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Crear Miembro'
        data['modulo'] = 'Miembro'
        return data