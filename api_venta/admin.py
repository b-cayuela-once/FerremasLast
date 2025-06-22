from django.contrib import admin
from .models import Carrito, Pedido, Pago

# Registro y configuración del modelo Carrito en el admin de Django
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    """
    Configuración para la administración del modelo Carrito.
    Muestra columnas relevantes, y permite búsqueda por nombre y email del usuario asociado.
    """
    list_display = ('usuario', 'despacho', 'bloqueado', 'actualizado')  # Campos que se muestran en la lista
    search_fields = ('usuario__nombre', 'usuario__email')  # Permite buscar carritos por nombre o email del usuario


# Registro y configuración del modelo Pedido en el admin de Django
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    Configuración para la administración del modelo Pedido.
    Muestra columnas importantes, añade filtros para facilitar la búsqueda y define campos de solo lectura.
    """
    list_display = ('id', 'usuario', 'fecha', 'total', 'despacho', 'aprobado')  # Columnas visibles en la lista
    list_filter = ('aprobado', 'despacho', 'fecha')  # Filtros en la barra lateral para filtrar pedidos
    search_fields = ('usuario__nombre', 'usuario__email')  # Permite búsqueda por nombre o email del usuario
    readonly_fields = ('fecha', 'productos')  # Campos que no se pueden modificar desde el admin


# Registro y configuración del modelo Pago en el admin de Django
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    """
    Configuración para la administración del modelo Pago.
    Define campos visibles, filtros, búsquedas, campos solo lectura, y configuración para relación many-to-many.
    """
    list_display = ('id', 'usuario', 'fecha_pago', 'total_pagado', 'despacho')  # Columnas visibles en la lista
    list_filter = ('despacho', 'fecha_pago')  # Filtros para facilitar la búsqueda
    search_fields = ('usuario__nombre', 'usuario__email')  # Búsqueda por nombre o email del usuario
    readonly_fields = ('fecha_pago',)  # Campo de solo lectura, no modificable en admin
    filter_horizontal = ('pedidos',)  # Interfaz horizontal para seleccionar pedidos asociados (relación many-to-many)
