from django.forms import  ChoiceField, ModelForm, Select, TextInput,Textarea,DateInput,NumberInput,CharField,ClearableFileInput
from AppControlDeClientes.models import Miembro,Membresia,HistorialMiembro,Asistencia,RutinaEjercicio,RutinaPersonalizada
from .op import opGenero
from AppControlDeClientes import op
class FormMiembro(ModelForm):
    
    class Meta:
        model=Miembro
        fields = {
            'telefono',
            'direcccion',
            'fecha_nac',
            'nombreContact',
            'telefonoContact',
            'genero',
            'foto'
        }
        labels={
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'fecha_nac': 'Fecha de nacimiento',
            'nombreContact':'Nombre de emergencia',
            'telefonoContact':'Teléfono de emergencia',
        }
        
        widgets={
                'telefono':  TextInput(
                    attrs={
                
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'pattern': '[0-9]{4}[-][0-9]{4}',
                        'id':'tel',
                        'autocomplete':'off',
                       
                    }
                ),
                'direcccion': Textarea(
                    attrs={
                        'style':'height: 100px',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                         'autocomplete':'off',
                    }
                ),
                'fecha_nac': DateInput(
                    attrs={
                        'type':'date',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':'off',
                    }
                ),
                'nombreContact': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                         'autocomplete':'off',
                       
                    }
                ),
                'telefonoContact':  TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'pattern': '[0-9]{4}[-][0-9]{4}',
                        'id':'telContact',
                        'autocomplete':'off',
                        
                    }
                ),
                'genero':  Select(
                    attrs={
                        'aria-label':"Seleccione genero",
                        'class': 'form-control',
                        'placeholder': 'Genero',
                        'autocomplete':'off',     
                    }
                )
        }
    def __init__(self, *args, **kargs):
            super().__init__(*args, **kargs)
            self.fields['genero'].queryset = opGenero
FormMiembro.field_order = [
            'genero',
            'fecha_nac',
            'telefono',
            'direcccion',
            'nombreContact',
            'telefonoContact'
            
        ]
      
#----------------------------------------------Membresia---------------------------------------------------
class FormMembresia(ModelForm):
    
    class Meta:
        model=Membresia
        fields = {
            'nombre',
            'precio',
            'duracion',
          
        }
        labels={
            'nombre': 'Nombre',
            'precio': 'Precio',
            'duracion': 'Duración',
            
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'precio': TextInput(
                    attrs={
                        'type':'text',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        

                        
                    }
                ),
                'duracion': TextInput(
                    attrs={
                        'type':'number',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        'value':"",
                    }
                )
         
         
        }

FormMembresia.field_order = [
            'nombre',
            'precio',
            'duracion'
        ]
        

#**************************************Historial -------------------------------------------------
class FormHistorialMiembro(ModelForm):   
    class Meta:
        model = HistorialMiembro
        fields = {
            'peso',
            'altura',
            'descripcion',
        }
        labels = {
            'peso': 'Peso (kg) ',
            'altura': 'Altura (M)',
            'descripcion': 'Descripción'       
        }

        widgets = {
            'peso': NumberInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': '0.00',
                }
            ),
            'altura': NumberInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'placeholder': '0.00',
                }
            ),
            'descripcion': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Descripción',
                }
            ),
        }
FormMembresia.field_order = [
            'peso',
            'altura',
            'descripcion',
        ]

from django.forms import ModelForm, Select
from .models import Asistencia, Comida, Dieta, Miembro

class FormAsistenciaMiembro(ModelForm):
    class Meta:
        model = Asistencia
        fields = ['miembro']
        labels = {
            'miembro': 'Miembro',
        }
        widgets = {
            'miembro': Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Miembro',
                    'id': 'SelectMiembro'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['miembro'].queryset = Miembro.objects.filter(estado=True).filter(estado_membresia=1)


class FormDieta(ModelForm):
    
    class Meta:
        model=Dieta
        fields = {
            'nombre',
            'rango',
        }
        labels={
            'nombre': 'Nombre',
            'rango': 'Rango',   
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'rango': Select(
                    attrs={
                        'type':'text',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        

                        
                    }
                ),

         
         
        }

FormDieta.field_order = [
            'nombre',
            'rango',

        ]

class FormComida(ModelForm):
    tiempo = ChoiceField(choices=op.opTiempo, widget=Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese tiempo de comida',
            'autocomplete': 'off',
        }
    ))
    class Meta:
        model=Comida
        fields = {
            'nombre',
            'tiempo',
            'detalle'
        }
        labels={
            'nombre': 'Nombre',
            'tiempo': 'Tiempo de comida',
            'detalle': 'Ingredientes',     
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
               
                'detalle': Textarea(
                    attrs={
                        'style':'height: 150px',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                         'autocomplete':'off',
                    }
                ),
         
         
        }

FormComida.field_order = [
            'nombre',
            'tiempo',
            'detalle',

        ]
        
##----------------------Rutinas de ejercicios------------------------------------------
class FormRutinaEjercicio(ModelForm):
    
    class Meta:
        model=RutinaEjercicio
        fields = {
          #  'dia',
            'imagen',
            'tipo_ejercicio',
            'detalle_ejercicio',
            'recomendacion',
            
        }
        labels={
           # 'dia': 'Dia',
            'imagen': 'Imagen ',
            'tipo_ejercicio': 'Tipo de ejercicio',
            'detalle_ejercicio': 'Series',
            'recomendacion':'Recomendacion',
          
        }
        
        widgets={
              #  'dia':  TextInput(
               #     attrs={
                
                #        'class': 'form-control',
                #        'placeholder': 'Ingrese nombre completo',
                #        'autocomplete':'off',
                       
                #    }
                #),
                'imagen': ClearableFileInput(  
                attrs={
                    'class': 'form-control',
                     }
                ),
                'tipo_ejercicio':  TextInput(
                        attrs={
                    
                            'class': 'form-control',
                            'placeholder': 'Ingrese nombre completo',
                            'autocomplete':'off',
                        
                        }
                    ),
               
                'detalle_ejercicio': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                         'autocomplete':'off',
                       
                    }
                ),
                'recomendacion': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                         'autocomplete':'off',
                       
                    }
                )
               
        }

FormRutinaEjercicio.field_order = [
            'dia',
            'tipo_ejercicio',
            'imagen',
            'detalle_ejercicio',
            'recomendacion',                     
        ]
##----------------------Rutinas de ejercicios Personalizadas------------------------------------------
'''class FormRutinaPersonalizada(ModelForm):
    intensidad = ChoiceField(choices=op.opIntensidad, widget=Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese  Intensidad de la Rutina',
            'autocomplete': 'off',
        }
    ))
    
    class Meta:
        model=RutinaPersonalizada
        fields = {
            'ejercicio',
            'intensidad',
            'duracionejer',
            'descanso',
            
        }
        labels={
            'ejercicio': 'ejercicio',
            'intensidad': '',
            'duracionejer': 'Series',
            'descanso':'Descanso entre series',
          
        }
        
        widgets={                      
                'ejercicio':  TextInput(
                        attrs={
                    
                            'class': 'form-control',
                            'placeholder': 'Ingrese nombre completo',
                            'autocomplete':'off',
                        
                        }
                    ),
               
                'duracionejer': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                         'autocomplete':'off',
                       
                    }
                ),
                'descanso': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                         'autocomplete':'off',
                       
                    }
                )
               
        }

FormRutinaPersonalizada.field_order = [
            'ejercicio',
            'intensidad',
            'duracionejer',
            'descanso',                     
        ]'''

from django import forms
from django.forms import ModelForm, TextInput, ChoiceField, Select
from .models import RutinaPersonalizada

class FormRutinaPersonalizada(ModelForm):
    intensidad = ChoiceField(
        choices=op.opIntensidad,
        widget=Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione Intensidad de la Rutina',
                'autocomplete': 'off',
                'required': 'required',  # Agregamos este atributo
            }
        )
    )
    
    class Meta:
        model = RutinaPersonalizada
        fields = ['ejercicio', 'intensidad', 'duracionejer', 'descanso']
        labels = {
            'ejercicio': 'Ejercicio',
            'intensidad': 'Intensidad',
            'duracionejer': 'Series',
            'descanso': 'Minutos entre series',
        }
        
        widgets = {
            'ejercicio': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre completo', 'autocomplete': 'off'}),
            'duracionejer': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre completo', 'autocomplete': 'off'}),
            'descanso': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre completo', 'autocomplete': 'off'}),
        }
