from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect, render
from .models import Usuario
from .serializers import (
    SignupSerializer, CreateStaffSerializer, LoginSerializer,
    LoginStaffSerializer, ForgotPasswordSerializer
)

# -----------------------------------------------
# API VIEWS - Endpoints para la API REST
# -----------------------------------------------

class SignupView(APIView):
    """
    POST /signup
    Registro de nuevos usuarios tipo CLIENTE.
    Valida los datos con SignupSerializer y crea un usuario nuevo.
    """
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Usuario cliente creado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateStaffView(APIView):
    """
    POST /create-staff
    Creación de usuarios STAFF (administrador, vendedor, bodeguero, contador).
    Usa CreateStaffSerializer para validar y guardar los datos.
    """
    def post(self, request):
        serializer = CreateStaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Usuario staff creado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /login
    Login para usuarios tipo CLIENTE.
    Valida email y contraseña, inicia sesión si son correctos.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                usuario = Usuario.objects.get(email=email)
                if usuario.check_password(password):
                    login(request, usuario)
                    return Response({'mensaje': 'Login exitoso'})
                else:
                    return Response({'error': 'Contraseña incorrecta'}, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginStaffView(APIView):
    """
    POST /login-staff
    Login para usuarios STAFF.
    Valida nombre y contraseña usando authenticate().
    Si el usuario debe cambiar contraseña, lo indica en la respuesta.
    """
    def post(self, request):
        serializer = LoginStaffSerializer(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['nombre']
            password = serializer.validated_data['password']
            user = authenticate(request, username=nombre, password=password)
            if user:
                login(request, user)
                if user.must_change_password:
                    return Response({
                        'mensaje': 'Debe cambiar su contraseña',
                        'change_password_required': True
                    })
                return Response({
                    'mensaje': 'Login staff exitoso',
                    'change_password_required': False,
                    'tipo_usuario': user.tipo_usuario  # Utilizado para redirecciones front-end
                })
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /logout
    Cierra la sesión del usuario autenticado.
    Solo accesible para usuarios autenticados.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return redirect('/')


class ForgotPasswordStaffView(APIView):
    """
    POST /forgot-password-staff
    Permite a usuarios STAFF restablecer su contraseña.
    Verifica que el usuario exista y actualiza la contraseña,
    desactivando el flag must_change_password.
    """
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['nombre']
            nueva_pass = serializer.validated_data['nueva_password']
            try:
                user = Usuario.objects.get(nombre=nombre)
                user.set_password(nueva_pass)
                user.must_change_password = False  # Usuario ya no debe cambiar contraseña
                user.save()
                return Response({
                    'mensaje': 'Contraseña actualizada',
                    'tipo_usuario': user.tipo_usuario
                })
            except Usuario.DoesNotExist:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------
# HTML TEMPLATE VIEWS - Renderización de páginas
# -----------------------------------------------

def signup_template(request):
    """
    Renderiza el template para registro de usuario cliente.
    """
    return render(request, 'api_usuario/signup.html')


def login_cliente_template(request):
    """
    Renderiza el template para login de usuario cliente.
    """
    return render(request, 'api_usuario/login.html')


def login_staff_template(request):
    """
    Renderiza el template para login de usuario staff.
    """
    return render(request, 'api_usuario/login-staff.html')


def forgot_password_staff_template(request):
    """
    Renderiza el template para formulario de recuperación de contraseña staff.
    """
    return render(request, 'api_usuario/forgot-password-staff.html')


def welcome_staff_template(request):
    """
    Renderiza el template de bienvenida para usuarios staff.
    """
    return render(request, 'api_usuario/welcome-staff.html')


def create_staff_template(request):
    """
    Renderiza el template para crear usuarios staff desde interfaz web.
    """
    return render(request, 'api_usuario/create-staff.html')
