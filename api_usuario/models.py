# IMPORTS.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# MANAGER PERSONALIZADO, CREAR USUARIOS Y SUPERUSUARIOS.
class UsuarioManager(BaseUserManager):
# CREACIÓN DE USUARIOS NORMALES.
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
        user.set_password(password)
        user.save(using=self._db)
        return user
    
# CREACIÓN DE SUPER USUARIOS.
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

# MODELO DE USUARIO PERSONALIZADO.
class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO = (
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
        ('bodeguero', 'Bodeguero'),
        ('contador', 'Contador'),
        ('administrador', 'Administrador'),
    )
    # CAMPOS DEL MODELO.
    nombre = models.CharField(max_length=100, unique=True)
    email = models.EmailField(null=True, blank=True)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO)
    
    #CAMPOS REQUERIDOS POR DJANGO.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 

    # FORZAR CAMBIO DE CONTRASEÑA.
    must_change_password = models.BooleanField(default=True)  
    
    # CONFIGURACIÓN PARA LOGIN.
    USERNAME_FIELD = 'nombre'
    REQUIRED_FIELDS = ['email'] 

    # CONEXIÓN CON EL MANAGER PERSONALIZADO.
    objects = UsuarioManager()

    def __str__(self):
        return self.nombre