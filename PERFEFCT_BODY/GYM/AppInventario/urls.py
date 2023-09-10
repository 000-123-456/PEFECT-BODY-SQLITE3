from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
urlpatterns = [
    ##-----------------------INICIO VISTAS DE CATEGORIA---------------------------------------
    path('Producto/ListadoCategoria/EliminarCategoria/<int:pk>/',login_required(views.DeleteCategoria), name='eliminar_categoria'),
    path('Producto/ListadoCategoria/',login_required(views.ListCategoria.as_view()), name='lista_categoria'),
    path('Producto/ListadoCategoria/<str:name>/',login_required(views.get_categoria), name='get_categoria'),
    path('Producto/CategoriaEliminadas/AltaCategoria/<int:pk>/',login_required(views.AltaCategoria), name='alta_categoria'),
    path('Producto/CategoriaEliminadas/AltasTodas/',login_required(views.AltaTodasCategoria), name='alta_todas_categoria'),
    path('Producto/CategoriaEliminadas/',login_required(views.ListCategoriaBajas.as_view()), name='lista_baja_categoria'),
    ##-----------------------FIN VISTAS DE CATEGORIA---------------------------------------

    ##-----------------------INICIO VISTAS DE PRODUCTO--------------------------------------- 
    path('Producto/CrearProducto/',login_required(views.CreateProducto.as_view()), name='crear_producto'),
    path('Producto/',login_required(views.ListProducto.as_view()), name='lista_productos'),
    path('Producto/ProductosEliminados/',login_required(views.ListProductoBajas.as_view()), name='lista_bajas_productos'),
    path('Producto/ProductosEliminados/AltaProducto/<int:pk>/',login_required(views.AltaProducto), name='alta_producto'),
    path('Producto/ProductosEliminados/AltaTodos/',login_required(views.AltaTodosProducto), name='alta_todos_productos'),
    path('Producto/ActualizarProductos/<int:pk>/', login_required(views.UpdateProducto.as_view()), name='actualizar_producto'),
    path('Producto/EliminarProducto/<int:pk>/', login_required(views.DeleteProducto), name='eliminar_producto'),
    ##-----------------------FIN VISTAS DE CATEGORIA---------------------------------------
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
