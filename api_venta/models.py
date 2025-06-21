from django.db import models
from django.conf import settings

class Carrito(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carrito')
    productos = models.JSONField(default=list)  # Estructura: [{id, nombre, precio, imagen, cantidad}]
    despacho = models.BooleanField(default=False)
    bloqueado = models.BooleanField(default=False)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.nombre}"

    def total(self):
        subtotal = sum(item['precio'] * item['cantidad'] for item in self.productos)
        return subtotal + (5000 if self.despacho else 0)


class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.JSONField()  # Copia exacta del carrito en el momento del pedido
    total = models.IntegerField()
    despacho = models.BooleanField(default=False)
    aprobado = models.BooleanField(null=True)  # None = pendiente, True = aprobado, False = rechazado
    preparado = models.BooleanField(default=False)  # Nuevo campo
    entregado = models.BooleanField(default=False)  # NUEVO CAMPO


    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.nombre} - ${self.total}"

    @property
    def estado(self):
        if self.aprobado is None:
            return "Pendiente"
        elif self.aprobado is True:
            return "Aprobado"
        elif self.preparado is False:
            return "Rechazado"
        else:
            return "Listo para " + ("despacho" if self.despacho else "retiro")
