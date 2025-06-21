# IMPORTS.
from rest_framework import serializers
from .models import Usuario

# SignupSerializer.
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'direccion', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'direccion': {'required': True},
        }

    def validate_email(self, value):
        if Usuario.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este correo ya está en uso.")
        return value

    def create(self, validated_data):
        return Usuario.objects.create_user(
            nombre=validated_data['nombre'],
            direccion=validated_data.get('direccion'),
            email=validated_data.get('email'),
            password=validated_data['password'],
            tipo_usuario='cliente'
        )

# CreateStaffSerializer.
class CreateStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'password', 'tipo_usuario']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return Usuario.objects.create_user(
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            tipo_usuario=validated_data['tipo_usuario'],
            must_change_password=True
        )

# LoginSerializer.
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# LoginStaffSerializer.
class LoginStaffSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    password = serializers.CharField(write_only=True)

# ForgotPasswordSerializer.
class ForgotPasswordSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    nueva_password = serializers.CharField(write_only=True)