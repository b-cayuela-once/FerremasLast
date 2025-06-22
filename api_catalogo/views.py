# ============================================================
# 📦 VISTAS DE CATÁLOGO DE PRODUCTOS
# Funciones para listar, crear, editar y eliminar productos,
# además de vistas HTML para catálogo, carrito y panel admin.
# ============================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Producto
from .forms import ProductoForm
from .serializers import ProductoSerializer

# =============================
# 🔍 LISTAR PRODUCTOS (Admin)
# =============================
def lista_productos(request):
    """
    Muestra una tabla con todos los productos en la base de datos.
    Solo accesible desde el panel de administración.
    """
    productos = Producto.objects.all()
    return render(request, 'api_catalogo/lista.html', {'productos': productos})


# =============================
# ➕ CREAR PRODUCTO
# =============================
def crear_producto(request):
    """
    Muestra un formulario para crear un nuevo producto.
    Si el método es POST, guarda el producto si el formulario es válido.
    """
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'api_catalogo/formulario.html', {'form': form})


# =============================
# ✏️ EDITAR PRODUCTO
# =============================
def editar_producto(request, pk):
    """
    Permite editar un producto existente identificado por su ID (pk).
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'api_catalogo/formulario.html', {'form': form})


# =============================
# 🗑️ ELIMINAR PRODUCTO
# =============================
def eliminar_producto(request, pk):
    """
    Muestra confirmación para eliminar un producto.
    Elimina el producto tras confirmación vía POST.
    """
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'api_catalogo/confirmar_eliminar.html', {'producto': producto})


# =============================
# 🌐 API - LISTA DE PRODUCTOS (JSON)
# =============================
class ProductoAPIView(APIView):
    """
    Endpoint API que retorna todos los productos como JSON.
    Utilizado para cargar dinámicamente el catálogo.
    """
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)


# =============================
# 🖥️ VISTA HTML - CATÁLOGO (Cliente)
# =============================
def catalogo(request):
    """
    Renderiza la página del catálogo para clientes.
    Los productos se cargan vía fetch desde la API.
    """
    return render(request, 'api_catalogo/catalogo.html')


# =============================
# 🛠️ VISTA HTML - PANEL ADMINISTRADOR
# =============================
def admin_site(request):
    """
    Muestra el panel de administración para gestionar productos.
    """
    return render(request, 'api_catalogo/admin_site.html')


# =============================
# 🛒 VISTA HTML - CARRITO
# =============================
@login_required
def carrito(request):
    """
    Muestra la vista del carrito de compras del cliente.
    Requiere que el usuario haya iniciado sesión.
    """
    return render(request, 'api_catalogo/carrito.html')
