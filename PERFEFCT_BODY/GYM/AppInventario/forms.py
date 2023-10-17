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
class FormCompra(ModelForm):   
    class Meta:
        model=Compra
        fields = {
            'cantidad',
            'precio_unitario',
            'total',
            'fecha_vec',
            'producto',
            'proveedor',
        
        }
        labels={
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio Unitario',
            'total': 'Total',
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
                'total': TextInput(
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
        
