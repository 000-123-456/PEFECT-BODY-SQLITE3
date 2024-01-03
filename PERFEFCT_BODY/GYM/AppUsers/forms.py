from django import forms
from AppUsers.models import User,Empresa
from django.contrib.auth.forms import UserCreationForm
from django.forms import  DateField, DateInput, ModelForm, Select, TextInput,ClearableFileInput,NumberInput,Textarea

class RegistroUsuarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['empresa'].required = False
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    class Meta:
        model = User
        fields=[
            'username',
            'first_name',
            'last_name',
            'email',
            'rol',
            'empresa',
        ]

        labels={
            'username': 'Usuario',
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'rol':'Rol',
            'empresa':'Empresa',
        }
        widgets={
                'username': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Nombre de usuario...',
                        'autocomplete':"off",
                    }
                ),
                'first_name':  TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Nombres...',
                        'autocomplete':"off",
                        
                    }
                ),
                'last_name': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Apellidos...',
                        'autocomplete':"off",
                    }
                ),
                'email': TextInput(
                    attrs={
                        'type': 'email',
                        'class': 'form-control',
                        'placeholder': 'Correo...',
                        'autocomplete':"off",
                    }
                ),
                 'rol': Select(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Seleccione el rol...',
                        'autocomplete':"off",
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
            'tarifa': 'Tarifa',
            'logo': 'Logo',
            'telefono': 'Telefono',
            'direcccion':'Dirección',
        }

#-------------------Widgets-------------------
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Perfect Body',
                        'autocomplete':"off",
                       
                    }
                ),
                'tarifa': NumberInput(
                    attrs={
                        'type': 'text',
                        'class': 'form-control',
                        'placeholder': '0.00',
                        'autocomplete':"off",
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
                    'autocomplete':"off",
                     }
                ),
                'direcccion': Textarea(
                    attrs={
                        'style':'height: 100px',
                        'class': 'form-control',
                        'placeholder': 'Casa #,Barrio,Municipio',
                        'autocomplete':"off",
                       
                    }
                ),
               
        }




FormEmpresa.field_order = [
            'nombre',
            'logo',
            'tarifa',
            'telefono',
            'direcccion',  
        ]


