from django.forms import  ModelForm, Select, TextInput,Textarea,DateInput
from AppControlDeClientes.models import Miembro,Membresia
class FormMiembro(ModelForm):
    
    class Meta:
        model=Miembro
        fields = {
            'nombre',
            'telefono',
            'direcccion',
            'fecha_nac',
            'nombreContact',
            'telefonoContact',
        }
        labels={
            'nombre': 'Nombre',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'fecha_nac': 'Fecha de nacimiento',
            'nombreContact':'Nombre de emergencia',
            'telefonoContact':'Teléfono de emergencia',
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        
                    }
                ),
                'telefono':  TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'pattern': '[0-9]{4}[-][0-9]{4}',
                        'id':'tel'
                       
                    }
                ),
                'direcccion': Textarea(
                    attrs={
                        'style':'height: 100px',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        
                    }
                ),
                'fecha_nac': DateInput(
                    attrs={
                        'type':'date',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                    }
                ),
                'nombreContact': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                       
                    }
                ),
                'telefonoContact':  TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'pattern': '[0-9]{4}[-][0-9]{4}',
                        'id':'telContact'
                        
                    }
                )
        }

FormMiembro.field_order = [
            'nombre',
            'telefono',
            'fecha_nac',
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
            'duracion': 'Duracion',
            
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        
                    }
                ),
                'precio': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'duracion': TextInput(
                    attrs={
                         'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                )
         
         
        }

FormMembresia.field_order = [
            'nombre',
            'precio',
            'duracion'
        ]
        

