#----------------------AQUI SE METE A DIETAS********************

from typing import Any
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from AppControlDeClientes.mixins import isAdministradorMixin, isMiembroMixin
from AppControlDeClientes.models import Comida, Dieta, ListaDietas, Miembro
from AppControlDeClientes import op
from AppControlDeClientes.funciones import encontrar_posicion_mas_cercana, mis_dietas, obtener_comidas_por_dieta
from AppControlDeClientes.op import rango
from AppControlDeClientes.forms import FormComida, FormDieta
from django.contrib import messages

class ListDietas(isMiembroMixin,ListView):
    model = Dieta
    template_name = 'AppControlDeClientes/Dietas/listaDietas.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Menú de dietas'
        data['modulo'] = 'Dietas'
        # Agregar las dietas y comidas al contexto
        data['dietas_y_comidas_del_miembro'] = mis_dietas(Miembro.objects.get(user = self.request.user))
        return data
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        data = {}
        try:
            #Si el parametro action es recomendaciones quiere decir se esta pidiendo recomendaciones de dietas
            action= request.POST['action']
            if action == 'recomendaciones':
                #obtenemos el miembro que ha iniciado sesion
                miembro = Miembro.objects.get(user = request.user.pk)
                #Verificamos si es hombre o mujer para definir el peso ideal y factor de actividad
                if miembro.genero == 1:
                    peso_ideal = int(request.POST['altura'])-100+3
                    factor_actividad = op.factor_hombres[int(request.POST['actividad_fisica'])-1][0]
                else:
                    peso_ideal = int(request.POST['altura'])-100-3
                    factor_actividad = op.factor_mujeres[int(request.POST['actividad_fisica'])-1][0]
                peso_ideal*=2.2
                calorias = peso_ideal*factor_actividad
                print(f'Peso ideal: {peso_ideal}')
                print(f'Factor de actividad: {factor_actividad}')
                print(f'Calorias necesarias: {calorias}')
                if int(request.POST['objetivo']) == 1:
                    calorias -=500
                else:
                    calorias +=500
                print(f'Calorias necesarias para el objetivo: {calorias}')
                rango_dietas = encontrar_posicion_mas_cercana(rango, int(request.POST['objetivo']),calorias)
                print(rango_dietas)
                data = obtener_comidas_por_dieta(rango_dietas)
                return JsonResponse(data, safe=False)
            elif action == 'guardar':
                print(request.POST)
                print(request.POST.get('dia'))
                print(request.POST.get('idDieta'))
                print(self.request.user)
                # Obtén la instancia de Miembro actual
                # Obtén el usuario actual
                user = self.request.user

                # Obtén la instancia de Miembro relacionada con el usuario
                miembro = get_object_or_404(Miembro, user=user)
                
                # Obtén el ID de la dieta desde el formulario
                id_dieta = request.POST.get('idDieta')
                print(id_dieta)
                # Obtén el día desde el formulario
                dia = request.POST.get('dia')
                print(f"ID Dieta: {id_dieta}")
                print(f"Día: {dia}")
            # Crea y guarda la instancia de ListaDietas
                if not ListaDietas.objects.filter(miembro=miembro, dia=dia).exists():
                    nueva_dieta = ListaDietas(miembro=miembro, dieta_id=id_dieta, dia=dia)
                    nueva_dieta.save()
                    messages.success(request, 'Dieta guardada')
                else:
                   mi_dieta = ListaDietas.objects.get(miembro=miembro, dia=dia)
                   mi_dieta.dieta_id = id_dieta
                   mi_dieta.save()
                   messages.success(request, 'Dieta guardada')


        except Exception as e:
            data['error']= str(e)
        return redirect('dietas')
    
#-----------RECOMENDACIONES DE DIETAS --------------------------------------------
class CreateRecomendacionDieta(isAdministradorMixin,CreateView):
    template_name = 'AppControlDeClientes/RecomendacionesDietas/createRecomendacion.html'
    form_class = FormDieta
    success_url = reverse_lazy('lista_recomendaciones_dieta')
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Registro de dieta'
        data['modulo'] = 'Dietas'
        return data
    def form_valid(self, form):
        messages.success(self.request, "Dieta registrada correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)

class ListRecomendacionDieta(isAdministradorMixin,ListView):
    model = Dieta
    template_name = 'AppControlDeClientes/RecomendacionesDietas/listRecomendacion.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Listado de dietas'
        data['modulo'] = 'Dietas'
        data['dietas'] = Dieta.objects.all().reverse()
        return data
    




#AQUI YA DE COMIDA



class ListRecomendacionComida(isAdministradorMixin,ListView):
    model = Comida
    template_name = 'AppControlDeClientes/RecomendacionesDietas/RecomendacionesComida/listComida.html'
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        # Obtengo el id de la dieta que paso por la URL
        id_dieta = self.kwargs.get('pk', None)
        data['titulo'] = 'Listado de comidas'
        data['modulo'] = 'Dietas'
        data['comidas'] = Comida.objects.filter(dieta=id_dieta).reverse()
        return data

class CreateRecomendacionComida(isAdministradorMixin,CreateView):
    template_name = 'AppControlDeClientes/RecomendacionesDietas/RecomendacionesComida/createComida.html'
    form_class = FormComida
    success_url = reverse_lazy('registro_recomendaciones_dieta')
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Agrega una opción adicional al campo 'tiempo'
        form.fields['tiempo'].choices += [('', 'Seleccione una opción')]

        return form
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Registro de comida'
        data['modulo'] = 'Dietas'
        return data
    def form_valid(self, form):
        #Obtengo el id de la dieta que paso por url
        id_dieta = self.kwargs.get('pk', None)

        # Se lo asigno al campo del modelo antes de guardarlo para crear la relacion
        # Obtengo el objeto Dieta correspondiente al ID
        dieta = Dieta.objects.get(id=id_dieta)
        form.instance.dieta = dieta
        messages.success(self.request, "Dieta registrada correctamente")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, format(form.errors.as_text()))
        return super().form_invalid(form)    
    
def eliminar_mi_dieta(request, pk):
    mi_dieta = ListaDietas.objects.get(id=pk)
    mi_dieta.delete()
    messages.success(request,f'La dieta fue eliminada de su lista.')
    return redirect(to='dietas')

