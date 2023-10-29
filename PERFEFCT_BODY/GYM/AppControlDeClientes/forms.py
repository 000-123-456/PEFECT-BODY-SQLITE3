from django.forms import  ModelForm, Select, TextInput,Textarea,DateInput,NumberInput,CharField
from AppControlDeClientes.models import Miembro,Membresia,HistorialMiembro
from .op import opGenero
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