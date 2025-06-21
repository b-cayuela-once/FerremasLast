from django.urls import path
from . import views

urlpatterns = [
    # VISTA PARA PANEL DE VENDEDOR.
    path('vendedor_site/', views.vendedor_site, name='vendedor_site'),
    path('lista_vendedor/', views.lista_vendedor, name='lista_vendedor'),
    path('aprobar_rechazar/', views.aprobar_rechazar, name='aprobar_rechazar'),
    path('aprobar_pedido/<int:pedido_id>/', views.aprobar_pedido, name='aprobar_pedido'),
    path('rechazar_pedido/<int:pedido_id>/', views.rechazar_pedido, name='rechazar_pedido'),
    path('confirmar_entrega/<int:pedido_id>/', views.confirmar_entrega, name='confirmar_entrega'),
    
    # VISTA PARA PANEL DE BODEGUERO.
    path('bodeguero_site/', views.bodeguero_site, name='bodeguero_site'),
    path('preparar-pedido/<int:pedido_id>/', views.preparar_pedido, name='preparar_pedido'),
    
    # VISTAS CREAR PEDIDO.
    path('obtener_carrito/', views.obtener_carrito, name='obtener_carrito'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    
]