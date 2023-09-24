from AppUsers.models import User,Empresa
from django.contrib.auth.forms import UserCreationForm
from django.forms import  DateField, DateInput, ModelForm, Select, TextInput,ClearableFileInput,NumberInput,Textarea

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields=[
            'username',
            'first_name',
            'last_name',
            'email',
            'rol',
            
        ]
        labels={
            'username': 'Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electronico',
            'rol':'Rol',
            'password1':'Ingrese la contraseña',
            'password2':' Confirme su contraseña',

        }
        widgets={
                'username': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Nombre de usuario...'
                    }
                ),
                'first_name':  TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Nombres...'
                    }
                ),
                'last_name': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Apellidos...'
                    }
                ),
                'email': TextInput(
                    attrs={
                        'type': 'email',
                        'class': 'form-select',
                        'placeholder': 'Correo...'
                    }
                ),
                 'rol': Select(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Seleccione el rol...'
                    }
                ),
                'password1': Select(
                    attrs={
                        'class': 'form-select',
                        'placeholder': 'Ingrese la contraseña...'
                    }
                ),
                
            
            }
        
#------------------------------------------------------Empresa---------------------------------------------
class FormEmpresa(ModelForm):
   
    class Meta:
        model=Empresa
        fields = [
            'nombre',
            'tarifa',
            'logo',
            'telefono',
            'direcccion',
           
        ]
        labels={
            'nombre': 'Nombre',
            'tarifa': 'Tarifa  ',
            'logo': 'logo ',
            'telefono': 'Telefono ',
            'direcccion':'Direccion ',
        }








#-----------------------------------------------------------widgets
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Perfect Body',
                       
                    }
                ),
                'tarifa': NumberInput(
                    attrs={
                        'type': 'number',
                        'step': '0.01',
                        'class': 'form-control',
                        'placeholder': '0.00',
                    }
                ),
               'logo': ClearableFileInput(  
                attrs={
                    'class': 'form-control',
                     }
                ),
                'telefono': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0000-0000',
                    'id': 'telefono',
                    'pattern': '[0-9]{4}[-][0-9]{4}',
                     }
                ),
                'direcccion': Textarea(
                    attrs={
                        'style':'height: 100px',
                        'class': 'form-control',
                        'placeholder': 'Casa #,Barrio,Municipio',
                       
                    }
                ),
               
        }




FormEmpresa.field_order = [
            'nombre',
            'tarifa',
            'logo',
            'telefono',
            'direcccion',  
        ]


