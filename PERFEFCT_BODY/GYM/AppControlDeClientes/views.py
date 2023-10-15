from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from AppControlDeClientes.models import Miembro,Membresia
from AppControlDeClientes.forms import FormMiembro,FormMembresia
from django.contrib import messages
from AppUsers.models import Empresa,User
from AppUsers.forms import RegistroUsuarioForm
from .op import generar_clave_temporal_segura
from django.core.mail import send_mail
# Create your views here.
def prueba(request):
    try:
        data = {
            'empresa': Empresa.objects.first(),
            
            }
    except:
        data = {
                    'empresa': Empresa.objects.first(),
                    
        }
    return render(request, "layout/index.html",data)



class RegistroMiembroView(CreateView):
    template_name = 'AppControlDeClientes/Miembro/createMiembro.html'
    form_class = FormMiembro
    success_url = reverse_lazy('crear_miembro')
    def form_valid(self, form):
        miembro = form.save()
        user_form = RegistroUsuarioForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(str(generar_clave_temporal_segura()))
            user.username = user.email
            user.save()
            miembro.user = user
            miembro.save()
            # Envía un correo electrónico al usuario con su username y password
            subject = 'Registro exitoso'
            message = f'Se ha registrado exitosamente.\nUsername: {user.username}\nPassword: {user.password}'
            from_email = 'tu@email.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return super().form_valid(form)
        else:

            print(user_form.errors)
            return render(self.request, self.template_name, {'form': form, 'user_form': user_form, 'empresa':Empresa.objects.first(), 'titulo':'Crear Miembro','modulo':'Miembro'})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['miembro_form'] = FormMiembro()  # Formulario de Miembro
        data['user_form'] = RegistroUsuarioForm()  # Formulario de Usuario
        data['titulo'] = 'Crear Miembro'
        data['modulo'] = 'Miembro'
        try:
            data['empresa'] = Empresa.objects.first()
        except Miembro.DoesNotExist:
            data['empresa'] = 'Error'
        return data

class CreateMiembro(CreateView):
    model = Miembro
    form_class = FormMiembro
    template_name = 'layout/form.html'
    success_url= reverse_lazy('crear_miembro')
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Crear Miembro'
        data['modulo'] = 'Miembro'
        return data
    
#---------------------------Membresia-------------------------------------------------------
class CreateMembresia(CreateView):
    model = Membresia
    form_class = FormMembresia
    success_url= reverse_lazy('crear_membresia')
    template_name = 'AppControlDeClientes/Membresia/createMembresia.html'
    success_message = "¡Registro realizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Crear membresia'
        data['modulo'] = 'Membresia'
        data['membresias'] = Membresia.objects.filter(estado=0)
        return data
    
    def form_valid(self, form):
        messages.success(self.request, "Membresia creada correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)

class ListMembresia(ListView):
    model = Membresia
    template_name = 'AppControlDeClientes/Membresia/listMembresia.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Lista de Membresia'
        data['modulo'] = 'Membresia'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['membresias'] = Membresia.objects.filter(estado=0)
        return data
    

class ListMembresiaBajas(ListView):
    model = Membresia
    template_name = 'AppControlDeClientes/Membresia/listMembresiaBajas.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Membresia eliminada'
        data['modulo'] = 'Membresia'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['membresias'] = Membresia.objects.filter(estado=1)
        return data


class UpdateMembresia(UpdateView):
    model = Membresia
    form_class = FormMembresia
    success_url= reverse_lazy('lista_membresias')
    template_name = 'AppControlDeClientes/Membresia/updateMembresia.html'
    success_message = "¡Membresia actualizada con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Actualizar Membresia'
        data['modulo'] = 'Membresia'
        return data
    def form_valid(self, form):
        messages.success(self.request, "Membresia actualizada correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)
    
def DeleteMembresia(request, pk):
    try:
        pro = Membresia.objects.get(id=pk)
        pro.estado = True
        pro.save()
        messages.success(request, "¡Membresia eliminada correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='lista_membresias')



def AltaMembresia(request, pk):
    try:
        pro = Membresia.objects.get(id=pk)
        pro.estado = False
        pro.save()
        messages.success(request, "¡Membresia restaurado correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='lista_bajas_membresias')


def AltaTodosMembresia(request):
    try:
        membresias = Membresia.objects.filter(estado=1)
        for m in membresias:
            m.estado = False
            m.save()
            messages.success(request, "¡Todas las membresias fueron restauradas correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='lista_membresias')

##--------------- FIN VISTAS MEMBRESIA ------------------------------------------
