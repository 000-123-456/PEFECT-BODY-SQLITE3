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

#class ListMaquinaria(ListView):
 #   model = Maquinaria
  #  form_class = FormMaquinariaEdit
   # template_name = 'AppInventarioMaquinaria/Maquinaria/listMaquinaria.html'
    #def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
     #   return super().dispatch(request, *args, **kwargs)  
  #  def get_context_data(self, **kwargs):
   #     data = super().get_context_data(**kwargs)
    #    data['empresa'] = Empresa.objects.first()
     #   data['titulo'] = 'Maquinarias'
      #  data['titulo2'] = 'Lista'
       # data['modulo'] = 'Maquinaria'
        #data['icono']  = '<i class="bi bi-plus-lg"></i>'
        #data['maquinas'] = Maquinaria.objects.exclude(estado_maquina='No Disponible')
        #return data
class ListMaquinaria(TemplateView):
    model = Maquinaria
    template_name = 'AppInventarioMaquinaria/Maquinaria/listMaquinaria.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        data={}
        try:
            action=request.POST['action']
            if action == 'add':

                print(request.POST)
                HistorialMaquinaria(opTipoM='Mantenimiento',detalle=request.POST['detalle'],fecha_ini=request.POST['fecha_ini'],fecha_fin=Any,maquinaria_id=request.POST['id']).save()
                messages.success(request, "¡Historial de maquinaria agregado correctamente!")
            else:
                data['error']= 'Ha ocurrido un error'         
        except Exception as e:
            data['error']= str(e)
            return redirect(to='listar_maquina')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['empresa'] = Empresa.objects.first()
        data['titulo'] = 'Maquinarias'
        data['titulo2'] = 'Lista'
        data['modulo'] = 'Maquinaria'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['maquinas'] = Maquinaria.objects.exclude(estado_maquina='No Disponible')
        return data
    
    @csrf_exempt
    def get_historial(request, name):
        data={}
        try:
            data = HistorialMaquinaria.get_historial(name).tojson()
            data['message']='success'
        except:
            data = {'message': 'Not Found'}
        return JsonResponse(data)
        
    
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
    
def agregar_historial_maquinaria(request):
    if request.method == 'POST':
        form = FormInicioHistorialMaquinaria(request.POST)
        if form.is_valid():
            # Obtén la instancia de Maquinaria y asígnala al formulario
            maquinaria_id = request.POST.get('maquinaria')
            maquinaria = Maquinaria.objects.get(pk=maquinaria_id)
            form.instance.maquinaria = maquinaria

            # Asigna un valor específico al campo "tipo"
            # En este ejemplo, asignaremos el valor "Mantenimiento" al campo "tipo"
            form.instance.tipo = 'Mantenimiento'

            # Imprime los valores del formulario
            print("Valores del formulario:")
            print("Detalle:", form.cleaned_data['detalle'])
            print("Fecha de inicio:", form.cleaned_data['fecha_ini'])
            print("Maquinaria ID:", maquinaria_id)  # Imprime el ID de la maquinaria

            # Guarda los datos en la base de datos
            historial = form.save()

             # Agrega un mensaje de éxito
            messages.success(request, "Historial de maquinaria agregado correctamente.")

            return redirect('listar_maquina')  # Redirige a la página de lista de máquinas
        else:
            # El formulario no es válido
            messages.error(request, "Error al agregar el historial de maquinaria. Por favor, verifica los datos.")
    else:
        form = FormHistorialMaquinaria()

    return render(request, '../templates/AppInventarioMaquinaria/Maquinaria/listMaquinaria.html', {'form': form})


