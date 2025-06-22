from django.urls import path
from . import views

urlpatterns = [
    # ---------------------------------------------
    # RUTAS PARA EL PANEL DE VENDEDOR
    # ---------------------------------------------
    path('vendedor_site/', views.vendedor_site, name='vendedor_site'),
    # Vista principal del panel de vendedor.

    path('lista_vendedor/', views.lista_vendedor, name='lista_vendedor'),
    # Muestra la lista de pedidos o ítems para el vendedor.

    path('aprobar_rechazar/', views.aprobar_rechazar, name='aprobar_rechazar'),
    # Ruta para manejar la aprobación o rechazo general de pedidos (puede ser con POST).

    path('aprobar_pedido/<int:pedido_id>/', views.aprobar_pedido, name='aprobar_pedido'),
    # Aprobar un pedido específico identificado por su ID.

    path('rechazar_pedido/<int:pedido_id>/', views.rechazar_pedido, name='rechazar_pedido'),
    # Rechazar un pedido específico identificado por su ID.

    path('confirmar_entrega/<int:pedido_id>/', views.confirmar_entrega, name='confirmar_entrega'),
    # Confirmar que un pedido ha sido entregado.

    # ---------------------------------------------
    # RUTAS PARA EL PANEL DE BODEGUERO
    # ---------------------------------------------
    path('bodeguero_site/', views.bodeguero_site, name='bodeguero_site'),
    # Vista principal del panel de bodeguero.

    path('preparar-pedido/<int:pedido_id>/', views.preparar_pedido, name='preparar_pedido'),
    # Marcar un pedido como preparado por el bodeguero.

    # ---------------------------------------------
    # RUTA PARA EL PANEL DE CONTADOR
    # ---------------------------------------------
    path('contador_site/', views.contador_site, name='contador_site'),
    # Vista principal del panel de contador.

    # ---------------------------------------------
    # RUTAS PARA LA CREACIÓN Y MANEJO DE PEDIDOS
    # ---------------------------------------------
    path('obtener_carrito/', views.obtener_carrito, name='obtener_carrito'),
    # Obtener el contenido actual del carrito de un usuario.

    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),
    # Actualizar el carrito (agregar, modificar o eliminar productos).

    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    # Crear un nuevo pedido a partir del carrito.

    # ---------------------------------------------
    # RUTAS RELACIONADAS CON WEBPAY (PAGO ONLINE)
    # ---------------------------------------------
    path('pagar/', views.iniciar_pago, name='iniciar_pago'),
    # Iniciar proceso de pago vía WebPay.

    path('webpay-respuesta/', views.webpay_respuesta, name='webpay_respuesta'),
    # Endpoint para recibir la respuesta del pago WebPay (confirmación, rechazo).

    path('registrar-pago/', views.registrar_pago, name='registrar_pago'),
    # Registrar el pago realizado para actualizar estado en el sistema.
]
