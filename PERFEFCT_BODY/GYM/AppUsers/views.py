from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from AppUsers.models import User
from django.contrib.auth.forms import UserCreationForm
from AppUsers.forms import RegistroUsuarioForm,FormEmpresa
from django.contrib.auth.views import LoginView
from django.views.generic import  UpdateView,ListView,TemplateView
from typing import Any
from AppUsers.models import Empresa
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from AppControlDeClientes.models import Asistencia, Miembro, VentaMembresia
from AppInventario.funciones import listar_productos_con_cantidad_baja, obtener_compras_proximas_a_vencer
from AppControlDeClientes.op import generar_clave_temporal_segura
from AppControlDeClientes.mixins import isAdministradorMixin, isMiembroMixin
from GYM.settings import STATIC_URL
from django.core.mail import send_mail
from GYM.settings import EMAIL_HOST_USER
from django.urls import reverse
from django.contrib.auth import logout
# Create your views here.
class inicioMiembro(isMiembroMixin,TemplateView):
    template_name = 'layout/userUI/index.html'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Inicio'
        context["modulo"] = 'Home'
        miembro = Miembro.objects.get(user = self.request.user)
        context["miembro"] = miembro
        context["venta_membresia"] = VentaMembresia.objects.get(id = miembro.venta_activa)
        return context


# Create your views here.
class RegistroUsuario(CreateView):
    model = User
    template_name = "AppUsers/User/signIn.html"
    form_class= RegistroUsuarioForm
    success_url = reverse_lazy('registrar_empresa')
    def form_valid(self, form):
        # Registra al usuario y luego inicia sesión
        response = super().form_valid(form)
        user = form.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        if user is not None:
            login(self.request, user)
        return response
    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)

class LoginFormView(LoginView):
    template_name='AppUsers/User/login.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.rol == 2:
                return redirect('registro_asistencia')
            elif request.user.rol == 3:
                return redirect('inicio_miembro')
            elif request.user.rol == 4:
                return redirect('lista_recomendaciones_dieta')
            elif request.user.rol == 5:
                return redirect('lista_Rutina_Ejercicio')
            else:
                return redirect('prueba')
        
        if User.objects.count()==0:
            return redirect('registrar')
        return super().dispatch(request, *args, **kwargs)
    def form_invalid(self, form):
        username = form.cleaned_data.get('username', '')
        print(f"Datos del formulario cuando es inválido para el usuario: {username}")

        # Imprimir otros datos del formulario si es necesario
        print(f"Contraseña proporcionada: {form.cleaned_data.get('password', '')}")

        try:
            user = User.objects.get(username=username)
                    # Verificar si el usuario está activo
            if not user.is_active:
                messages.error(self.request, "Su cuenta no está activa. Comuníquese con el administrador.")
            if user.rol == 3:
                if not Miembro.objects.get(user = user).venta_activa:
                    messages.error(self.request, "No puede acceder al sistema, su membresía se venció o no cuenta con una. Comuníquese con el administrador o recepcionista para renovarla.")
            else:
            # Usuario existe, pero la contraseña es incorrecta
                messages.error(self.request, "Contraseña incorrecta. Por favor, verifique sus credenciales e inténtelo de nuevo.")
                
        except User.DoesNotExist:
            # Usuario no existe
            messages.error(self.request, "Usuario no encontrado. Por favor, verifique sus credenciales e inténtelo de nuevo.")
        # Imprimir los errores del formulario
        print("Errores del formulario:")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"{field}: {error}")
        return super().form_invalid(form)
    def form_valid(self, form):
        # Realizar la autenticación del usuario
        self.user = form.get_user()
        print(f"Usuario después de form.get_user(): {self.user}")
        if self.user is not None:
        # Verificar si es el primer ingreso
            if self.user.primer_ingreso:
                login(self.request, self.user)
                return redirect('primera_clave')
        if not self.user.is_active:
            messages.error(self.request, "Su cuenta no está activa. Comuníquese con el administrador.")
            return self.form_invalid(form)
        user = User.objects.get(username = self.user.username)

        # Comprobar si el rol es igual a 3 (miembro) y comprobar si el miembro tiene membresia activa
        if user.rol == 3:
            if not Miembro.objects.get(user = user).venta_activa:
                return self.form_invalid(form)   

        login(self.request, self.user)

        # Verificar el rol del usuario y redirigir en consecuencia
  # Reemplaza 'vista_miembro' con el nombre de la vista a la que deseas redirigir a los miembros
        if self.user.rol == 2:
            return redirect('registro_asistencia')  # Reemplaza 'otra_vista' con el nombre de la vista a la que deseas redirigir a otros usuarios autenticados
        elif self.user.rol == 3:
                return redirect('inicio_miembro')
        elif self.user.rol == 4:
            return redirect('lista_recomendaciones_dieta')  # Reemplaza 'otra_vista' con el nombre de la vista a la que deseas redirigir a otros usuarios autenticados
        elif self.user.rol == 5:
            return redirect('lista_Rutina')  # Reemplaza 'otra_vista' con el nombre de la vista a la que deseas redirigir a otros usuarios autenticados
        else:
            return redirect('prueba') 
class CambioClave(UpdateView):
    model = User
    template_name = "AppUsers/User/primeraClave.html"
    form_class = RegistroUsuarioForm
    def dispatch(self, request, *args, **kwargs):
        if not request.user.primer_ingreso:
            if request.user.rol == 2:
                return redirect('registro_asistencia')
            elif request.user.rol == 3:
                return redirect('inicio_miembro')
            elif request.user.rol == 4:
                return redirect('lista_recomendaciones_dieta')
            elif request.user.rol == 5:
                return redirect('lista_Rutina')
            else:
                return redirect('prueba')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Hacer campos no relacionados con contraseñas opcionales
        form.fields['username'].required = False
        form.fields['email'].required = False
        form.fields['first_name'].required = False
        form.fields['last_name'].required = False
        return form

    def get_object(self, queryset=None):
        # Devuelve el objeto del usuario actual
        return self.request.user

    def form_valid(self, form):
        # Lógica para manejar el formulario válido
        user_current = User.objects.get(username=self.request.user.username)
        user_current.set_password(self.request.POST['password1'])
        user_current.primer_ingreso = False
        user_current.save()

        logout(self.request)
        login(self.request,user_current)
        messages.success(self.request, "Contraseña actualizada correctamente.")
        if user_current.rol == 2:
            return redirect('registro_asistencia')  # Reemplaza 'otra_vista' con el nombre de la vista a la que deseas redirigir a otros usuarios autenticados
        elif user_current.rol == 3:
                return redirect('inicio_miembro')
        elif user_current.rol == 4:
            return redirect('lista_recomendaciones_dieta')  # Reemplaza 'otra_vista' con el nombre de la vista a la que deseas redirigir a otros usuarios autenticados
        elif user_current.rol == 5:
            return redirect('lista_Rutina')  # Reemplaza 'otra_vista' con el nombre de la vista a la que deseas redirigir a otros usuarios autenticados
        else:
             return redirect('prueba')


    def form_invalid(self, form):
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return super().form_invalid(form) 
class OlvidoClave(TemplateView):
    template_name = "AppUsers/User/olvido-clave.html"
    def post(self, request, *args, **kwargs):
        form = request.POST
        #Se comprueba si el usuario ingresado existe y mandar el correo de recuperacion 
        if User.objects.filter(username=form['username']).exists():
            user = User.objects.get(username=form['username'])
            clave = str(generar_clave_temporal_segura())
            user.set_password(clave)
            ## Se activa primer ingreso para que pueda cambiar la clave temporal
            user.primer_ingreso = True
            user.save()
            subject = 'Olvido de contraseña'
            message = f'Hola {user.first_name}, con los siguientes datos podras ingresar al sistema y cambiar tu contraseña.\nUsuario: {user.username}\nContraseña temporal: {clave}\nIngrese al siguiente link: {self.request.build_absolute_uri(reverse("login"))}\n\n¡LA FAMILIA PERFECT BODY, SIEMPRE PARA DARTE LOS MEJOR DE NOSOTROS! 💛🖤'
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message,from_email, recipient_list)
            messages.success(self.request, 'Revisa tu correo, se han enviado tus datos para que puedas acceder al sistema.')
            return redirect('login')
        else:
            messages.warning(self.request, "El usuario ingresado no existe, revise que sus datos sean correctos.")
        return redirect('olvido_clave')
    


class CrearUsuario(isAdministradorMixin,CreateView):
    model= User
    template_name = 'AppUsers/User/createUsuario.html'
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('crear_usuario')
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Registrar usuarios'
        context["modulo"] = 'Usuarios'
        context["url_modulo"] = reverse_lazy('lista_usuario')
        context["icono"] = 'bi bi-plus-lg'
        
        return context
    def form_valid(self, form):
        
        #obtengo la url absoluta
        user_form = RegistroUsuarioForm(self.request.POST)
        url = self.request.build_absolute_uri(reverse('login'))
        try:
            if form.cleaned_data['username'] == '':
            # Asignar el valor del campo 'email' al campo 'username' si viene vacio
                form.instance.username = form.cleaned_data['email']
            user = user_form.save(commit=False)
            clave = str(generar_clave_temporal_segura())
            user.rol = self.request.POST['rol']
            user.set_password(clave)
            user.empresa = Empresa.objects.first()
            user.save()
            subject = 'Bienvenido'
            message = f'Se ha registrado exitosamente, con los siguientes datos podrá hacer uso del sistema.\nUsuario: {user.username}\nContraseña: {clave}\nIngrese al siguiente link: {url}\n\n¡BIENVENIDO A LA FAMILIA PERFECT BODY!💛🖤\nSiempre dandole lo mejor a nuestros clientes.'
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            send_mail(subject, message,from_email, recipient_list)
            print('correcto')
            messages.success(self.request, "Usuario registrado correctamente")
            
        # 3. Validación de usuario guardado correctamente
        except IntegrityError:
            print('Fallo')
            messages.error(self.request, "El nombre o correo ya existe de usuario ya existe. Por favor, elija otro nombre de usuario.")
            return render(self.request, self.template_name, {'form': form, 'titulo':'Registrar usuarios','modulo':'Usuarios'})

        return redirect('crear_usuario')

class UpdateUsuario(isAdministradorMixin,UpdateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'AppUsers/User/updateUsuario.html'
    success_url = reverse_lazy('lista_usuario')
    def form_valid(self, form):
        user_form = RegistroUsuarioForm(self.request.POST)
        try:
            current_user = User.objects.get(pk=self.object.pk)

            # Verificar si el username ha cambiado
            if form.cleaned_data['username'] != current_user.username:
                form.instance.username = form.cleaned_data['username']
                
                # Generar una nueva clave temporal segura
                user = user_form.save(commit=False)
                clave = str(generar_clave_temporal_segura())
                user.rol = self.request.POST['rol']
                user.set_password(clave)
                user.empresa = Empresa.objects.first()
                user.primer_ingreso = True
                user.save()
                # Guardar el usuario con los cambios

                # Enviar correo con la nueva contraseña
                subject = 'Actualizacion de datos'
                message = f'Se ha actualizado exitosamente, con los siguientes datos podrá acceder al sistema.\nUsuario: {form.instance.username}\nContraseña: {clave}\nIngrese al siguiente link: {self.request.build_absolute_uri(reverse("login"))}\n\n¡BIENVENIDO A LA FAMILIA PERFECT BODY!💛🖤\nSiempre dándole lo mejor a nuestros clientes.'
                from_email = EMAIL_HOST_USER
                recipient_list = [form.instance.email]
                send_mail(subject, message, from_email, recipient_list)

                messages.success(self.request, "Usuario actualizado correctamente")
                return redirect('lista_usuario')

            # Verificar si el email ha cambiado
            elif form.cleaned_data['email'] != current_user.email:
                form.save()

                # Enviar correo de confirmación del email
                subject = 'Confirmación de Email'
                message = f'{form.instance.first_name} {form.instance.last_name}, su dirección de correo electrónico ha sido actualizada correctamente a {form.instance.email}.'
                from_email = EMAIL_HOST_USER
                recipient_list = [form.instance.email]
                send_mail(subject, message, from_email, recipient_list)

                messages.success(self.request, "Usuario actualizado correctamente")
                return redirect('lista_usuario')

            # Si no hay cambios en el username ni en el email
            else:
                form.save()

                messages.success(self.request, "Usuario actualizado correctamente")
                return redirect('lista_usuario')

        except IntegrityError:
            messages.error(self.request, "El nombre de usuario ya existe. Por favor, elija otro nombre de usuario.")
            return render(self.request, self.template_name, {'form': form, 'titulo': 'Actualizar usuarios', 'modulo': 'Usuarios'})

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Actualizar usuarios'
        context["modulo"] = 'Usuarios'
        context["url_modulo"] = reverse_lazy('lista_usuario')
        context["icono"] = 'bi bi-pencil-square'
        
        return context
class ListUsuarios(isAdministradorMixin,ListView):
    model= User
    template_name = 'AppUsers/User/listUsuario.html'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Listado de usuarios'
        context["modulo"] = 'Usuarios'
        context["url_modulo"] = reverse_lazy('lista_usuario')
        context["url_papelera"] = reverse_lazy('papelera_usuario')
        context["url_nuevo"] = reverse_lazy('crear_usuario')
        #Obtiene todos los usuarios que no son miembros
        context["usuarios"] = User.objects.exclude(miembro__isnull=False).order_by('-id').filter(is_active=True)
        return context
class ListBajasUsuarios(isAdministradorMixin,ListView):
    model= User
    template_name = 'AppUsers/User/listBajasUsuario.html'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = 'Usuarios eliminados'
        context["modulo"] = 'Usuarios'
        context["url_modulo"] = reverse_lazy('lista_usuario')
        #Obtiene todos los usuarios que no son miembros que no estan activos
        context["usuarios"] = User.objects.exclude(miembro__isnull=False).order_by('-id').filter(is_active=False)
        return context



def BajaUsuario(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.is_active = False
        user.save()
        messages.success(request, "¡Usuario eliminado correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='lista_usuario')

def AltaUsuario(request, pk):
    try:
        user = User.objects.get(id=pk)
        user.is_active = True
        user.save()
        messages.success(request, "Usuario restaurado correctamente!")
    except:
        messages.error(request, "¡Error, la accion no se pudo realizar!")
    return redirect(to='papelera_usuario')

#-------------------------------------------------EMPRESA-----------------------------

class CrearEmpresa(isAdministradorMixin,CreateView):
    model = Empresa
    template_name = 'AppUsers/Empresa/createEmpresa.html'
    form_class= FormEmpresa
    success_url = reverse_lazy('prueba')





#class UpdateEmpresa(UpdateView):
 #   model = Empresa
  #  form_class = FormEmpresa
   # success_url= reverse_lazy('lista_empresas')
    #template_name = 'AppUsers/Empresa/updateEmpresa.html'
    #success_message = "¡Registro actualizado con éxito!"
    #def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
     #   return super().dispatch(request, *args, **kwargs)  
    #def get_context_data(self, **kwargs):
     #   data = super().get_context_data(**kwargs)
      #  data['empresa'] = Empresa.objects.first()
       # data['titulo'] = 'Actualizar empresa'
        #data['modulo'] = 'Empresa'
        #return data
    #def post(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        #messages.success(request,'Empresa actualizada correctamente!')
        #return super().post(request, *args, **kwargs)
    
@method_decorator(login_required, name='dispatch')
class UpdateEmpresa(UpdateView):
    model = Empresa
    form_class = FormEmpresa
    template_name = 'AppUsers/Empresa/updateEmpresa.html'
    success_message = "¡Registro actualizado con éxito!"

    def get_success_url(self):
        try:
            emp = Empresa.objects.first()
            url = '/Empresa/ActualizarEmpresas/' + str(emp.id) + '/'
            return url
        except Empresa.DoesNotExist:
            # En caso de que no se encuentre una empresa, redirigir a otra URL
            return '/'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        try:
            data['empresa'] = Empresa.objects.first()
        except Empresa.DoesNotExist:
            data['empresa'] = 'Error'
        data['titulo'] = 'Actualizar empresa'
        data['modulo'] = 'Empresa'
        return data
    

##----CLASES DE ERRORES PERSONALIZADAS ---------------
class Error404View(TemplateView):
    template_name = 'Errors/error_404.html'

class SinPermisoView(TemplateView):
    template_name = 'Errors/sin_permiso.html'    

class NotificacionesView(TemplateView):
    template_name = 'notificaciones/notificacion.html'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["modulo"] = "Notificaciones"
        context["titulo"] = "Todas las notificaciones"
        context["url_modulo"] = reverse_lazy('notificaciones')
        context["notificaciones_productos_bajos"] = listar_productos_con_cantidad_baja()
        context["notificaciones_productos_vencidos"] = obtener_compras_proximas_a_vencer()
        context["notificaciones_count"] = listar_productos_con_cantidad_baja()['count_productos_bajos_total']+obtener_compras_proximas_a_vencer()['cantidad_registros_total']
        return context
    
class BitacoraVentaMembresiaView(isAdministradorMixin,TemplateView):
    template_name = 'Bitacora/bitacoraVentaMembresia.html'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["modulo"] = "Historial"
        context["titulo"] = "Ventas de membresías"
        context["url_modulo"] = reverse_lazy('bitacora_venta_membresia')
        context["venta_membresia"] = VentaMembresia.objects.all().reverse()
        return context
class BitacoraAsistenciaView(isAdministradorMixin,TemplateView):
    template_name = 'Bitacora/bitacoraAsistencia.html'
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["modulo"] = "Historial"
        context["titulo"] = "Asistencias"
        context["url_modulo"] = reverse_lazy('bitacora_asistencias')
        context["asistencias"] = Asistencia.objects.all().reverse()
        return context
    

    