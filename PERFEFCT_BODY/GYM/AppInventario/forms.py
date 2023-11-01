from django import forms
from django.forms import  ModelForm, Select, TextInput,Textarea,DateInput,ImageField,Form
from AppInventario.models import *
class FormCategoria(ModelForm):   
    class Meta:
        model=Categoria
        fields = {
            'nombre',
        }
        labels={
            'nombre': 'Nombre',
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

FormCategoria.field_order = [
            'nombre',  
        ]

class FormProducto(ModelForm):   
    class Meta:
        model=Producto
        fields = {
            'nombre',
            'descripcion',
            'precio_venta',
            'categoriaP',
            'img',
            'nivel_bajo',
        }
        labels={
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio_venta': 'Precio de venta',
            'categoriaP':'Categoría',
            'img':'Foto',
            'nivel_bajo':'Cantidad mínima',
        }
        
        widgets={
                'nombre': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'precio_venta': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'descripcion': Textarea(
                    attrs={
                        'style':'height: 100px',
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        
                    }
                ),
                
                'categoriaP': Select(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Seleccione la categoria',
                        'id':'selectPro',
                        
                        
                    }
                ),
                'nivel_bajo': TextInput(
                    attrs={
                        'type':'number',
                        'class': 'form-control',
                        'placeholder': 'Cantidad baja del producto',
                        'autocomplete':"off",
                        
                    }
                ),

        }
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.fields['categoriaP'].queryset = Categoria.objects.filter(estado=0)

FormProducto.field_order = [
            'nombre',
            'precio_venta',
            'nivel_bajo',
            'descripcion',
            'categoriaP',
            'img', 
        ]



#---------------------------------------COMPRAS--------------------------------------------------
#------------------------------------------------------------------------------------------------
                 #forms agregue con el .
class FormCompra(ModelForm):   
    #*****************esto acabo de agregar***************

    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(estado=0), 
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

  

    #************hasta aqui termina lo que acabo de agregar*********
    class Meta:
        model=Compra
        fields = {
            'cantidad',
            'precio_unitario',
            'fecha_vec',
            'producto',
            'proveedor',
        
        }

        
        labels={
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario',
            'fecha_vec':'Fecha de Vencimiento',
            'producto':'Producto',
            'proveedor':'Proveedor',
        }

        widgets={
                'cantidad': TextInput(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'precio_unitario': TextInput(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'autocomplete':"off",
                        
                    }
                ),
                'fecha_vec': DateInput(
                attrs={
                    'class': 'form-control', 
                    'type': 'date'
                }
                ),
                'producto': Select(
                    attrs={
                        
                        'class': 'form-control',
                        'placeholder': 'Ingrese nombre completo',
                        'id':'selectPro',
                        
                    }
                ),             
                'proveedor': Select(
                    attrs={
                        'class': 'form-control',
                        'placeholder': 'Cantidad baja del producto',
                        'id':'selectProve',
                        
                    }
                ),

        }
    def __init__(self, *args, **kwargs):
        super(FormCompra, self).__init__(*args, **kwargs)

        # Hacer que el campo de fecha de vencimiento sea opcional
        if 'producto' in self.data:
            producto_id = int(self.data.get('producto'))
            producto = Producto.objects.get(pk=producto_id)
            if not producto.categoriaP.perecedero:
                self.fields['fecha_vec'].required = False
        
FormCompra.field_order = [
            'producto',
            'proveedor',
            'cantidad',
            'precio_unitario',
            'fecha_vec',
        ]
