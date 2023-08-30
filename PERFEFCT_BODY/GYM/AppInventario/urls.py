from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('Producto/ListadoCategoria/',login_required(views.ListCategoria.as_view()), name='lista_categoria'),
    path('Producto/CrearProducto/',login_required(views.CreateProducto.as_view()), name='crear_producto'),
    path('Producto/',login_required(views.ListProducto.as_view()), name='lista_productos'),
    path('Producto/ActualizarProductos/<int:pk>/', login_required(views.UpdateProducto.as_view()), name='actualizar_producto'),
    path('Producto/EliminarProducto/<int:pk>/', login_required(views.DeleteProducto), name='eliminar_producto'),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
