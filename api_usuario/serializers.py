# ===================================================
# 📦 serializers.py - Serializadores para Usuario
# ===================================================

# ---------------------------------------------------
# 🔧 Imports necesarios
# ---------------------------------------------------
from rest_framework import serializers
from .models import Usuario

# ---------------------------------------------------
# 📝 SignupSerializer - Registro de clientes
# ---------------------------------------------------
class SignupSerializer(serializers.ModelSerializer):
    """
    Serializador para registrar nuevos usuarios tipo 'cliente'.
    """
    class Meta:
        model = Usuario
        fields = ['nombre', 'direccion', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},      # No incluir contraseña en respuestas
            'email': {'required': True},
            'direccion': {'required': True}
        }

    def validate_email(self, value):
        """
        Valida que el correo electrónico no esté ya registrado.
        """
        if Usuario.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este correo ya está en uso.")
        return value

    def create(self, validated_data):
        """
        Crea un nuevo usuario cliente.
        """
        return Usuario.objects.create_user(
            nombre=validated_data['nombre'],
            direccion=validated_data.get('direccion'),
            email=validated_data.get('email'),
            password=validated_data['password'],
            tipo_usuario='cliente'
        )

# ---------------------------------------------------
# 👥 CreateStaffSerializer - Registro de usuarios staff
# ---------------------------------------------------
class CreateStaffSerializer(serializers.ModelSerializer):
    """
    Serializador para crear usuarios staff (vendedor, bodeguero, etc.).
    """
    class Meta:
        model = Usuario
        fields = ['nombre', 'password', 'tipo_usuario']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Crea un usuario staff forzando cambio de contraseña en primer login.
        """
        return Usuario.objects.create_user(
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            tipo_usuario=validated_data['tipo_usuario'],
            must_change_password=True
        )

# ---------------------------------------------------
# 🔐 LoginSerializer - Login general de clientes
# ---------------------------------------------------
class LoginSerializer(serializers.Serializer):
    """
    Serializador para login general con email y contraseña.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# ---------------------------------------------------
# 🔐 LoginStaffSerializer - Login para usuarios staff
# ---------------------------------------------------
class LoginStaffSerializer(serializers.Serializer):
    """
    Serializador para login de usuarios staff usando nombre y contraseña.
    """
    nombre = serializers.CharField()
    password = serializers.CharField(write_only=True)

# ---------------------------------------------------
# 🔁 ForgotPasswordSerializer - Restablecer contraseña
# ---------------------------------------------------
class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializador para restablecer la contraseña de usuarios staff.
    """
    nombre = serializers.CharField()
    nueva_password = serializers.CharField(write_only=True)