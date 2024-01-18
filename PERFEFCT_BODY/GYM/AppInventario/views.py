import datetime
from ipaddress import summarize_address_range
import json
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
from django.db.models import F, BooleanField, Case, When, Value
from AppInventario.forms import FormProducto,FormCategoria,FormCompra,FormProveedor
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models import Sum, Count
from datetime import timedelta
from django.utils import timezone
from flask import Flask, request, jsonify

from AppControlDeClientes.mixins import isAdministradorOrEmpleadoMixin
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
                try: 
                    Categoria(nombre=request.POST['nombre'],perecedero=perecedero_res).save()
                    messages.success(request,"Categoría agregada correctamente")
                except Exception as e:
                    messages.error(request,"Ya existe una categoría con el mismo nombre")
            elif action == 'update':
               print(request.POST['id'])
               cate = Categoria.objects.get(id=request.POST['id'])
               perecedero_res=False
               
               if 'perecedero' in request.POST:
                    perecedero_res=True
               try:
                    cate.nombre = request.POST['nombre']
                    cate.perecedero = perecedero_res
                    cate.save()
                    messages.success(request,"Categoría modificada correctamente")
               except Exception as e:
                    messages.error(request,"Ya existe una categoría con el mismo nombre")
            else:
                data['error']= 'Ha ocurrido un error'         
        except Exception as e:
            data['error']= str(e)
        return redirect('lista_categoria')
        
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
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
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
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
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Crear producto'
        data['modulo'] = 'Producto'
        data['categorias'] = Categoria.objects.filter(estado=0)
        return data
    
    def form_valid(self, form):
        messages.success(self.request, "producto añadido correctamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)
    
def get_producto(request, name):
    data={}
    try:
        product = Producto.objects.get(nombre=name)
        data = product.toJSON()
        data['categoria'] = str(product.categoriaP)
        data['img'] = str(product.get_image())
        data['message']= 'success'
    except Exception as e :
        data = {'message': 'Not Found'}
        print(e)
    return JsonResponse(data)

class ListProducto(ListView):
    model = Producto
    template_name = 'AppInventario/Producto/listProducto.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
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
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
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
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Actualizar producto'
        data['modulo'] = 'Producto'
        return data
    
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, "Producto añadido correctamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Obtiene la instancia del modelo que se está actualizando
        instance = self.get_object()
        
        # Envía el objeto instance como contexto a la plantilla
        context = self.get_context_data(object=instance)
        
        # Agrega mensajes de error al contexto
        messages.error(self.request, format(form.errors.as_text()))
        
        # Retorna la respuesta con el contexto actualizado
        return self.render_to_response(context)
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

##-------------------------------------------------------------------------------------------------
##-----------------------------COMPRAS-------------------------------------------------------------
from django.db.models import F
from django.shortcuts import get_object_or_404
from datetime import date, timezone

class CreateCompra(CreateView):
    model = Compra
    form_class = FormCompra
    success_url = reverse_lazy('crear_compra')
    template_name = 'AppInventario/Compra/createCompra.html'
    success_message = "¡Registro realizado con éxito!"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Crear compra'
        data['modulo'] = 'Compra'
        data['compras'] = Compra.objects.all()
        data['producto'] = Producto.objects.filter(estado=0)
        data['proveedor'] = Proveedor.objects.filter(estado=0)
        return data
    

    def form_valid(self, form):
       # --------------Obtengo el producto seleccionado en la compra
        producto = form.cleaned_data['producto']
        #----------- Recupero la cantidad comprada en la compra
        cantidad_comprada = form.cleaned_data['cantidad']

             
        # Verifica si el producto pertenece a una categoría perecedera
        if producto.categoriaP.perecedero:


            # Si es perecedero, asegúrate de que la fecha de vencimiento no esté vacía
            fecha_vec = form.cleaned_data['fecha_vec']
            if not fecha_vec:
                messages.error(self.request, "Fecha de Vencimiento: este campo es obligatorio.")
                return super().form_invalid(form) 
            
                # Verifica si la fecha de vencimiento es anterior a la fecha actual
            if fecha_vec < date.today():
                messages.error(self.request, "Fecha de Vencimiento: debe ser una fecha futura.")
                return super().form_invalid(form)
         

        # --------------Actualizo la cantidad de productos en stock sumando la cantidad comprada
        Producto.objects.filter(id=producto.id).update(cantidad=F('cantidad') + cantidad_comprada)
        # -------------Obténgo la cantidad comprada y el precio unitario del formulario
     
        precio_unitario = form.cleaned_data['precio_unitario']
        total_compra = cantidad_comprada * precio_unitario   


        
        
        # ********************************************************  
        form.instance.total = total_compra
        # ------------- Guardo el objeto de compra en la base de datos
        form.save()

        messages.success(self.request, "Compra añadida correctamente!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)

def get_compra(request, id):
    data = {}
    try:
        comp = Compra.objects.get(id=id)
        data = comp.toJSON()
        data['producto'] = str(comp.producto)
        data['proveedor'] = str(comp.proveedor)
        data['message'] = 'success'
    except ObjectDoesNotExist:
        data = {'message': 'Compra no encontrada'}
    return JsonResponse(data)
    
##*******************************************LISTA***********************************************
class ListCompra(ListView):
    model = Compra
    template_name = 'AppInventario/Compra/listCompra.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Lista de Compra'
        data['modulo'] = 'Compra'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['compras'] = Compra.objects.all()
        data['producto'] = Producto.objects.filter(estado=0)
        data['proveedor'] = Proveedor.objects.filter(estado=0)
        return data
    
#**********************************************************************************************
class ListCompraBajas(ListView):
    model = Compra
    template_name = 'AppInventario/Compra/listCompraBajas.html'
    context_object_name = 'compras'  # Establece el nombre del objeto en el contexto

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Compras Eliminadas'
        data['modulo'] = 'Compra'
        data['icono'] = '<i class="bi bi-plus-lg"></i>'

             # Filtra las compras eliminadas basadas en el estado del producto
        data['compras'] = Compra.objects.annotate(
            producto_estado=Case(
                When(producto__estado=True, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            )
        ).filter(producto_estado=False)

        data['proveedores'] = Proveedor.objects.filter(estado=1)  # Filtra proveedores activos
        data['productos'] = Producto.objects.filter(estado=1)  # Filtra productos activos

        return data


#*************************************************************************************************
class UpdateCompra(UpdateView):
   

    model = Compra
    form_class = FormCompra
    success_url = reverse_lazy('lista_compras')
    template_name = 'AppInventario/Compra/updateCompra.html'
    success_message = "¡Compra actualizado con éxito!"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Actualizar compra'
        data['modulo'] = 'Compra'
        data['compras'] = Compra.objects.all()
        
        return data

    def form_valid(self, form):
        # ********Obténgo la instancia de la compra que se está actualizando
        compra = self.object

        # ********Obténgo el producto relacionado con la compra
        producto = compra.producto

        # ******* consulta a la base de datos para obtener el valor original de la cantidad de producto
        cantidad_anterior = Producto.objects.get(pk=producto.pk).cantidad

        #****** Actualizo la cantidad de inventario del producto
        diferencia_cantidad = form.cleaned_data['cantidad'] - cantidad_anterior
        producto.cantidad += diferencia_cantidad
        producto.save()

          # Verifica si el producto pertenece a una categoría perecedera
        if producto.categoriaP.perecedero:
            # Asegúrate de que la fecha de vencimiento no esté vacía
            fecha_vec = form.cleaned_data['fecha_vec']
            if not fecha_vec:
                messages.error(self.request, "Fecha de Vencimiento: este campo es obligatorio.")
                return super().form_invalid(form)

            # Verifica si la fecha de vencimiento es anterior a la fecha actual
            if fecha_vec < date.today():
                messages.error(self.request, "Fecha de Vencimiento: debe ser una fecha futura.")
                return super().form_invalid(form)

        #***************************************** Calcula el nuevo total******************************************
        form.instance.total = form.cleaned_data['cantidad'] * form.cleaned_data['precio_unitario']

       
         

        messages.success(self.request, "Compra actualizada correctamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        instance = self.get_object()
        context = self.get_context_data(object=instance)
        messages.error(self.request, format(form.errors.as_text()))
        return self.render_to_response(context)



    
#-------------------------------------------------------------------------

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Compra

from django.db import transaction

@transaction.atomic
def DeleteCompra(request, pk):
    try:
        
        compra = Compra.objects.get(id=pk)
        producto = compra.producto

    
        producto.cantidad -= compra.cantidad
        producto.save()

      
        compra.delete()

        messages.success(request, "¡Compra eliminada correctamente!")
    except Compra.DoesNotExist:
        messages.error(request, "¡Error, la compra no se pudo encontrar!")
    except Exception as e:
        messages.error(request, f"¡Error, la acción no se pudo realizar! {str(e)}")

    return redirect(to='lista_compras')




#******************************************************************************
def AltaCompra(request, pk):
    try:
        compra = Compra.objects.get(id=pk)
        
        # Verifica el estado del producto asociado
        if compra.producto.estado:
            messages.error(request, "¡Error, el producto asociado ya está activo!")
        else:
            compra.producto.estado = True  # Cambia el estado del producto a activo
            compra.producto.save()
            compra.estado = True  # Cambia el estado de eliminado a activo
            compra.save()
            messages.success(request, "¡Compra restaurada correctamente!")
        
    except Compra.DoesNotExist:
        messages.error(request, "¡Error, la compra no se pudo encontrar!")
    except Exception as e:
        messages.error(request, "¡Error, la acción no se pudo realizar!")

    return redirect(to='lista_baja_compras')


#*********************************************************************************



def AltaTodasCompra(request):
        try:
            compras = Compra.objects.filter(estado=1)
            for c in compras:
                c.estado = False
                c.save()
            messages.success(request, "¡Todas las compras fueron restauradas correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_compras')



#------------------------------------------------------------OBTENER IMAGEN
# views.py
from django.http import JsonResponse

def Obtenerimagenpro(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        imagen_url = producto.get_image()  # Asume que existe un método get_image en tu modelo Producto
        return JsonResponse({'imagen_url': imagen_url})
    except Producto.DoesNotExist:
        return JsonResponse({'imagen_url': None})

#------------------------------------------------------------OBTENER SI EL PRODUCTO VENCE O NO

from django.http import JsonResponse

def Categoriaproducto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        data = {'perecedero': producto.categoriaP.perecedero}
        return JsonResponse(data)
    except Producto.DoesNotExist:
        data = {'perecedero': False}
        return JsonResponse(data)
    
class CreateProveedor(isAdministradorOrEmpleadoMixin,CreateView):
    model = Proveedor
    form_class = FormProveedor
    success_url= reverse_lazy('crear_proveedor')
    template_name = 'AppInventario/Proveedor/createProveedor.html'
    success_message = "¡Registro realizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Crear proveedor'
        data['modulo'] = 'Proveedor'
        return data
    
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, "Proveedor añadido correctamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Obtiene la instancia del modelo que se está actualizando
        instance = self.get_object()
        
        # Envía el objeto instance como contexto a la plantilla
        context = self.get_context_data(object=instance)
        
        # Agrega mensajes de error al contexto
        messages.error(self.request, format(form.errors.as_text()))
        
        # Retorna la respuesta con el contexto actualizado
        return self.render_to_response(context)
    
class ListProveedor(isAdministradorOrEmpleadoMixin,ListView):
    model = Proveedor
    template_name = 'AppInventario/Proveedor/listaProveedor.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Lista de proveedores'
        data['modulo'] = 'Proveedor'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['proveedores'] = Proveedor.objects.filter(estado=0)
        return data
class ListProveedorBajas(isAdministradorOrEmpleadoMixin,ListView):
    model = Proveedor
    template_name = 'AppInventario/Proveedor/listaProveedorBajas.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Proveedores eliminados'
        data['modulo'] = 'Proveedor'
        data['proveedores'] = Proveedor.objects.filter(estado=1)
        return data

def DeleteProveedor(request, pk):
        try:
            proveedor = Proveedor.objects.get(id=pk)
            proveedor.estado = True
            proveedor.save()
            messages.success(request, "¡Proveedor eliminado correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_proveedor')

def AltaProveedor(request, pk):
        try:
            proveedor = Proveedor.objects.get(id=pk)
            proveedor.estado = False
            proveedor.save()
            messages.success(request, "¡Proveedor restaurado correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_bajas_proveedor')

def AltaTodosProveedor(request):
        try:
            proveedores = Proveedor.objects.filter(estado=1)
            for p in proveedores:
                p.estado = False
                p.save()
            messages.success(request, "¡Todos los proveedores fueron restaurados correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_proveedor')

class UpdateProveedor(isAdministradorOrEmpleadoMixin,UpdateView):
    model = Proveedor
    form_class = FormProveedor
    success_url= reverse_lazy('lista_proveedor')
    template_name = 'AppInventario/Proveedor/updateProveedor.html'
    success_message = "¡Proveedor actualizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Actualizar proveedor'
        data['modulo'] = 'Proveedor'
        return data
    
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, "Proveedor actualizado correctamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Obtiene la instancia del modelo que se está actualizando
        instance = self.get_object()
        
        # Envía el objeto instance como contexto a la plantilla
        context = self.get_context_data(object=instance)
        
        # Agrega mensajes de error al contexto
        messages.error(self.request, format(form.errors.as_text()))
        
        # Retorna la respuesta con el contexto actualizado
        return self.render_to_response(context)
    
class CreateVenta(isAdministradorOrEmpleadoMixin,TemplateView):
    template_name = 'AppInventario/Venta/registroVenta.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Registro de venta'
        data['titulo2'] = 'Registro'
        data['modulo'] = 'Ventas'
        return data
    
    
def lista_productos(request):
    q = request.GET.get('q') # obtener término de búsqueda
    try:
        if q is not None:
            # Filtrar por nombre o apellido que contenga q
            productos = Producto.objects.filter(
                Q(nombre__icontains=q) | Q(descripcion__icontains=q) | Q(categoriaP__nombre__icontains=q), estado=False, cantidad__gt=0
            )
        else:
            productos = Producto.objects.filter(estado=False, cantidad__gt=0)

        # Serializa los objetos Producto a una lista de diccionarios
        productos_list = [
            {
                'id': producto.id,
                'nombre': producto.nombre,
                'descripcion': producto.descripcion,
                'foto': producto.get_image(),
                'precio': producto.precio_venta,
                'cantidad': producto.cantidad,
            }
            for producto in productos
        ]
        
        # Devuelve la lista de productos como JSON
        return JsonResponse(productos_list, safe=False)
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'No hay productos'}, status=400)

    

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#def registrar_venta recibiendo un array de productos data: JSON.stringify({ carrito: data }),
@csrf_exempt
def registro_venta(request):
    if request.method == 'POST':
        try:
            # Obtén los datos JSON del cuerpo de la solicitud
            data = json.loads(request.body.decode('utf-8'))
            
            emple = User.objects.get(id=request.user.id)
            venta = Venta( total=0, empleado = emple)
            venta.save()

            # Procesa los datos del carrito
            totalVenta = 0
            for item in data['carrito']:
                # Realiza las operaciones necesarias con cada item (por ejemplo, guarda en la base de datos)
                print(item)
                producto = Producto.objects.get(id=item['id'])
                producto.cantidad -= item['cantidad']
                producto.save()

                detalle = LineaVenta( cantidad=item['cantidad'], precio_vendido=item['precio'], subtotal=item['subtotal'], venta=venta, producto=producto)
                detalle.save()
                totalVenta += item['subtotal']

            venta.total = totalVenta
            venta.save()
            # Puedes devolver una respuesta JSON exitosa
            messages.success(request, 'Venta realizada con éxito')
        except json.JSONDecodeError as e:
            messages.error(request, "¡No se pudo realizar la venta!")
    return JsonResponse({'message': 'success'})

#*************************************************************************************************
class ListVenta(isAdministradorOrEmpleadoMixin,ListView):
    model = Venta
    template_name = 'AppInventario/Venta/listVentas.html'
    context_object_name = 'ventas'  # Establece el nombre del objeto en el contexto

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Lista de ventas'
        data['modulo'] = 'Ventas'
        data['icono'] = '<i class="bi bi-plus-lg"></i>'

         # Get the current date and time in the local timezone
        now = datetime.datetime.now()
        # Filtra las ventas eliminadas basadas en el estado del producto
        ventas = Venta.objects.filter(fecha_venta__month=now.month)
        # Calcula el total sumado de las ventas este mes
        total_ventas_mes = ventas.aggregate(Sum('total'))['total__sum']
        data['total_ventas_mes'] = total_ventas_mes if total_ventas_mes else 0.00

        #calcular la suma para el dia de hoy
        ventas = Venta.objects.filter(fecha_venta__day=now.day)
        total_ventas_dia = ventas.aggregate(Sum('total'))['total__sum']
        data['total_ventas_hoy'] = total_ventas_dia if total_ventas_dia else 0.00


        # Filtra las ventas eliminadas basadas en el estado del producto
        data['ventas'] = Venta.objects.all().reverse()

        return data

#lista de linea de venta por el id de la venta
@csrf_exempt
def get_productosVendidos(request, venta_id):
    try:
        venta = Venta.objects.get(id=venta_id)
        lineas_venta = LineaVenta.objects.filter(venta=venta)
        lineas_venta_list = [
            {
                'id': linea_venta.id,
                'producto': linea_venta.producto.nombre,
                'cantidad': linea_venta.cantidad,
                'precio_vendido': linea_venta.precio_vendido,
                'subtotal': linea_venta.subtotal,
            }
            for linea_venta in lineas_venta
        ]
        return JsonResponse(lineas_venta_list, safe=False)
    except Venta.DoesNotExist:
        return JsonResponse({'error': 'No hay ventas'}, status=400)
    

#metodo para eliminar una venta, se eliminan todas las lineas de venta asociadas a la venta y se restaura el stock de los productos
@csrf_exempt
def eliminar_venta(request, venta_id):
    try:
        venta = Venta.objects.get(id=venta_id)
        lineas_venta = LineaVenta.objects.filter(venta=venta)
        for linea_venta in lineas_venta:
            producto = linea_venta.producto
            producto.cantidad += linea_venta.cantidad
            producto.save()
            linea_venta.delete()
        venta.delete()
        messages.success(request, 'Venta eliminada con éxito')
    except json.JSONDecodeError as e:
            messages.error(request, "¡No se pudo realizar la eliminación!")
    return redirect(to='lista_venta')