from django import http
from django.shortcuts import render
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView,TemplateView
from AppInventario.models import *
from django.contrib import messages

from AppInventario.forms import FormProducto,FormCategoria
# Create your views here.

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
                Categoria(nombre=request.POST['nombre']).save()
            elif action == 'update':
               cate = Categoria.objects.get(id=request.POST['id'])
               cate.nombre = request.POST['nombre']
               cate.save()
            else:
                data['error']= 'Ha ocurrido un error'         
        except Exception as e:
            data['error']= str(e)
        return redirect('lista_categoria')
        
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Categorias de productos'
        data['modulo'] = 'Producto'
        data['categorias'] = Categoria.objects.all()
        data['form'] = FormCategoria()
        return data

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
    


class UpdateProducto(UpdateView):
    model = Producto
    form_class = FormProducto
    success_url= reverse_lazy('lista_productos')
    template_name = 'AppInventario/Producto/updateProducto.html'
    success_message = "¡Registro actualizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Actualizar producto'
        data['modulo'] = 'Producto'
        return data
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        messages.success(request, "Producto actualizado correctamente!")
        return super().post(request, *args, **kwargs)
def DeleteProducto(request, pk):
        pro = Producto.objects.get(id=pk)
        pro.estado = True
        pro.save()
        messages.success(request, "Eliminado correctamente!")
        return redirect(to='lista_productos')


