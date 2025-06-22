# ===================================================
# urls.py - Definición de rutas para API y vistas HTML
# ===================================================

# ---------------------------------------------------
# 📦 IMPORTS
# ---------------------------------------------------
from django.urls import path

# Importación de vistas basadas en API (clases)
from .views import (
    SignupView, CreateStaffView, LoginView,
    LoginStaffView, LogoutView, ForgotPasswordStaffView
)

# Importación de vistas para renderizar plantillas HTML (funciones)
from .views import (
    signup_template, login_cliente_template,
    login_staff_template, forgot_password_staff_template,
    welcome_staff_template, create_staff_template
)

# ---------------------------------------------------
# 🔗 Definición de rutas URL
# ---------------------------------------------------
urlpatterns = [

    # -----------------------------------------------
    # API ENDPOINTS
    # -----------------------------------------------

    # Rutas para usuarios tipo CLIENTE
    path('signup', SignupView.as_view(), name='signup'),                  # Registro usuario cliente
    path('login', LoginView.as_view(), name='login'),                     # Login usuario cliente

    # Rutas para usuarios tipo STAFF (administrador, vendedor, bodeguero, contador)
    path('create-staff', CreateStaffView.as_view(), name='create-staff'), # Crear usuario staff
    path('login-staff', LoginStaffView.as_view(), name='login-staff'),    # Login usuario staff
    path('forgot-password-staff', ForgotPasswordStaffView.as_view(), name='forgot-password-staff'),  # Restablecer contraseña staff

    # Ruta para cerrar sesión (logout), disponible para cualquier usuario
    path('logout', LogoutView.as_view(), name='logout'),

    # -----------------------------------------------
    # VISTAS HTML (Páginas para interfaz web)
    # -----------------------------------------------

    # Formularios para usuarios tipo CLIENTE
    path('signup-form', signup_template, name='signup-form'),             # Formulario registro cliente
    path('login-form', login_cliente_template, name='login-form'),        # Formulario login cliente

    # Formularios para usuarios tipo STAFF (administrador, vendedor, bodeguero, contador)
    path('create-staff-form', create_staff_template, name='create-staff-form'),    # Formulario creación staff
    path('login-form-staff', login_staff_template, name='login-form-staff'),       # Formulario login staff
    path('forgot-password-staff-form', forgot_password_staff_template, name='forgot-password-staff-form'), # Formulario recuperar contraseña staff
    path('welcome-staff', welcome_staff_template, name='welcome-staff'),            # Página de bienvenida staff
]