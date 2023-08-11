from AppUsers.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import  DateField, DateInput, ModelForm, Select, TextInput

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
                        'class': 'form-select',
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
        
