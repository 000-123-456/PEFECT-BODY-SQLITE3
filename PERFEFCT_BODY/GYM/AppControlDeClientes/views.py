from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from AppControlDeClientes.models import Miembro,Membresia
from AppControlDeClientes.forms import FormMiembro,FormMembresia
from django.contrib import messages
# Create your views here.
def prueba(request):
     return render(request, "layout/index.html")


    


class CreateMiembro(CreateView):
    model = Miembro
    form_class = FormMiembro
    template_name = 'layout/form.html'
    success_url= reverse_lazy('crear_miembro')
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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
        data['titulo'] = 'Crear membresia'
        data['modulo'] = 'Membresia'
        data['membresias'] = Membresia.objects.filter(estado=0)
        return data
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(request, "Membresia creada correctamente!")
        return super().post(request, *args, **kwargs)

class ListMembresia(ListView):
    model = Membresia
    template_name = 'AppControlDeClientes/Membresia/listMembresia.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
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
        data['titulo'] = 'Actualizar Membresia'
        data['modulo'] = 'Membresia'
        return data
    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        messages.success(request,'Membresia actualizado correctamente!')
        return super().post(request, *args, **kwargs)
    
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
