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
    path('Producto/get_producto/<str:name>/',login_required(views.get_producto), name='get_producto'),
    path('Producto/CrearProducto/',login_required(views.CreateProducto.as_view()), name='crear_producto'),
    path('Producto/',login_required(views.ListProducto.as_view()), name='lista_productos'),
    path('Producto/ProductosEliminados/',login_required(views.ListProductoBajas.as_view()), name='lista_bajas_productos'),
    path('Producto/ProductosEliminados/AltaProducto/<int:pk>/',login_required(views.AltaProducto), name='alta_producto'),
    path('Producto/ProductosEliminados/AltaTodos/',login_required(views.AltaTodosProducto), name='alta_todos_productos'),
    path('Producto/ActualizarProductos/<int:pk>/', login_required(views.UpdateProducto.as_view()), name='actualizar_producto'),
    path('Producto/EliminarProducto/<int:pk>/', login_required(views.DeleteProducto), name='eliminar_producto'),
    ##-----------------------FIN VISTAS DE PRODUCTO---------------------------------------


    ##------------------------------INICIO DE VISTA DE COMPRAS-----------------------------------------------------------------
    path('Compra/get_compra/<str:name>/', login_required(views.get_compra), name='get_compra'),
    path('Compra/CrearCompra/',login_required(views.CreateCompra.as_view()), name='crear_compra'),
    path('Compra/',login_required(views.ListCompra.as_view()), name='lista_compras'),
    path('Compra/ComprasEliminados/',login_required(views.ListCompraBajas.as_view()), name='lista_bajas_compras'),

    path('Compra/ComprasEliminados/AltaCompra/<int:pk>/',login_required(views.AltaCompra), name='alta_compra'),
    path('Compra/ComprasEliminados/AltaTodos/',login_required(views.AltaTodasCompra), name='alta_todos_compras'),

    
    path('Compra/ActualizarCompras/<int:pk>/', login_required(views.UpdateCompra.as_view()), name='actualizar_compra'),
    path('Compra/EliminarCompra/<int:pk>/', login_required(views.DeleteCompra), name='eliminar_compra'),

    path('Obtenerimagenpro/<int:producto_id>/', views.Obtenerimagenpro, name='Imagenproducto'),
    path('Categoriaproducto/<int:producto_id>/', views.Categoriaproducto, name='Categoriaproducto'),
    ##---------------------------------FIN DE VISTAS DE COMPRAS----------------------------------------------------------------


    ##------------------------------INICIO DE VISTA DE PROVEEDOR-----------------------------------------------------------------
    path('Proveedor/Crear/', login_required(views.CreateProveedor.as_view()), name='crear_proveedor'),
    path('Proveedor/', login_required(views.ListProveedor.as_view()), name='lista_proveedor'),
    path('Proveedor/Eliminados/',login_required(views.ListProveedorBajas.as_view()), name='lista_bajas_proveedor'),
    path('Proveedor/Eliminar/<int:pk>/', login_required(views.DeleteProveedor), name='eliminar_proveedor'),
    path('Proveedor/Alta/<int:pk>/',login_required(views.AltaProveedor), name='alta_proveedor'),
    path('Proveedor/AltaTodos/',login_required(views.AltaTodosProveedor), name='alta_todos_proveedor'),
    path('Proveedor/Actualizar/<int:pk>/', login_required(views.UpdateProveedor.as_view()), name='actualizar_proveedor'),


    ##------------------------------FIN DE VISTA DE VENTA-----------------------------------------------------------------
    path('Venta/',login_required(views.CreateVenta.as_view()), name='vista_venta'),
    path('Venta/listaProductos/',login_required(views.lista_productos), name='lista_productos_venta'),
    path('Venta/registroVenta/',login_required(views.registro_venta), name='registro_venta'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
