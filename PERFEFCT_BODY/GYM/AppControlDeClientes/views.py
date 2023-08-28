from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from AppControlDeClientes.models import Miembro
from AppControlDeClientes.forms import FormMiembro
from django.contrib import messages
# Create your views here.
def prueba(request):
     return render(request, "layout/index.html")


    


class CreateMiembro(CreateView):
    model = Miembro
    form_class = FormMiembro
    template_name = 'layout/form.html'
    success_url= reverse_lazy('crear_miembro')
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['titulo'] = 'Crear Miembro'
        data['modulo'] = 'Miembro'
        return data