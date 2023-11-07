import json
from django import http
from django.shortcuts import get_object_or_404, render
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
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
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
        
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import FormHistorialMaquinaria  # Asegúrate de importar el formulario adecuado
from .models import HistorialMaquinaria, Maquinaria
from django.contrib import messages
from django.utils import timezone


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
        data['fecha_hoy'] = timezone.now().date()
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
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
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
    
def get_maquina(request, id):

  try:
    maquina = Maquinaria.objects.get(pk=id)
  
  except Maquinaria.DoesNotExist:
    maquina = None
  
  return maquina


#-----------------------------------------AGREGAR NUEVO HISTORIAL DE MÁQUINA---------------------------------------
@csrf_exempt
def agregar_historial_maquinaria(request):
  if request.method == 'POST':

    tipo = request.POST['tipo']
    fecha_ini = request.POST['fecha_ini']
    detalle = request.POST['detalle']

    maquina_id = request.POST['maquinariaID']
    maquina = Maquinaria.objects.get(id=maquina_id)
    if tipo == 'Preventivo':
        maquina.estado_maquina = 'Mantenimiento'
    else:
        maquina.estado_maquina = 'Reparacion'

    print(maquina_id)
    print(tipo)
    print(fecha_ini)
    print(detalle) 

    if maquina:

      historial = HistorialMaquinaria()
      historial.tipo = tipo
      historial.fecha_ini = fecha_ini 
      historial.detalle = detalle
      historial.maquinaria = maquina
      
      maquina.save()
      historial.save() #Esto crea el registro
      
      messages.success(request, 'Historial agregado!')

    else:
      messages.error(request, 'Error al obtener máquina') 

  return redirect('listar_maquina')


#--------------------------------------------CERRAR EL HISTORIAL DE MÁQUINA------------------------------------------
@csrf_exempt
def terminar_historial_maquinaria(request):

  if request.method == 'POST':

    fecha_fin = request.POST['fecha_fin']
    hisotial_id = request.POST['historialID']
    maquina_id = request.POST['maquinaID']

    historial = HistorialMaquinaria.objects.get(id=hisotial_id)
    maquina = Maquinaria.objects.get(id=maquina_id)

    if historial and maquina:
        historial.fecha_fin = fecha_fin
        maquina.estado_maquina = 'Disponible'
        historial.save() #Esto crea el registro
        maquina.save()
        messages.success(request, 'Máquina Disponible!')
    else:
      messages.error(request, 'Error al obtener máquina') 

  return redirect('listar_maquina')


#----------------------------OBTENER EL ID DEL HISTORIAL ABIERTO DE UNA MÁQUINA ESPECÍFICA-------------------------
@csrf_exempt 
def obtener_ultimo_historial(request, id_maquina):
  try:
     # Intenta obtener el historial abierto para la máquina específica
        historial = HistorialMaquinaria.objects.get(maquinaria=id_maquina, fecha_fin=None)
        # Si encontraste un historial abierto, devuelve su ID
        data = {
            'id': historial.id,
            'fecha_ini': historial.fecha_ini.strftime('%Y-%m-%d')  # Convierte el objeto de fecha a formato de cadena
        }
        return JsonResponse(data)
  except HistorialMaquinaria.DoesNotExist:
    return JsonResponse({'error':'No hay historial abierto'}, status=400)

#--------------------------------------------VER HISTORIAL DE LA MAQUINA--------------------------------------------
class ListHistorialMaquina(ListView):
    template_name = 'AppInventarioMaquinaria/Maquinaria/listHistorialMaquinaria.html'  # Ruta a tu plantilla HTML para mostrar el historial
    context_object_name = 'historial'  # Nombre del objeto en el contexto que contiene el historial

    def get_queryset(self):
        # Obten el ID de la máquina desde los parámetros de la URL
        maquina_id = self.kwargs.get('maquina_id')
        # Filtra el historial por el ID de la máquina
        queryset = HistorialMaquinaria.objects.filter(maquinaria=maquina_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega otros datos que necesites en el contexto
        context['empresa'] = Empresa.objects.first()
        context['titulo'] = 'Maquinarias'
        context['titulo2'] = 'Lista'
        context['modulo'] = 'Historial'
        context['icono']  = '<i class="bi bi-plus-lg"></i>'
        return context

@csrf_exempt
def eliminarHistorial(request, pk):
    try:
        historial = get_object_or_404(HistorialMaquinaria, id=pk)
        historial.delete()
        messages.success(request, "¡Historial Eliminado!")
    except HistorialMaquinaria.DoesNotExist:
        messages.error(request, "¡El historial que intentas eliminar no existe!")
    except Exception as e:
        messages.error(request, f"¡Error: {str(e)}")
    return redirect('lista_historial', maquina_id=historial.maquinaria.id)
    