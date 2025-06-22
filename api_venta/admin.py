from django.contrib import admin
from .models import Carrito, Pedido, Pago

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

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pago', 'total_pagado', 'despacho')
    list_filter = ('despacho', 'fecha_pago')
    search_fields = ('usuario__nombre', 'usuario__email')
    readonly_fields = ('fecha_pago',)
    filter_horizontal = ('pedidos',)  # Para poder seleccionar los pedidos asociados fácilmente en admin
