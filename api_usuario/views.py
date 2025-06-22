from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import Usuario
from .serializers import (
    SignupSerializer, CreateStaffSerializer, LoginSerializer,
    LoginStaffSerializer, ForgotPasswordSerializer
)
from django.contrib.auth import login, logout
from django.shortcuts import redirect



# ----------------------------------------------- #
# / TEMPLATES API.
# ----------------------------------------------- #

# /signup
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Usuario cliente creado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /create-staff
class CreateStaffView(APIView):
    def post(self, request):
        serializer = CreateStaffSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Usuario staff creado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /login
class LoginView(APIView):
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

# /login-staff
class LoginStaffView(APIView):
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
                # Aquí retornamos también el tipo de usuario
                return Response({
                    'mensaje': 'Login staff exitoso',
                    'change_password_required': False,
                    'tipo_usuario': user.tipo_usuario  # <--- esto es lo que necesitaba tu JS
                })
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return redirect('/') 

# /forgot-password
class ForgotPasswordStaffView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            nombre = serializer.validated_data['nombre']
            nueva_pass = serializer.validated_data['nueva_password']
            try:
                user = Usuario.objects.get(nombre=nombre)
                user.set_password(nueva_pass)
                user.must_change_password = False  # <-- marcar que ya cambió
                user.save()
                return Response({
                    'mensaje': 'Contraseña actualizada',
                    'tipo_usuario': user.tipo_usuario  # 👈 asegúrate que este campo exista en tu modelo Usuario
                })


            except Usuario.DoesNotExist:
                return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------------------------------------- #
# / TEMPLATES HTML.
# ----------------------------------------------- #
from django.shortcuts import render

# api_usuario/signup.html
def signup_template(request):
    return render(request, 'api_usuario/signup.html')

# api_usuario/login.html
def login_cliente_template(request):
    return render(request, 'api_usuario/login.html')

# api_usuario/login-staff.html
def login_staff_template(request):
    return render(request, 'api_usuario/login-staff.html')

# api_usuario/forgot-password-staff.html
def forgot_password_staff_template(request):
    return render(request, 'api_usuario/forgot-password-staff.html')

# api_usuario/welcome-staff.html
def welcome_staff_template(request):
    return render(request, 'api_usuario/welcome-staff.html')

# api_usuario/create-staff.html
def create_staff_template(request):
    return render(request, 'api_usuario/create-staff.html')










