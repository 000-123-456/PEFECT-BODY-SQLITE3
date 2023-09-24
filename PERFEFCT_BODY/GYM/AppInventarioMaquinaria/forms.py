from AppInventarioMaquinaria.models import *
from django.forms import ModelForm, TextInput, Select, FileInput
from AppInventarioMaquinaria.opciones import *

class FormMaquinaria(ModelForm):   
    class Meta:
        model= Maquinaria
        fields = {
            'nombre',
            'descripcion',
            'foto',
            'categoriaM',
        }
        labels={
            'nombre': 'Modelo',
            'descripcion': 'Descripción',
            'foto': 'Foto',
            'categoriaM':'Categoría',
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'descripcion': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'categoriaM': Select(choices=opCategoriaM,
                    attrs={
                        'class': 'form-control',
                        'autocomplete':"off",
                        
                    }
                ),
        }
        
class FormMaquinariaEdit(ModelForm):
    class Meta:
        model= Maquinaria
        fields = {
            'nombre',
            'descripcion',
            'foto',
            'categoriaM',
            'estado_maquina'
        }
        labels={
            'nombre': 'Modelo',
            'descripcion': 'Descripción',
            'foto': 'Foto',
            'categoriaM':'Categoría',
            'estado_maquina':'Estado de máquina'
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'descripcion': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'categoriaM': Select(choices=opCategoriaM,
                    attrs={
                        'class': 'form-control',
                        'autocomplete':"off",
                        
                    }
                ),
                'estado_maquina': Select(choices=opEstadoM,
                    attrs={
                        'class': 'form-control',
                        'autocomplete':"off",
                        
                    }
                ),
        }

FormMaquinaria.field_order = [
            'nombre',
            'descripcion',
            'categoriaM',
            'foto'
        ]