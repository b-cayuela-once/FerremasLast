# ===================================================
# 📁 models.py - Modelo personalizado de usuario
# ===================================================

# ---------------------------------------------------
# 📦 Imports necesarios
# ---------------------------------------------------
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# ---------------------------------------------------
# 👤 Manager personalizado de usuarios
# ---------------------------------------------------
# Esta clase administra la creación de usuarios normales y superusuarios.
class UsuarioManager(BaseUserManager):

    # 🧑 Crear un usuario estándar
    def create_user(self, nombre, email=None, password=None, direccion=None, tipo_usuario='cliente', must_change_password=True):
        if not nombre:
            raise ValueError('El usuario debe tener un nombre')

        user = self.model(
            nombre=nombre,
            email=self.normalize_email(email),
            direccion=direccion,
            tipo_usuario=tipo_usuario,
            must_change_password=must_change_password
        )
        user.set_password(password)  # Encripta la contraseña
        user.save(using=self._db)    # Guarda en la base de datos actual
        return user

    # 👑 Crear un superusuario (admin con todos los permisos)
    def create_superuser(self, nombre, email, password):
        user = self.create_user(
            nombre=nombre,
            email=email,
            password=password,
            tipo_usuario='administrador'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# ---------------------------------------------------
# 🧾 Modelo personalizado de Usuario
# ---------------------------------------------------
class Usuario(AbstractBaseUser, PermissionsMixin):
    # ⚙️ Opciones disponibles para el tipo de usuario
    TIPO_USUARIO = (
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
        ('administrador', 'Administrador'),
    )

    # 🧩 Campos principales del usuario
    nombre = models.CharField(max_length=100, unique=True)              # Nombre único (usado para login)
    email = models.EmailField(null=True, blank=True)                    # Correo electrónico
    direccion = models.CharField(max_length=255, null=True, blank=True) # Dirección física
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO) # Rol del usuario en el sistema

    # ✅ Campos requeridos por Django
    is_active = models.BooleanField(default=True)   # ¿Está activo el usuario?
    is_staff = models.BooleanField(default=False)   # ¿Tiene acceso al admin de Django?

    # 🔐 Campo personalizado: obligar a cambiar contraseña en el primer inicio
    must_change_password = models.BooleanField(default=True)

    # 🔑 Configuración para el sistema de autenticación de Django
    USERNAME_FIELD = 'nombre'       # Campo que se usará para iniciar sesión
    REQUIRED_FIELDS = ['email']     # Campos obligatorios al crear un superusuario

    # 📦 Conexión con el manager personalizado
    objects = UsuarioManager()

    # Representación legible del usuario
    def __str__(self):
        return self.nombre