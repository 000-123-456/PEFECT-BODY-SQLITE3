from django.forms import  ChoiceField, ModelForm, Select, TextInput,Textarea,DateInput,NumberInput,CharField,ClearableFileInput
from AppControlDeClientes.models import Miembro,Membresia,HistorialMiembro,Asistencia,Rutina,Ejercicio
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
        
#*********************************************************RUTINA***************************************************************
class FormRutina(ModelForm):
    experiencia = ChoiceField(choices=op.opExperiencia, widget=Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la experiencia que usted tiene ',
            'autocomplete': 'off',
        }
    ))
    tipo_ejercicio = ChoiceField(choices=op.opTipoEjercicio, widget=Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese tipo ejercicio ',
            'autocomplete': 'off',
        }
    ))


    class Meta:
        model=Rutina
        fields = {
            'experiencia',
            'tipo_ejercicio',
            'nombre'
        }
        labels={
            'experiencia': 'Experiencia',
            'tipo_ejercicio': 'Tipo de Ejercicio',
            'nombre': 'Nombre Rutina',     
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),                       
         
        }

FormRutina.field_order = [
            'experiencia',
            'tipo_ejercicio',
            'nombre',

        ]

#////////////////////////////////////Ejercicio
class FormEjercicio(ModelForm):
    musculo = ChoiceField(choices=op.opMusculo, widget=Select(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el musculo que desea hacer ejercicio en especifico ',
            'autocomplete': 'off',
        }
    ))  
    class Meta:
        model=Ejercicio
        fields = {
            'nombre',
            'imagen',
            'musculo',
            'detalle_ejercicio',
            'recomendacion',
            
        }
        labels={
            'nombre': 'nombre',
            'imagen': 'Imagen ',
            'musculo': 'Musculo en especifico que desea trabajar',
            'detalle_ejercicio': 'Series',
            'recomendacion':'Recomendacion',
          
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                         'autocomplete':'off',
                       
                    }
                ),
    
                'imagen': ClearableFileInput(  
                attrs={
                    'class': 'form-control',
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

FormEjercicio.field_order = [
            'nombre',
            'imagen',
            'musculo',
            'detalle_ejercicio',
            'recomendacion',                  
        ]