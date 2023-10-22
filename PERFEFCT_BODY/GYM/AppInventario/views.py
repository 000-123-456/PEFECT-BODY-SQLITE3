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
from AppInventario.forms import FormProducto,FormCategoria,FormCompra
from django.core.exceptions import ObjectDoesNotExist
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
        messages.success(self.request, "Máquina añadida correctamente!")
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
        messages.success(self.request, "Máquina añadida correctamente!")
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

class CreateCompra(CreateView):
    model = Compra
    form_class = FormCompra
    success_url= reverse_lazy('crear_compra')
    template_name = 'AppInventario/Compra/createCompra.html'
    success_message = "¡Registro realizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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
     

        messages.success(self.request, "Compra añadida correctamente!")
        #---------------aqui irian los datos que se ingreso
        #---consulta obtener producto
        #--cambio a la cantidad de producto 
        #--sumando cuando compra restando cuando elimina, actualizando restando la cantidad vieja  y sumarle la nueva
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)
    
def get_compra(request, name):
    data = {}
    try:
        comp = Compra.objects.get(nombre=name)
        data = comp.toJSON()
        data['producto'] = str(comp.productoP)
        data['proveedor'] = str(comp.proveedorP)
        data['message'] = 'success'
    except ObjectDoesNotExist:
        data = {'message': 'Compra no encontrada'}
    return JsonResponse(data)


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
    

class ListCompraBajas(ListView):
    model = Compra
    template_name = 'AppInventario/Compra/listCompraBajas.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Compra eliminadas'
        data['modulo'] = 'Compra'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['compras'] = Compra.objects.all()
        data['proveedor'] = Proveedor.objects.filter(estado=1)
        data['productos'] = Producto.objects.filter(estado=1)
        return data
#-------------------------------------------------------
class UpdateCompra(UpdateView):
    model = Compra
    form_class = FormCompra
    success_url= reverse_lazy('lista_compras')
    template_name = 'AppInventario/Compra/updateCompra.html'
    success_message = "¡Compra actualizado con éxito!"
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
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
    
        return super().post(request, *args, **kwargs)
    def form_valid(self, form):
        messages.success(self.request, "Compra añadida correctamente!")
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
    
#-------------------------------------------------------------------------
    
def DeleteCompra(request, pk):
        try:
            compra = Compra.objects.get(id=pk)
            compra.estado = True
            compra.save()
            messages.success(request, "¡Compra eliminada correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_compras')




def AltaCompra(request, pk):
        try:
            compra = Compra.objects.get(id=pk)
            compra.estado = False
            compra.save()
            messages.success(request, "¡Compra restaurada correctamente!")
        except:
            messages.error(request, "¡Error, la accion no se pudo realizar!")
        return redirect(to='lista_baja_compras')



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



class ListCompraBajas(TemplateView):
    model = Compra
    template_name = 'AppInventario/Producto/listCompraBajas.html'
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
        data['modulo'] = 'Proveedor'
        data['compras'] = Compra.objects.filter(estado=1)
        return data
