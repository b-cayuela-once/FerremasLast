from django.urls import path
from . import views
from .views import ProductoAPIView

urlpatterns = [
    # LISTA DE PRODUCTOS MODIFICABLES POR ADMIN.
    path('lista_productos', views.lista_productos, name='lista_productos'),
    
    # VISTA BASE PARA EL ADMIN.
    path('admin_site/', views.admin_site, name='admin_site'),
    
    # OPCIONES PARA CREAR, EDITAR O ELIMINAR PRODUCTOS POR ADMIN.
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    
    # API CREAR PRODUCTOS.
    path('api/', ProductoAPIView.as_view(), name='api_productos'),
    
    # VISTA PARA PRODUCTOS.
    path('catalogo/', views.catalogo, name='catalogo'),
    # VISTA PARA CARRITO DE COMPRAS.
    path('carrito/', views.carrito, name='carrito'),

]