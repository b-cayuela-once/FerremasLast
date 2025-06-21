from django.contrib import admin
from .models import Carrito, Pedido

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'despacho', 'bloqueado', 'actualizado')
    search_fields = ('usuario__nombre', 'usuario__email')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total', 'despacho', 'aprobado')
    list_filter = ('aprobado', 'despacho', 'fecha')
    search_fields = ('usuario__nombre', 'usuario__email')
    readonly_fields = ('fecha', 'productos')
