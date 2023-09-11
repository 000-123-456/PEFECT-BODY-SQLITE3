from django import http
from django.shortcuts import render
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core import serializers
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,TemplateView
from AppInventario.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from AppInventario.forms import FormProducto,FormCategoria
# Create your views here.


##--------------- IINICIO VISTAS CATEGORIA ------------------------------------------
class ListCategoria(TemplateView):
    model = Categoria
    template_name = 'AppInventario/Producto/listCategoria.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        data={}
        try:
            action= request.POST['action']
            if action == 'add':
                perecedero_res=False
                if 'perecedero' in request.POST:
                    perecedero_res=True
                print(request.POST)
                Categoria(nombre=request.POST['nombre'],perecedero=perecedero_res).save()
                messages.success(request,"¡Categoría agregada correctamente!")
            elif action == 'update':
               print(request.POST['id'])
               cate = Categoria.objects.get(id=request.POST['id'])
               perecedero_res=False
               if 'perecedero' in request.POST:
                    perecedero_res=True
               cate.nombre = request.POST['nombre']
               cate.perecedero = perecedero_res
               cate.save()
               messages.success(request,"¡Categoría modificada correctamente!")
            else:
                data['error']= 'Ha ocurrido un error'         
        except Exception as e:
            data['error']= str(e)
        return redirect('lista_categoria')
        
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Listado de categorías'
        data['modulo'] = 'Producto'
        data['categorias'] = Categoria.objects.filter(estado=0)
        data['form'] = FormCategoria()
        return data
@csrf_exempt
def get_categoria(request, name):
    data={}
    try:
        data = Categoria.objects.get(nombre=name).toJSON()
        data['message']= 'success'
    except:
        data = {'message': 'Not Found'}
    return JsonResponse(data)

def DeleteCategoria(request, pk):
        try:
            categoria = Categoria.objects.get(id=pk)
            categoria.estado = True
            categoria.save()
            messages.success(request, "¡Categoría eliminada correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_categoria')

def AltaCategoria(request, pk):
        try:
            categoria = Categoria.objects.get(id=pk)
            categoria.estado = False
            categoria.save()
            messages.success(request, "¡Categoría restaurada correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_baja_categoria')

def AltaTodasCategoria(request):
        try:
            categorias = Categoria.objects.filter(estado=1)
            for c in categorias:
                c.estado = False
                c.save()
            messages.success(request, "¡Todas las categorías fueron restauradas correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_categoria')

class ListCategoriaBajas(TemplateView):
    model = Categoria
    template_name = 'AppInventario/Producto/listCategoriaBajas.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Categorías eliminadas'
        data['modulo'] = 'Producto'
        data['categorias'] = Categoria.objects.filter(estado=1)
        return data

##--------------- FIN VISTAS CATEGORIA ------------------------------------------


##--------------- INICIO VISTAS PRODUCTO ------------------------------------------
class CreateProducto(CreateView):
    model = Producto
    form_class = FormProducto
    success_url= reverse_lazy('crear_producto')
    template_name = 'AppInventario/Producto/createProducto.html'
    success_message = "¡Registro realizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Crear producto'
        data['modulo'] = 'Producto'
        data['categorias'] = Categoria.objects.filter(estado=0)
        return data
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(request, "Producto creado correctamente!")
        return super().post(request, *args, **kwargs)
    

class ListProducto(ListView):
    model = Producto
    template_name = 'AppInventario/Producto/listProducto.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Lista de producto'
        data['modulo'] = 'Producto'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['productos'] = Producto.objects.filter(estado=0)
        return data
class ListProductoBajas(ListView):
    model = Producto
    template_name = 'AppInventario/Producto/listProductoBajas.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Producto eliminados'
        data['modulo'] = 'Producto'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['productos'] = Producto.objects.filter(estado=1)
        return data


class UpdateProducto(UpdateView):
    model = Producto
    form_class = FormProducto
    success_url= reverse_lazy('lista_productos')
    template_name = 'AppInventario/Producto/updateProducto.html'
    success_message = "¡Producto actualizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Actualizar producto'
        data['modulo'] = 'Producto'
        return data
    def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        messages.success(request,'¡Producto actualizado correctamente!')
        return super().post(request, *args, **kwargs)
    
def DeleteProducto(request, pk):
    try:
        pro = Producto.objects.get(id=pk)
        pro.estado = True
        pro.save()
        messages.success(request, "¡Producto eliminado correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='lista_productos')

def AltaProducto(request, pk):
    try:
        pro = Producto.objects.get(id=pk)
        pro.estado = False
        pro.save()
        messages.success(request, "¡Producto restaurado correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='lista_bajas_productos')

def AltaTodosProducto(request):
    try:
        productos = Producto.objects.filter(estado=1)
        for p in productos:
            p.estado = False
            p.save()
            messages.success(request, "¡Todos los productos fueron restaurados correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='lista_productos')

##--------------- FIN VISTAS PRODUCTO ------------------------------------------
