from django.shortcuts import redirect
from django.urls import reverse_lazy

#Mixin que valida si el usuario es administrador, sirve para dar permiso de acceder a la vista al Administrador 
class isAdministradorMixin(object):
    def dispatch(self, request, *args, **kwargs):
        #Si el usuario iniciado en sesion tiene el rol 1 (Administrador) que muestre la pagina 
        if request.user.rol == 1:
            return super().dispatch(request, *args, **kwargs)
        #Sino redirige a una pagina personalizada para indicar que no tiene permisos
        return redirect('sin_permiso')
    

#Mixin que valida si el usuario es empleado, sirve para dar permiso de acceder a la vista al empleado    
class isEmpleadoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        #Si el usuario iniciado en sesion tiene el rol 2 (Empleado) que muestre la pagina 
        if request.user.rol == 2:
            return super().dispatch(request, *args, **kwargs)
        #Sino redirige a una pagina personalizada para indicar que no tiene permisos
        return redirect('sin_permiso')


#Mixin que valida si el usuario es administrador o empleado, sirve para dar permiso de acceder a la vista a ambos
class isAdministradorOrEmpleadoMixin(object):
    def dispatch(self, request, *args, **kwargs):
        #Si el usuario iniciado en sesion tiene el rol 1 (Administrador) ó 2 (Empleado) que muestre la pagina 
        if request.user.rol == 1 or request.user.rol == 2:
            return super().dispatch(request, *args, **kwargs)
        #Sino redirige a una pagina personalizada para indicar que no tiene permisos
        return redirect('sin_permiso')

#Mixin que valida si el usuario es miembro, sirve para dar permiso de acceder a la vistas al miembro    
class isMiembroMixin(object):
    def dispatch(self, request, *args, **kwargs):
        #Si el usuario iniciado en sesion tiene el rol 3 (Miembro) que muestre la pagina 
        if request.user.rol == 3:
            return super().dispatch(request, *args, **kwargs)
        #Sino redirige a una pagina personalizada para indicar que no tiene permisos
        return redirect('sin_permiso')    