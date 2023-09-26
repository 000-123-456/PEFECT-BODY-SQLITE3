from django import http
from django.shortcuts import render
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core import serializers
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,TemplateView

from AppInventarioMaquinaria.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from AppInventarioMaquinaria.forms import *
# Create your views here.



class CreateMaquinaria(CreateView):
    model = Maquinaria
    form_class = FormMaquinaria
    success_url= reverse_lazy('añadir_maquina')
    template_name = 'AppInventarioMaquinaria/Maquinaria/createMaquinaria.html'
    success_message = "¡Registro realizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['empresa'] = Empresa.objects.first()
        data['titulo'] = 'Máquina'
        data['titulo2'] = 'Añadir'
        data['modulo'] = 'Maquinaria'
        return data
    def form_valid(self, form):
        form.instance.estado_maquina = 'Disponible'
        # Imprime los datos del formulario
        print("Datos del formulario:")
        print("Nombre:", form.cleaned_data['nombre'])
        print("Descripción:", form.cleaned_data['descripcion'])
        print("Categoría:", form.cleaned_data['categoriaM'])
        print("Foto:", self.request.FILES.get('foto'))

        # Guarda el formulario en la base de datos
        messages.success(self.request, "Máquina añadida correctamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Obtener una lista de mensajes de error como texto plano
        error_messages = []
        for field, errors in form.errors.as_text():
            for error in errors:
                error_messages.append(f"{field}: {error}")
        
        # Concatenar todos los mensajes de error en una sola cadena de texto
        error_message = "Error al añadir la máquina. Por favor, verifica los datos: " + ", ".join(error_messages)
        
        # Imprimir los errores en la consola
        print("Errores en el formulario:", error_message)
        
        # Agregar el mensaje de error personalizado a la lista de mensajes de la sesión
        messages.error(self.request, error_message)
        return super().form_invalid(form)

class ListMaquinaria(ListView):
    model = Maquinaria
    form_class = FormMaquinariaEdit
    template_name = 'AppInventarioMaquinaria/Maquinaria/listMaquinaria.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['empresa'] = Empresa.objects.first()
        data['titulo'] = 'Maquinarias'
        data['titulo2'] = 'Lista'
        data['modulo'] = 'Maquinaria'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['maquinas'] = Maquinaria.objects.exclude(estado_maquina='No Disponible')
        return data
    
class ListBajaMaquinaria(ListView):
    model = Maquinaria
    form_class = FormMaquinariaEdit
    template_name = 'AppInventarioMaquinaria/Maquinaria/listaBajaMaquinarias.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['empresa'] = Empresa.objects.first()
        data['titulo'] = 'Maquinarias'
        data['titulo2'] = 'Lista de Eliminadas'
        data['modulo'] = 'Maquinaria'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['maquinas'] = Maquinaria.objects.filter(estado_maquina='No Disponible')
        return data
    
def EliminarMaquinaria(request,pk):
    try:
        maquina = Maquinaria.objects.get(id=pk)
        maquina.estado_maquina = 'No Disponible'
        maquina.save()
        messages.success(request, "¡Máquina eliminada correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='listar_maquina')

def AltaMaquinaria(request,pk):
    try:
        maquina = Maquinaria.objects.get(id=pk)
        maquina.estado_maquina = 'Disponible'
        maquina.save()
        messages.success(request, "¡Máquina dada de alta correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='listar_baja_maquina')

def AltaTodasMaquinaria(request):
    try:
        maquinas = Maquinaria.objects.filter(estado_maquina='No Disponible')
        for maquina in maquinas:
            maquina.estado_maquina = 'Disponible'
            maquina.save()
        messages.success(request, "¡Máquinas dadas de alta correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='listar_maquina')

class UpdateMaquinaria(UpdateView):
    model = Maquinaria
    form_class = FormMaquinaria
    template_name = 'AppInventarioMaquinaria/Maquinaria/actualizarMaquinaria.html'
    success_url= reverse_lazy('listar_maquina')
    success_message = "¡Registro actualizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['empresa'] = Empresa.objects.first()
        data['titulo'] = 'Máquina'
        data['titulo2'] = 'Editar'
        data['modulo'] = 'Maquinaria'
        return data
    def form_valid(self, form):
        # Guarda el formulario en la base de datos
        messages.success(self.request, "Máquina actualizada correctamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Imprime los errores si el formulario no es válido
        print("Errores en el formulario:", form.errors)
        messages.error(self.request, "Error al actualizar la máquina. Por favor, verifica los datos.")
        return super().form_invalid(form)

