
import json
from typing import Any
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from AppControlDeClientes.models import HistorialMiembro, Miembro,Membresia,VentaMembresia, Asistencia
from AppControlDeClientes.forms import FormMiembro,FormMembresia, FormHistorialMiembro, FormAsistenciaMiembro
from django.contrib import messages
from AppUsers.models import Empresa,User
from AppUsers.forms import RegistroUsuarioForm
from .op import generar_clave_temporal_segura
from django.core.mail import send_mail
from GYM.settings import EMAIL_HOST_USER
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from .funciones import calcular_edad, calcular_fecha_final, getCantidadVentas, obtener_url_imagen,vencimientoMembresias,getVentasMensuales
import locale
from django.db.models import Sum, Count
from datetime import date
from datetime import timedelta
from django.db.models import Q
from fuzzywuzzy import process
from django.views.decorators.csrf import csrf_exempt

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


#*************************Miembro****************************************
class RegistroMiembroView(CreateView):
    template_name = 'AppControlDeClientes/Miembro/createMiembro.html'
    form_class = FormMiembro
    success_url = reverse_lazy('crear_miembro')
    def form_valid(self, form):
        if not self.request.FILES.get('foto'):
            genero = form.cleaned_data.get('genero')  # Asume que tu formulario tiene un campo 'genero'
            url_imagen_aleatoria = obtener_url_imagen(genero)
            form.instance.foto = url_imagen_aleatoria
        
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
    def form_invalid(self, form):
        # Lógica para el formulario inválido
       
        user_form = RegistroUsuarioForm(data=self.request.POST)
        context = self.get_context_data()
        context['form'] = form
        context['user_form'] = user_form
        return self.render_to_response(context)
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
    


class ActualizarMiembroView(UpdateView):
    model = Miembro
    form_class = FormMiembro
    template_name = 'AppControlDeClientes/Miembro/updateMiembro.html'
    success_url = reverse_lazy('lista_miembros')  # Puedes cambiarlo si es necesario

    def form_valid(self, form):
        
        miembro = form.save(commit=False)
        miembro_fecha_nacimiento = miembro.fecha_nac
        fecha_actual = timezone.now().date()

        if miembro_fecha_nacimiento >= fecha_actual:
            messages.error(self.request, "La fecha de nacimiento debe ser anterior a la fecha actual.")
            return render(self.request, self.template_name, {'form': form, 'empresa': Empresa.objects.first(), 'titulo': 'Crear Miembro', 'modulo': 'Miembro'})

        user_form = RegistroUsuarioForm(self.request.POST, instance=miembro.user)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            try:
                user.empresa = Empresa.objects.first()
            except Empresa.DoesNotExist:
                empresa = 'Error'
            user.username = user.email
            email = user.email
            print(email)
            email_viejo = Miembro.objects.get(user=self.object.user).user.email
            respuesta = email_viejo==email
            miembro.user = user
            try:
            # 3. Validación de usuario guardado correctamente
                    user.save()
            except IntegrityError:
                    messages.error(self.request, "El nombre de usuario ya existe. Por favor, elija otro nombre de usuario.")
                    return render(self.request, self.template_name, {'form': form, 'user_form': user_form, 'empresa':Empresa.objects.first(), 'titulo':'Crear Miembro','modulo':'Miembro'})
            
            
            miembro.save()
            print(email_viejo)
            if not respuesta:
                subject = 'Actualización exitosa'
                message = f'Se ha actualizado exitosamente.\nUsuario nuevo: {user.username}\nIngrese al siguiente link: http://127.0.0.1:8000/'
                from_email = EMAIL_HOST_USER
                recipient_list = [user.username]
                send_mail(subject, message, from_email, recipient_list)

            messages.success(self.request, "Miembro actualizado")
            return super().form_valid(form)
        else:
            messages.error(self.request, "El formulario de usuario no es válido. Por favor, corrige los errores.")
            return render(self.request, self.template_name, {'form': form, 'user_form': user_form, 'empresa': Empresa.objects.first(), 'titulo': 'Crear Miembro', 'modulo': 'Miembro'})
    def form_invalid(self, form):
        # Lógica para el formulario inválido
        user_form = RegistroUsuarioForm(data=self.request.POST)
        context = self.get_context_data()
        context['form'] = form
        context['user_form'] = user_form
        return self.render_to_response(context)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['miembro_form'] = data['form']
        fecha_nac = self.object.fecha_nac.strftime('%Y-%m-%d')  # Cambia '/' por '-' si es necesario
        data['miembro_form'].initial['fecha_nac'] = fecha_nac
        data['user_form'] = RegistroUsuarioForm(instance=self.object.user)  # Rellenar el formulario de usuario con la instancia del usuario
        data['titulo'] = 'Actualizar Miembro'
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
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        data['fecha'] = timezone.localtime(timezone.now()).date()
        vencimientoMembresias()
        data['miembros'] = Miembro.objects.filter(estado=0).order_by('-id')
        data['membresias'] = Membresia.objects.filter(estado=0)
        return data
class ListMiembroEliminados(ListView):
    model = Miembro
    template_name = 'AppControlDeClientes/Miembro/listMiembroBajas.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        data['titulo'] = 'Miembros eliminados'
        data['modulo'] = 'Miembros'
        data['miembros'] = Miembro.objects.filter(estado=1).order_by('-id')
        return data
def get_miembro(request, username):
    data={}
    try:
        user = User.objects.get(username=username)
        miembro = Miembro.objects.get(user=user.id)
        data = miembro.toJSON()
        data['nombre'] = str(user.first_name) +" "+ str(user.last_name)
        data['edad'] = str(miembro.calcular_edad())
        if miembro.genero==1:
            data['genero'] = 'Masculino'
        else:
            data['genero'] = 'Femenino' 
        
        data['foto'] = str(miembro.get_image())
        if miembro.fecha_fin:
            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') 
            data['fecha_fin'] = miembro.fecha_fin.strftime('%d de %B de %Y')
        data['email']= str(miembro.user.email)
        data['message']= 'success'
    except Exception as e :
        print(e)
        data = {'message': 'Not Found'}
       
    return JsonResponse(data)

def baja_miembro(request, pk):
    miembro = Miembro.objects.get(id=pk)
    if miembro.estado_membresia == 1:
        messages.warning(request, f'{miembro.user.first_name} tiene una membresía activa, no se puede eliminar.')
        return redirect(to='lista_miembros')
    else:
        miembro.estado = 1
        miembro.save()
        messages.success(request,f'{miembro.user.first_name} fue eliminado correctamente.')
        return redirect(to='lista_miembros')

def alta_miembro(request, pk):
    miembro = Miembro.objects.get(id=pk)
    miembro.estado = 0
    miembro.save()
    messages.success(request,f'{miembro.user.first_name} fue restaurado correctamente.')
    return redirect(to='bajas_miembros')
def alta_todos_miembros(request):
    miembros = Miembro.objects.filter(estado=1)
    for m in miembros:
        m.estado = 0
        m.save()
    messages.success(request,f'Todos los miembros fueron restaurados correctamente.')
    return redirect(to='lista_miembros')
#*************************Miembro****************************************



#*************************VENTA DE MEMBRESIA****************************************
def create_venta_membresia(request, username,idmember):
    try:
        user = User.objects.get(username=username)
        miembro = Miembro.objects.get(user=user.id)
        empleado = request.user
        membresia = Membresia.objects.get(id=idmember)
        monto_pagado = membresia.precio
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_inicio = timezone.localtime(timezone.now()).date()
        venta_membresia = VentaMembresia(empleado=empleado,miembro=miembro,monto_pagado=monto_pagado,membresia=membresia)
        miembro.estado_membresia = 1
        miembro.fecha_inicio = venta_membresia.fecha
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        fecha_fin = calcular_fecha_final(fecha_inicio, membresia.duracion)
        miembro.fecha_fin = fecha_fin
        fecha_fin_formateada = fecha_fin.strftime('%d de %B de %Y')

        # Restaura el idioma local a su valor original
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') 
        miembro.save()
        venta_membresia.save()
        miembro.venta_activa = venta_membresia.id
        miembro.save()
        print(venta_membresia.id)
        print(fecha_fin)
        messages.success(request, f"Venta realizada con éxito, el plan vence {fecha_fin_formateada}")
        subject = 'Compra realizada con éxito'
        message = f'\nEl plan comprado fue el {membresia.nombre}, con un costo de ${membresia.precio} y una duración de {membresia.duracion} meses. Finaliza el {fecha_fin_formateada}.\n\n¡GRACIAS POR FORMAR PARTE DE LA FAMILIA PERFECT BODY!\n\nCualquier consulta puedes acercate con nuestros encargados de turno, estamos para servirte.'
        from_email = EMAIL_HOST_USER
        recipient_list = [user.username]
        send_mail(subject, message, from_email, recipient_list)
        return redirect(to='lista_miembros')

    except Exception as e:
        print(e)
        return redirect(to='lista_miembros')
    


class ListVentaMembresia(ListView):
    model = VentaMembresia
    template_name = 'AppControlDeClientes/VentaMembresia/listVentaMembresia.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        vencimientoMembresias()
        data['titulo'] = 'Ventas realizadas'
        data['modulo'] = 'Venta de membresías'
        data['icono']  = '<i class="bi bi-plus-lg"></i>'
        data['ventas_membresia'] = VentaMembresia.objects.select_related('miembro').order_by('-id')
        
        # GANANCIAS DIARIAS
        fecha_actual = timezone.localtime(timezone.now()).date()
        ventas_hoy = VentaMembresia.objects.filter(fecha=fecha_actual)
        ventas_hoy_dinero = ventas_hoy.aggregate(total_ventas=Sum('monto_pagado'))['total_ventas']
        if ventas_hoy_dinero:

            data['ganancia_hoy'] = ventas_hoy_dinero
        else:
             data['ganancia_hoy'] = "0.00"
                # Realiza un recuento de todas las ventas por nombre

        # MEMBRESIA MAS VENDIDA
        try:
            ventas_contadas = VentaMembresia.objects.values('membresia').annotate(total_ventas=Count('membresia'))

            # Ordena las ventas contadas de mayor a menor
            ventas_ordenadas = ventas_contadas.order_by('-total_ventas')

            # La venta más común será la primera en la lista ordenada
            data['mas_vendida'] = Membresia.objects.get(id=ventas_ordenadas[0]['membresia'])
        except Exception as e:
            data['mas_vendida'] = "Ninguna"

        # Calcula la fecha de inicio de la semana actual (lunes)
        dias_para_lunes = fecha_actual.weekday()
        fecha_inicio_semana = fecha_actual - timedelta(days=dias_para_lunes)

        # Calcula la fecha de finalización de la semana actual (domingo)
        fecha_fin_semana = fecha_inicio_semana + timedelta(days=6)

        # Filtra las ventas dentro del rango de fechas de la semana actual
        ventas_semana = VentaMembresia.objects.filter(fecha__range=[fecha_inicio_semana, fecha_fin_semana])

        # Suma el monto pagado de las ventas de la semana actual
        ganancia_semana = ventas_semana.aggregate(total_ventas=Sum('monto_pagado'))['total_ventas']

        # Si hay ganancias para la semana, guárdalas en 'data', de lo contrario, establece el valor en "0.00"
        if ganancia_semana:
            data['ganancia_semana'] = ganancia_semana
        else:
            data['ganancia_semana'] = "0.00"
        # Filtra las ventas del mes actual
        ventas_mes_actual = VentaMembresia.objects.filter(fecha__year=fecha_actual.year, fecha__month=fecha_actual.month)

        # Calcula la suma de las ventas del mes
        ventas_mes_actual_dinero = ventas_mes_actual.aggregate(total_ventas=Sum('monto_pagado'))['total_ventas']

        if ventas_mes_actual_dinero:
            data['ganancia_mes_actual'] = ventas_mes_actual_dinero
        else:
            data['ganancia_mes_actual'] = "0.00"
        return data
class EstadisticasVentaMembresia(ListView):
    model = VentaMembresia
    template_name = 'AppControlDeClientes/VentaMembresia/estadisticas.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data = super().get_context_data(**kwargs)
        try:
             data['empresa'] = Empresa.objects.first()
        except:
             data['empresa'] = 'Error'
        vencimientoMembresias()
        data['titulo'] = 'Estadísticas'
        data['modulo'] = 'Venta de membresías'
         # GANANCIAS DIARIAS
        fecha_actual = timezone.localtime(timezone.now()).date()
        ventas_hoy = VentaMembresia.objects.filter(fecha=fecha_actual)
        ventas_hoy_dinero = ventas_hoy.aggregate(total_ventas=Sum('monto_pagado'))['total_ventas']
        if ventas_hoy_dinero:

            data['ganancia_hoy'] = ventas_hoy_dinero
        else:
             data['ganancia_hoy'] = "0.00"
                # Realiza un recuento de todas las ventas por nombre

        # MEMBRESIA MAS VENDIDA
        try:
            ventas_contadas = VentaMembresia.objects.values('membresia').annotate(total_ventas=Count('membresia'))

            # Ordena las ventas contadas de mayor a menor
            ventas_ordenadas = ventas_contadas.order_by('-total_ventas')

            # La venta más común será la primera en la lista ordenada
            data['mas_vendida'] = Membresia.objects.get(id=ventas_ordenadas[0]['membresia'])
        except Exception as e:
            data['mas_vendida'] = "Ninguna"

        # Calcula la fecha de inicio de la semana actual (lunes)
        dias_para_lunes = fecha_actual.weekday()
        fecha_inicio_semana = fecha_actual - timedelta(days=dias_para_lunes)

        # Calcula la fecha de finalización de la semana actual (domingo)
        fecha_fin_semana = fecha_inicio_semana + timedelta(days=6)

        # Filtra las ventas dentro del rango de fechas de la semana actual
        ventas_semana = VentaMembresia.objects.filter(fecha__range=[fecha_inicio_semana, fecha_fin_semana])

        # Suma el monto pagado de las ventas de la semana actual
        ganancia_semana = ventas_semana.aggregate(total_ventas=Sum('monto_pagado'))['total_ventas']

        # Si hay ganancias para la semana, guárdalas en 'data', de lo contrario, establece el valor en "0.00"
        if ganancia_semana:
            data['ganancia_semana'] = ganancia_semana
        else:
            data['ganancia_semana'] = "0.00"
        # Filtra las ventas del mes actual
        ventas_mes_actual = VentaMembresia.objects.filter(fecha__year=fecha_actual.year, fecha__month=fecha_actual.month)

        # Calcula la suma de las ventas del mes
        ventas_mes_actual_dinero = ventas_mes_actual.aggregate(total_ventas=Sum('monto_pagado'))['total_ventas']

        if ventas_mes_actual_dinero:
            data['ganancia_mes_actual'] = ventas_mes_actual_dinero
        else:
            data['ganancia_mes_actual'] = "0.00"
        from decimal import Decimal

        # Supongamos que tienes una lista llamada `ventas_cada_mes` con la estructura actual

        # Convierte los valores Decimal a float
        ventas_cada_mes = getVentasMensuales()
        for data_dict in ventas_cada_mes:
            data_dict['data'] = [float(val) for val in data_dict['data']]
        print(ventas_cada_mes)
        data['ventas_cada_mes'] = ventas_cada_mes
        data['cantidad_de_ventas'] =getCantidadVentas()
        return data
def DeleteVentaMembresia(request, pk):
    venta_membresia = VentaMembresia.objects.get(id=pk)
    try:
        miembro = Miembro.objects.get(venta_activa=venta_membresia.id)
        miembro.estado_membresia = 0
        miembro.fecha_inicio = None
        miembro.fecha_fin = None
        miembro.venta_activa = None
        miembro.save()
        venta_membresia.delete()
        messages.success(request, 'Venta eliminada correctamente')
    except Miembro.DoesNotExist:
        venta_membresia.delete()
        messages.success(request, 'Venta eliminada correctamente')
    return redirect(to='list_venta_membresia')
#*************************VENTA DE MEMBRESIA****************************************



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

##---------------------------------------------INICIO DE HISTORIAL DE MIEMBRO---------------------------------
class CreateHistorialMiembro(CreateView):
    model = HistorialMiembro
    form_class = FormHistorialMiembro
    success_url = reverse_lazy('crear_historialmiembro')
    template_name = 'AppControlDeClientes/HistorialMiembro/createHistorialMiembro.html'
    success_message = "¡Registro realizado con éxito!"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Crear Bitacora'
        data['modulo'] = 'Bitacora'
      
        return data

    def form_valid(self, form):
        # Calcula el IMC antes de guardar el registro
        altura = form.cleaned_data['altura']
        peso = form.cleaned_data['peso']
        imc = peso / (altura * altura)  # Fórmula para calcular el IMC

        form.instance.imc = imc  # Asigna el valor calculado al campo IMC en el modelo
    

        form.instance.miembro = Miembro.objects.get(pk=1)  # Aquí debes reemplazar con el miembro actual

        # Guarda el registro en la base de datos
        messages.success(self.request, "Bitacora añadida correctamente!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)


 #--------------------------------obteniendo el get del historial ----------------------------
def get_historialmiembro(request, name):
    data={}
    try:
        historial = HistorialMiembro.objects.get(miembro=name)
        data = historial.toJSON()
        data['miembros'] = str(historial.miembro)
        data['img'] = str(historial.get_image())
        data['message']= 'success'
    except Exception as e :
        data = {'message': 'Not Found'}
        print(e)
    return JsonResponse(data)
#*********************************

class ListHistorialMiembro(ListView):
    model = HistorialMiembro
    template_name = 'AppControlDeClientes/HistorialMiembro/listHistorialMiembro.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Bitacora'
        data['modulo'] = 'Bitacora'
        data['icono'] = '<i class="bi bi-plus-lg"></i>'
        # Aquí obtén los historiales de miembros y agrégalos al contexto
        data['historialmiembros'] = HistorialMiembro.objects.all()  # O usa el filtro que necesites
        return data


    #********************************

class UpdateHistorialMiembro(UpdateView):
    model = HistorialMiembro
    form_class = FormHistorialMiembro
    success_url = reverse_lazy('lista_historialmiembros')
    template_name = 'AppControlDeClientes/HistorialMiembro/updateHistorialMiembro.html'
    success_message = "¡Historial Miembro actualizado con éxito!"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)  

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Bitacora Miembro'
        data['modulo'] = 'Bitacora'
        return data

    def form_valid(self, form):
        altura = form.cleaned_data['altura']
        peso = form.cleaned_data['peso']
        imc = peso / (altura * altura)  # Fórmula para calcular el IMC
        form.instance.imc = imc  # Asigna el valor calculado al campo IMC en el modelo
    
        messages.success(self.request, "Historial Miembro actualizado con éxito!")
        return super().form_valid(form)

    
#***********************************
def DeleteHistorialMiembro(request, pk):
    try:
        historial = HistorialMiembro.objects.get(id=pk)
        historial.delete()  # Elimina el registro del historial
        messages.success(request, "¡Historial eliminado correctamente!")
    except HistorialMiembro.DoesNotExist:
        messages.error(request, "¡Error, el historial no se pudo encontrar!")
    except Exception as e:
        messages.error(request, "¡Error, la acción no se pudo realizar!")

    return redirect(to='lista_historialmiembros')


#***********************************ASISTENCIA**************************************************************
class CreateAsistenciaMiembro(TemplateView):
    template_name = 'AppControlDeClientes/Asistencia/registroAsistencia.html'
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)  
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Asistencia'
        data['titulo2'] = 'Miembro'
        data['modulo'] = 'Asistencia'
        return data
    
def lista_miembros(request):
    q = request.GET.get('q') # obtener término de búsqueda
    try:
        if q is not None:
            # Filtrar por nombre o apellido que contenga q
            miembros = Miembro.objects.filter(
                Q(user__first_name__icontains=q) | 
                Q(user__last_name__icontains=q),
                estado=False
            )
            if not miembros:
                miembros = Miembro.objects.filter(estado=False)
                nombres = [m.user.first_name for m in miembros]
                apellidos = [m.user.last_name for m in miembros]

                # Buscar coincidencias aproximadas
                nombre_match = process.extractOne(q, nombres)
                apellido_match = process.extractOne(q, apellidos)

                query = Q()

                if nombre_match[1] > 40:
                    query |= Q(user__first_name=nombre_match[0])

                if apellido_match[1] > 40:
                    query |= Q(user__last_name=apellido_match[0])

                miembros = miembros.filter(query)
        else:
            miembros = Miembro.objects.filter(estado=False)
            # Serializa los objetos Miembro a una lista de diccionarios
        miembros_list = [
            {
                'id': miembro.id,
                'nombre': miembro.user.first_name,
                'apellido': miembro.user.last_name,
                'fotoURL': miembro.foto.url,
                'edad' : calcular_edad(miembro.fecha_nac),
            }
            for miembro in miembros
        ]
        # Devuelve la lista de miembros como JSON
        return JsonResponse(miembros_list, safe=False)
    except Miembro.DoesNotExist:
        return JsonResponse({'error': 'No hay miembros'}, status=400)
    
def calcular_edad(fecha_nac):
    fecha_actual = timezone.now().date()
    edad = fecha_actual.year - fecha_nac.year
    if fecha_actual.month < fecha_nac.month:
        edad -= 1
    elif fecha_actual.month == fecha_nac.month and fecha_actual.day < fecha_nac.day:
        edad -= 1
    return edad

@csrf_exempt
def registrar_asistencia(request):
    if request.method == 'POST':
        # Obtener el ID del miembro seleccionado del cuerpo de la solicitud POST
        member_id = request.POST.get('member_id')
        if member_id:
            print("SE RECIBE EL ID: " +member_id)
            # Obtener el miembro de la base de datos
            try:
                miembro = Miembro.objects.get(id=member_id)
            except Miembro.DoesNotExist:
                return JsonResponse({'error': 'Miembro no encontrado'}, status=400)

            if miembro.estado_membresia == 1:
                # Crear un nuevo registro de asistencia
                asistencia = Asistencia(miembro=miembro, empleado=request.user)
                asistencia.save()
                messages.success(request, 'Asistencia Registrada')
            else:
                print("MEMBRESIA VENCIDA")
                messages.error(request, 'La membresía de este miembro está vencida')
        else:
            nombre = request.POST.get('nombre').upper()
            monto = Empresa.objects.first().tarifa
            if nombre:
                asistencia = Asistencia(nombre=nombre, empleado=request.user, monto_pagado=monto)
                asistencia.save()
                messages.success(request, 'Asistencia Registrada')
        return redirect(to='registro_asistencia')
    
class ListHistorialAsistencias(ListView):
    model = Asistencia
    template_name = 'AppControlDeClientes/Asistencia/listaHistorialAsistencia.html'
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except:
            data['empresa'] = 'Error'
        data['titulo'] = 'Historial de Asistencias'
        data['modulo'] = 'Asistencia'
        data['icono'] = '<i class="bi bi-plus-lg"></i>'
        data['asistencias'] = Asistencia.objects.all()
        return data
    
@csrf_exempt
def eliminarHistorial(request, pk):
    try:
        historial = get_object_or_404(Asistencia, id=pk)
        historial.delete()
        messages.success(request, "¡Historial Eliminado!")
    except Asistencia.DoesNotExist:
        messages.error(request, "¡La asistencia que intentas eliminar no existe!")
    except Exception as e:
        messages.error(request, f"¡Error: {str(e)}")
    return redirect(to='lista_asistencia')
    

    






















