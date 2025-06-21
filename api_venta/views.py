from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from api_catalogo.models import Producto
from .models import Pedido, Carrito
from .serializers import CarritoSerializer
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

import json

# ----------------------------------------------
# VISTAS HTML (ADMIN / VENDEDOR)
# ----------------------------------------------

def vendedor_site(request):
    return render(request, 'api_venta/vendedor_site.html')

def lista_vendedor(request):
    productos = Producto.objects.all()
    return render(request, 'api_venta/lista_vendedor.html', {'productos': productos})

@login_required
def aprobar_rechazar(request):
    pedidos = Pedido.objects.filter(
        Q(aprobado__isnull=True) | Q(aprobado=True, entregado=False)
    ).order_by('-fecha')
    return render(request, 'api_venta/aprobar_rechazar.html', {'pedidos': pedidos})

def bodeguero_site(request):
    pedidos = Pedido.objects.filter(aprobado=True)
    return render(request, 'api_venta/bodeguero_site.html', {'pedidos': pedidos})

@require_POST
def preparar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    pedido.preparado = True
    pedido.save()
    return redirect('bodeguero_site')

@require_POST
@login_required
def confirmar_entrega(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, aprobado=True, preparado=True, entregado=False)
    pedido.entregado = True
    pedido.save()
    return redirect('aprobar_rechazar')  # o a otra vista si lo prefieres

# ----------------------------------------------
# API: CARRITO - Obtener y sincronizar
# ----------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    serializer = CarritoSerializer(carrito)

    # Obtener el último pedido del usuario (por fecha)
    ultimo_pedido = Pedido.objects.filter(usuario=request.user).order_by('-fecha').first()
    aprobado = None
    if ultimo_pedido:
        aprobado = ultimo_pedido.aprobado

    data = serializer.data
    data['pedido_aprobado'] = aprobado  # True, False o None

    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def actualizar_carrito(request):
    try:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
        carrito.productos = request.data.get('productos', [])
        carrito.despacho = request.data.get('despacho', False)
        carrito.bloqueado = request.data.get('bloqueado', False)
        carrito.save()
        return Response({'status': 'ok'})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)

# ----------------------------------------------
# API: CREAR PEDIDO (solo si está logueado)
# ----------------------------------------------

@csrf_exempt
@login_required
def crear_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            productos = data.get('productos', [])
            total = data.get('total', 0)
            despacho = data.get('despacho', False)

            # Crear el pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                productos=productos,
                total=total,
                despacho=despacho,
            )

            # Bloquear carrito después del pedido
            carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
            carrito.bloqueado = True
            carrito.save()

            return JsonResponse({'status': 'ok', 'pedido_id': pedido.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

# ----------------------------------------------
# APROBAR Y RECHAZAR PEDIDO (POST)
# ----------------------------------------------

@login_required
def aprobar_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id, aprobado=None)
        pedido.aprobado = True
        pedido.save()
        # Aquí podrías agregar notificaciones o acciones extra
        return redirect('aprobar_rechazar')
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def rechazar_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id, aprobado=None)
        pedido.aprobado = False
        pedido.save()

        # Desbloquear el carrito del usuario
        carrito = Carrito.objects.filter(usuario=pedido.usuario).first()
        if carrito:
            carrito.bloqueado = False
            carrito.save()

        return redirect('aprobar_rechazar')
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
