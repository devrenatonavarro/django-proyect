# -*- coding: utf-8 -*-
"""
Controllers: Cliente Views
Vistas relacionadas con la gestión de clientes (registro, login, carrito, pedidos).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from core.models import Cliente, Producto, Carrito, DetalleCarrito, Pedido, DetallePedido
from decimal import Decimal


def ubicacion(request):
    """Vista de ubicación y contacto"""
    # Obtener cantidad de items en el carrito si hay sesión
    cantidad_carrito = 0
    if 'cliente_id' in request.session:
        cliente = Cliente.objects.get(id=request.session['cliente_id'])
        carrito = Carrito.objects.filter(cliente=cliente, activo=True).first()
        if carrito:
            cantidad_carrito = carrito.detalles.aggregate(
                total=Sum('cantidad')
            )['total'] or 0
    
    context = {
        'cantidad_carrito': cantidad_carrito,
        'cliente_autenticado': 'cliente_id' in request.session
    }
    return render(request, 'core/ubicacion.html', context)


def index(request):
    """Vista principal: muestra productos disponibles"""
    productos = Producto.objects.filter(activo=True, eliminado=False)
    
    # Obtener cantidad de items en el carrito si hay sesión
    cantidad_carrito = 0
    if 'cliente_id' in request.session:
        cliente = Cliente.objects.get(id=request.session['cliente_id'])
        carrito = Carrito.objects.filter(cliente=cliente, activo=True).first()
        if carrito:
            cantidad_carrito = carrito.detalles.aggregate(
                total=Sum('cantidad')
            )['total'] or 0
    
    context = {
        'productos': productos,
        'cantidad_carrito': cantidad_carrito,
        'cliente_autenticado': 'cliente_id' in request.session
    }
    return render(request, 'core/index.html', context)


def registro(request):
    """Vista para registrar nuevos clientes"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validaciones
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden')
            return render(request, 'core/registro.html')
        
        if Cliente.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return render(request, 'core/registro.html')
        
        # Crear cliente
        cliente = Cliente.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion,
            password=make_password(password)
        )
        
        messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión')
        return redirect('login')
    
    return render(request, 'core/registro.html')


def login(request):
    """Vista para iniciar sesión de clientes"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            cliente = Cliente.objects.get(email=email)
            if check_password(password, cliente.password):
                # Crear sesión
                request.session['cliente_id'] = cliente.id
                request.session['cliente_nombre'] = cliente.nombre
                messages.success(request, f'¡Bienvenido {cliente.nombre}!')
                return redirect('index')
            else:
                messages.error(request, 'Credenciales incorrectas')
        except Cliente.DoesNotExist:
            messages.error(request, 'Credenciales incorrectas')
    
    return render(request, 'core/login.html')


def logout(request):
    """Vista para cerrar sesión"""
    if 'cliente_id' in request.session:
        del request.session['cliente_id']
        del request.session['cliente_nombre']
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('index')


def agregar_al_carrito(request, producto_id):
    """Vista para agregar productos al carrito"""
    if 'cliente_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para agregar productos al carrito')
        return redirect('login')
    
    cliente = Cliente.objects.get(id=request.session['cliente_id'])
    producto = get_object_or_404(Producto, id=producto_id, activo=True, eliminado=False)
    
    # Obtener o crear carrito activo
    carrito, created = Carrito.objects.get_or_create(
        cliente=cliente,
        activo=True
    )
    
    # Obtener o crear detalle del carrito
    detalle, created = DetalleCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={'cantidad': 1}
    )
    
    if not created:
        # Si ya existe, incrementar cantidad
        detalle.cantidad += 1
        detalle.save()
        messages.success(request, f'Cantidad de {producto.nombre} actualizada en el carrito')
    else:
        messages.success(request, f'{producto.nombre} agregado al carrito')
    
    return redirect('index')


def ver_carrito(request):
    """Vista para ver el carrito de compras"""
    if 'cliente_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para ver tu carrito')
        return redirect('login')
    
    cliente = Cliente.objects.get(id=request.session['cliente_id'])
    carrito = Carrito.objects.filter(cliente=cliente, activo=True).first()
    
    detalles = []
    total = Decimal('0.00')
    
    if carrito:
        detalles = carrito.detalles.select_related('producto').all()
        # Calcular total
        for detalle in detalles:
            subtotal = detalle.producto.precio * detalle.cantidad
            detalle.subtotal = subtotal
            total += subtotal
    
    context = {
        'carrito': carrito,
        'detalles': detalles,
        'total': total,
        'cliente_autenticado': True
    }
    return render(request, 'core/carrito.html', context)


def actualizar_cantidad_carrito(request, detalle_id):
    """Vista para actualizar la cantidad de un producto en el carrito"""
    if 'cliente_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        detalle = get_object_or_404(DetalleCarrito, id=detalle_id)
        
        # Verificar que el carrito pertenece al cliente
        if detalle.carrito.cliente.id != request.session['cliente_id']:
            messages.error(request, 'Acción no permitida')
            return redirect('ver_carrito')
        
        if cantidad > 0:
            detalle.cantidad = cantidad
            detalle.save()
            messages.success(request, 'Cantidad actualizada')
        else:
            detalle.delete()
            messages.success(request, 'Producto eliminado del carrito')
    
    return redirect('ver_carrito')


def eliminar_del_carrito(request, detalle_id):
    """Vista para eliminar un producto del carrito"""
    if 'cliente_id' not in request.session:
        return redirect('login')
    
    detalle = get_object_or_404(DetalleCarrito, id=detalle_id)
    
    # Verificar que el carrito pertenece al cliente
    if detalle.carrito.cliente.id != request.session['cliente_id']:
        messages.error(request, 'Acción no permitida')
        return redirect('ver_carrito')
    
    producto_nombre = detalle.producto.nombre
    detalle.delete()
    messages.success(request, f'{producto_nombre} eliminado del carrito')
    
    return redirect('ver_carrito')


def finalizar_compra(request):
    """Vista para finalizar la compra y crear el pedido"""
    if 'cliente_id' not in request.session:
        return redirect('login')
    
    cliente = Cliente.objects.get(id=request.session['cliente_id'])
    carrito = Carrito.objects.filter(cliente=cliente, activo=True).first()
    
    if not carrito or not carrito.detalles.exists():
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('index')
    
    # Calcular total
    total = Decimal('0.00')
    detalles = carrito.detalles.select_related('producto').all()
    for detalle in detalles:
        total += detalle.producto.precio * detalle.cantidad
    
    # Crear pedido
    pedido = Pedido.objects.create(
        cliente=cliente,
        total_venta=total,
        estado='EN_PREPARACION'
    )
    
    # Crear detalles del pedido
    for detalle in detalles:
        DetallePedido.objects.create(
            pedido=pedido,
            producto=detalle.producto,
            producto_nombre=detalle.producto.nombre,
            cantidad=detalle.cantidad,
            precio_unitario=detalle.producto.precio
        )
    
    # Desactivar carrito
    carrito.activo = False
    carrito.save()
    
    messages.success(request, f'¡Pedido {pedido.codigo_unico} realizado exitosamente!')
    return redirect('mis_pedidos')


def mis_pedidos(request):
    """Vista para ver los pedidos del cliente"""
    if 'cliente_id' not in request.session:
        return redirect('login')
    
    cliente = Cliente.objects.get(id=request.session['cliente_id'])
    pedidos = Pedido.objects.filter(cliente=cliente).prefetch_related('detalles__producto')
    
    context = {
        'pedidos': pedidos,
        'cliente_autenticado': True
    }
    return render(request, 'core/mis_pedidos.html', context)
