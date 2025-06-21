# IMPORTS.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario

# CLASE PERSONALIZADA PARA MOSTRAR USUARIOS EN EL ADMIN (DJANGO).
class UsuarioAdmin(BaseUserAdmin):
    list_display = ('id', 'nombre', 'email', 'tipo_usuario', 'is_active')
    search_fields = ('nombre', 'email')
    ordering = ('nombre',)
    fieldsets = (
        (None, {'fields': ('nombre', 'email', 'password')}),
        ('Información Personal', {'fields': ('direccion', 'tipo_usuario')}),
        ('Permisos', {'fields': ('is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre', 'email', 'password1', 'password2'),
        }),
    )

# REGISTRO DEL MODELO "USUARIO" EN LA CONFIGURACIÓN PERSONALIZADA EN EL ADMIN.
admin.site.register(Usuario, UsuarioAdmin)