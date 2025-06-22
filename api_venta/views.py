from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api_catalogo.models import Producto
from .models import Pedido, Carrito, Pago
from .serializers import CarritoSerializer

import json
import uuid
from transbank.webpay.webpay_plus.transaction import Transaction


# ----------------------------------------------
# VISTAS HTML PARA ADMINISTRACIÓN / VENTA
# ----------------------------------------------

def vendedor_site(request):
    """
    Vista principal para el dashboard del vendedor.
    """
    return render(request, 'api_venta/vendedor_site.html')

def lista_vendedor(request):
    """
    Muestra una lista de todos los productos disponibles para el vendedor.
    """
    productos = Producto.objects.all()
    return render(request, 'api_venta/lista_vendedor.html', {'productos': productos})

@login_required
def aprobar_rechazar(request):
    """
    Muestra los pedidos pendientes de aprobación o entregados parcialmente.
    """
    pedidos = Pedido.objects.select_related('usuario').filter(
        Q(aprobado__isnull=True) | Q(aprobado=True, entregado=False)
    ).order_by('-fecha')
    return render(request, 'api_venta/aprobar_rechazar.html', {'pedidos': pedidos})

def bodeguero_site(request):
    """
    Vista del bodeguero con pedidos que ya han sido aprobados.
    """
    pedidos = Pedido.objects.filter(aprobado=True)
    return render(request, 'api_venta/bodeguero_site.html', {'pedidos': pedidos})

@require_POST
def preparar_pedido(request, pedido_id):
    """
    Marca un pedido como preparado.
    """
    pedido = Pedido.objects.get(pk=pedido_id)
    pedido.preparado = True
    pedido.save()
    return redirect('bodeguero_site')

@require_POST
@login_required
def confirmar_entrega(request, pedido_id):
    """
    Confirma que un pedido fue entregado.
    """
    pedido = get_object_or_404(Pedido, id=pedido_id, aprobado=True, preparado=True, entregado=False)
    pedido.entregado = True
    pedido.save()
    return redirect('aprobar_rechazar')

def contador_site(request):
    """
    Vista principal para el dashboard del contador.
    """
    pagos = Pago.objects.all().order_by('-fecha_pago')
    return render(request, 'api_venta/contador_site.html', {'pagos': pagos})




# ----------------------------------------------
# API: OBTENER Y ACTUALIZAR CARRITO
# ----------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def obtener_carrito(request):
    """
    Devuelve el carrito actual del usuario, si está aprobado,
    y el ID del último pedido (para WebPay).
    """
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    serializer = CarritoSerializer(carrito)

    ultimo_pedido = Pedido.objects.filter(usuario=request.user).order_by('-fecha').first()
    aprobado = ultimo_pedido.aprobado if ultimo_pedido else None
    pedido_id = ultimo_pedido.id if ultimo_pedido else None

    data = serializer.data
    data['pedido_aprobado'] = aprobado
    data['ultimo_pedido_id'] = pedido_id

    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def actualizar_carrito(request):
    """
    Actualiza los productos, estado de despacho y bloqueo del carrito del usuario.
    """
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
# API: CREACIÓN DE PEDIDO
# ----------------------------------------------

@csrf_exempt
@login_required
def crear_pedido(request):
    """
    Crea un nuevo pedido basado en los datos del carrito del usuario.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            productos = data.get('productos', [])
            total = data.get('total', 0)
            despacho = data.get('despacho', False)

            pedido = Pedido.objects.create(
                usuario=request.user,
                productos=productos,
                total=total,
                despacho=despacho,
            )

            carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
            carrito.bloqueado = True
            carrito.save()

            return JsonResponse({'status': 'ok', 'pedido_id': pedido.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


# ----------------------------------------------
# API: APROBAR O RECHAZAR PEDIDOS
# ----------------------------------------------

@login_required
def aprobar_pedido(request, pedido_id):
    """
    Aprueba un pedido específico si aún no ha sido aprobado/rechazado.
    """
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id, aprobado=None)
        pedido.aprobado = True
        pedido.save()
        return redirect('aprobar_rechazar')
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def rechazar_pedido(request, pedido_id):
    """
    Rechaza un pedido específico y desbloquea el carrito del usuario.
    """
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id, aprobado=None)
        pedido.aprobado = False
        pedido.save()

        carrito = Carrito.objects.filter(usuario=pedido.usuario).first()
        if carrito:
            carrito.bloqueado = False
            carrito.save()

        return redirect('aprobar_rechazar')
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


# ----------------------------------------------
# API: INTEGRACIÓN CON WEBPAY (SDK TRANSBANK)
# ----------------------------------------------

# Instancia global de transacción configurada para ambiente de pruebas
transaction = Transaction()
transaction.configure_for_testing()

from django.views.decorators.http import require_POST

@require_POST
@login_required
def iniciar_pago(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pedido_id = data.get('pedido_id')
            amount = data.get('total')

            if not pedido_id or not amount:
                return JsonResponse({'status': 'error', 'message': 'Faltan datos'}, status=400)

            buy_order = str(pedido_id)  # puedes usar el ID directamente
            session_id = str(uuid.uuid4())
            return_url = request.build_absolute_uri('/api/venta/webpay-respuesta/')

            response = transaction.create(buy_order, session_id, amount, return_url)

            return JsonResponse({
                'status': 'ok',
                'redirect_url': response['url'] + '?token_ws=' + response['token']
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def webpay_respuesta(request):
    """
    Procesa la respuesta de WebPay, y actualiza el estado del pedido.
    """
    token = request.POST.get('token_ws') or request.GET.get('token_ws')
    if not token:
        return HttpResponse("Token no encontrado", status=400)

    response = transaction.commit(token)

    if response.get('status') == 'AUTHORIZED':
        # Obtener el ID del pedido desde buy_order
        pedido_id = response.get('buy_order')
        pedido = Pedido.objects.filter(id=pedido_id).first()
        if pedido:
            pedido.pagado = True  # ⚠️ Asegúrate de tener este campo en tu modelo Pedido
            pedido.save()

        return render(request, 'api_venta/pago_exitoso.html', {'response': response})
    else:
        return render(request, 'api_venta/pago_rechazado.html', {'response': response})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_pago(request):
    """
    Registra el pago final y crea un objeto Pago.
    """
    usuario = request.user
    data = request.data

    try:
        pedido_ids = data.get('pedidos')  # Lista de IDs de pedidos
        despacho = data.get('despacho', False)
        total = data.get('total')

        if not pedido_ids or not isinstance(pedido_ids, list):
            return Response({'error': 'Lista de pedidos inválida'}, status=400)

        pedidos = Pedido.objects.filter(id__in=pedido_ids, usuario=usuario)

        if pedidos.count() != len(pedido_ids):
            return Response({'error': 'Algunos pedidos no existen o no pertenecen al usuario'}, status=400)

        # Marcar los pedidos como pagados
        pedidos.update(pagado=True)

        # Crear el pago
        pago = Pago.objects.create(
            usuario=usuario,
            total_pagado=total,
            despacho=despacho,
        )

        pago.pedidos.set(pedidos)
        pago.save()

        return Response({'status': 'ok', 'mensaje': '✅ Pago registrado correctamente', 'pago_id': pago.id})

    except Exception as e:
        print("Error al registrar el pago:", e)
        return Response({'error': 'Error interno al registrar el pago'}, status=500)
