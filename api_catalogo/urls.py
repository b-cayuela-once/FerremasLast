from django.urls import path
from . import views
from .views import ProductoAPIView

urlpatterns = [
    # ============================================
    # 🛠️ PANEL ADMINISTRADOR Y GESTIÓN DE PRODUCTOS
    # ============================================

    # Lista de productos accesible para el administrador.
    path('lista_productos', views.lista_productos, name='lista_productos'),

    # Vista principal del panel de administración.
    path('admin_site/', views.admin_site, name='admin_site'),

    # Formulario para crear un nuevo producto.
    path('crear/', views.crear_producto, name='crear_producto'),

    # Formulario para editar un producto existente (por ID).
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),

    # Vista para confirmar y eliminar un producto (por ID).
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),

    # ============================================
    # 🌐 API DE PRODUCTOS
    # ============================================

    # Endpoint API que entrega todos los productos en formato JSON.
    # Usado principalmente por el catálogo del cliente (vía fetch JS).
    path('api/', ProductoAPIView.as_view(), name='api_productos'),

    # ============================================
    # 🛒 VISTAS CLIENTE
    # ============================================

    # Página del catálogo de productos visible para usuarios.
    path('catalogo/', views.catalogo, name='catalogo'),

    # Página del carrito de compras del usuario (requiere login).
    path('carrito/', views.carrito, name='carrito'),
]
