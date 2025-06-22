# ===================================================
# 📁 admin.py - Configuración del panel de administración
# ===================================================

# ---------------------------------------------------
# 📦 Imports necesarios
# ---------------------------------------------------
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # Base para personalizar la vista de usuarios
from .models import Usuario  # Importa el modelo personalizado de Usuario

# ---------------------------------------------------
# ⚙️ Clase personalizada para gestionar usuarios
# ---------------------------------------------------
# Esta clase define cómo se visualizarán y gestionarán los usuarios en el panel de administración de Django.
class UsuarioAdmin(BaseUserAdmin):
    # Campos que se mostrarán en la lista de usuarios
    list_display = ('id', 'nombre', 'email', 'tipo_usuario', 'is_active')

    # Campos por los que se puede buscar
    search_fields = ('nombre', 'email')

    # Orden por defecto al mostrar la lista de usuarios
    ordering = ('nombre',)

    # Secciones y campos que se mostrarán al editar un usuario existente
    fieldsets = (
        (None, {'fields': ('nombre', 'email', 'password')}),
        ('Información Personal', {'fields': ('direccion', 'tipo_usuario')}),
        ('Permisos', {'fields': ('is_active',)}),
    )

    # Secciones y campos que se mostrarán al crear un nuevo usuario desde el admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),  # Clase para que los campos ocupen todo el ancho
            'fields': ('nombre', 'email', 'password1', 'password2'),  # Campos requeridos al crear
        }),
    )

# ---------------------------------------------------
# ✅ Registro del modelo Usuario en el admin de Django
# ---------------------------------------------------
# Se registra el modelo personalizado con la configuración de la clase UsuarioAdmin
admin.site.register(Usuario, UsuarioAdmin)
