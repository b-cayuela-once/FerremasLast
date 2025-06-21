# IMPORTS.
from django.urls import path

# IMPORTS VISTAS API.
from .views import (
    SignupView, CreateStaffView, LoginView,
    LoginStaffView, LogoutView, ForgotPasswordStaffView
)

# IMPORTS VISTAS HTML.
from .views import ( 
    signup_template, login_cliente_template, 
    login_staff_template, forgot_password_staff_template,
    welcome_staff_template, create_staff_template)

urlpatterns = [

# ----------------------------------------------- #
# RUTAS API.
# ----------------------------------------------- #   
    # PARA USUARIOS DE TIPO CLIENTE.
    path('signup', SignupView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    
    # PARA USUARIOS DE TIPO ADMINISTRADOR, VENDEDOR, BODEGUERO, CONTADOR.
    path('create-staff', CreateStaffView.as_view(), name='create-staff'),
    path('login-staff', LoginStaffView.as_view(), name='login-staff'),
    path('forgot-password-staff', ForgotPasswordStaffView.as_view(), name='forgot-password-staff'),
    
    # PARA CUALQUIER TIPO DE USUARIOS.
    path('logout', LogoutView.as_view(), name='logout'),
    
# ----------------------------------------------- #   
# RUTAS HTML.
# ----------------------------------------------- #
    # PARA USUARIOS DE TIPO CLIENTE.
    path('signup-form', signup_template, name='signup-form'),
    path('login-form', login_cliente_template, name='login-form'),
    
    # PARA USUARIOS DE TIPO ADMINISTRADOR, VENDEDOR, BODEGUERO, CONTADOR.
    path('create-staff-form', create_staff_template, name='create-staff-form'),
    path('login-form-staff', login_staff_template, name='login-form-staff'),
    path('forgot-password-staff-form', forgot_password_staff_template, name='forgot-password-staff-form'),
    path('welcome-staff', welcome_staff_template, name='welcome-staff'),
]