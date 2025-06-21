from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Producto
from .serializers import ProductoSerializer
from django.contrib.auth.decorators import login_required

# LISTAR productos
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'api_catalogo/lista.html', {'productos': productos})

# CREAR producto
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'api_catalogo/formulario.html', {'form': form})

# EDITAR producto
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'api_catalogo/formulario.html', {'form': form})

# ELIMINAR producto
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'api_catalogo/confirmar_eliminar.html', {'producto': producto})

class ProductoAPIView(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
def catalogo(request):
    return render(request, 'api_catalogo/catalogo.html')

def admin_site(request):
    return render(request, 'api_catalogo/admin_site.html')

# VISTA CARRITO.
@login_required
def carrito(request):
    return render(request, 'api_catalogo/carrito.html')
