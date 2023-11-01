from AppInventarioMaquinaria.models import *
from django.forms import DateInput, ModelForm, TextInput, Select, FileInput
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

class FormHistorialMaquinaria(ModelForm):
    class Meta:
        model= HistorialMaquinaria
        fields = {
            'tipo',
            'detalle',
            'fecha_fin',
            'fecha_ini',
            'maquinaria'
        }
        labels={
            'tipo': 'Tipo',
            'detalle': 'Detalle',
            'fecha_fin': 'Fecha final',
            'fecha_ini':'Fecha de inicio',
            'maquinaria':'Maquinaria'
        }
        widgets={
            'tipo': Select(choices=opTipoM,
                attrs={
                    'class': 'form-control',

                    
                }
            ),
            'detalle': TextInput(
                attrs={
                    'class': 'form-control',

                }
            ),
            'fecha_fin': DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
            'fecha_ini': DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
            'maquinaria': Select(
                attrs={
                    'class': 'form-control', 
                    'id': 'SelectMaquinaria'
                }
            ),
        }


class FormInicioHistorialMaquinaria(ModelForm):
    class Meta:
        model= HistorialMaquinaria
        fields = {
            'detalle',
            'fecha_ini',
            'tipo',
            'maquinaria'
        }
        labels={
            'detalle': 'Detalle',
            'fecha_ini':'Fecha de inicio',
            'tipo':'Tipo',
            'maquinaria':'Maquinaria'
        }
        widgets={
            'detalle': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese los detalles',
                    'autocomplete':"off", 
                }
            ),
            'fecha_ini': DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
            ),
            'tipo': Select(choices=opTipoM,
                attrs={
                    'class': 'form-control',
                }
            ),
            'maquinaria': Select(
                attrs={
                    'class': 'form-control', 
                    'id': 'SelectMaquinaria'
                }
            ),
        }
    
