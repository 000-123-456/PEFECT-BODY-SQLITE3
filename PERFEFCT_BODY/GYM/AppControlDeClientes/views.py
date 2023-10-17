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
from GYM.settings import EMAIL_HOST_USER
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
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
        # 1. Validación de fecha de nacimiento
        miembro = form.save(commit=False)
        miembro_fecha_nacimiento = miembro.fecha_nac
        fecha_actual = timezone.now().date()
        user_form = RegistroUsuarioForm(self.request.POST)
        if miembro_fecha_nacimiento >= fecha_actual:
            messages.error(self.request, "La fecha de nacimiento debe ser anterior a la fecha actual.")
            return render(self.request, self.template_name, {'form': form, 'user_form': user_form, 'empresa':Empresa.objects.first(), 'titulo':'Crear Miembro','modulo':'Miembro'})
        
        # 2. Validación de usuario existente
        if not user_form.is_valid():
            print(user_form.errors)
            return render(self.request, self.template_name, {'form': form, 'user_form': user_form, 'empresa':Empresa.objects.first(), 'titulo':'Crear Miembro','modulo':'Miembro'})

        user = user_form.save(commit=False)
        clave = str(generar_clave_temporal_segura())
        user.set_password(clave)
        user.username = user.email
        user.rol=3
        try:
            user.empresa = Empresa.objects.first()
        except Empresa.DoesNotExist:
            empresa = 'Error'
        try:
            # 3. Validación de usuario guardado correctamente
            user.save()
        except IntegrityError:
            messages.error(self.request, "El nombre de usuario ya existe. Por favor, elija otro nombre de usuario.")
            return render(self.request, self.template_name, {'form': form, 'user_form': user_form, 'empresa':Empresa.objects.first(), 'titulo':'Crear Miembro','modulo':'Miembro'})

        # Si pasa todas las validaciones, guarda el miembro
        miembro.user = user
        miembro.save()
            # Envía un correo electrónico al usuario con su username y password
        subject = 'Registro exitoso'
        message = f'Se ha registrado exitosamente.\nUsuario: {user.username}\nContraseña: {clave}\nIngrese al siguiente link: http://127.0.0.1:8000/'
        from_email = EMAIL_HOST_USER
        recipient_list = [user.username]
        send_mail(subject, message,from_email, recipient_list)
        messages.success(self.request, "Miembro registrado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['miembro_form'] = FormMiembro()  # Formulario de Miembro
        data['user_form'] = RegistroUsuarioForm()  # Formulario de Usuario
        data['titulo'] = 'Registrar Miembro'
        data['modulo'] = 'Miembro'
        try:
            data['empresa'] = Empresa.objects.first()
        except Empresa.DoesNotExist:
            data['empresa'] = 'Error'
        return data

class ListMiembro(ListView):
    model = Miembro
    template_name = 'AppControlDeClientes/Miembro/listMiembro.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Lista de miembros'
        data['modulo'] = 'Miembro'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['miembros'] = Miembro.objects.select_related('user')
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
