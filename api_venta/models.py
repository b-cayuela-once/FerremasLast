from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Carrito(models.Model):
    """
    Modelo que representa el carrito de compras de un usuario.
    Un carrito está asociado a un único usuario y contiene una lista de productos.
    """
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carrito'
    )
    productos = models.JSONField(
        default=list,
        help_text="Lista de productos en formato JSON: [{id, nombre, precio, imagen, cantidad}]"
    )
    despacho = models.BooleanField(
        default=False,
        help_text="Indica si el usuario seleccionó despacho a domicilio."
    )
    bloqueado = models.BooleanField(
        default=False,
        help_text="Indica si el carrito está bloqueado para modificaciones."
    )
    actualizado = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de la última actualización del carrito."
    )

    def __str__(self):
        return f"Carrito de {self.usuario.nombre}"

    def total(self):
        """
        Calcula el total del carrito sumando el precio * cantidad de cada producto,
        y agrega un costo fijo de despacho si está activado.
        """
        subtotal = sum(item['precio'] * item['cantidad'] for item in self.productos)
        return subtotal + (5000 if self.despacho else 0)


class Pedido(models.Model):
    """
    Modelo que representa un pedido realizado por un usuario.
    Contiene los productos en el momento del pedido, el total, estado y otros flags.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se creó el pedido."
    )
    productos = models.JSONField(
        help_text="Copia exacta del carrito en el momento del pedido."
    )
    total = models.IntegerField(
        help_text="Total a pagar por el pedido (en la moneda local)."
    )
    despacho = models.BooleanField(
        default=False,
        help_text="Indica si el pedido incluye despacho a domicilio."
    )
    aprobado = models.BooleanField(
        null=True,
        help_text="Estado de aprobación: None=pending, True=approved, False=rejected."
    )
    preparado = models.BooleanField(
        default=False,
        help_text="Indica si el pedido fue preparado."
    )
    entregado = models.BooleanField(
        default=False,
        help_text="Indica si el pedido fue entregado al cliente."
    )
    pagado = models.BooleanField(
        default=False,
        help_text="Indica si el pedido fue pagado."
    )

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.nombre} - ${self.total}"

    @property
    def estado(self):
        """
        Retorna el estado textual del pedido según los flags internos.
        """
        if self.aprobado is None:
            return "Pendiente"
        elif self.aprobado is True:
            return "Aprobado"
        elif self.preparado is False:
            return "Rechazado"
        else:
            return "Listo para " + ("despacho" if self.despacho else "retiro")


class Pago(models.Model):
    """
    Modelo que representa un pago realizado por un usuario,
    que puede estar asociado a uno o más pedidos.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pagos'
    )
    pedidos = models.ManyToManyField(
        Pedido,
        help_text="Pedidos asociados a este pago."
    )
    fecha_pago = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se realizó el pago."
    )
    total_pagado = models.PositiveIntegerField(
        help_text="Monto total pagado."
    )
    despacho = models.BooleanField(
        default=False,
        help_text="Indica si el pago incluye despacho."
    )

    def __str__(self):
        # Intenta obtener nombre o email del usuario para representación legible
        nombre_usuario = getattr(self.usuario, 'nombre', None) or getattr(self.usuario, 'email', 'Usuario desconocido')
        return f"Pago #{self.id} - Usuario: {nombre_usuario} - Total: ${self.total_pagado}"