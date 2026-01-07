# -*- coding: utf-8 -*-
"""
Controllers: Cliente Views
Vistas relacionadas con la gestión de clientes (registro, login, carrito, pedidos).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from core.models import Cliente, Categoria, Producto, Carrito, DetalleCarrito, Pedido, DetallePedido
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
    """Vista principal: muestra categorías y productos disponibles"""
    # Obtener categorías activas con sus productos
    categorias = Categoria.objects.filter(activo=True).prefetch_related(
        'productos'
    ).order_by('nombre')
    
    # Enriquecer cada categoría con sus productos
    categorias_con_productos = []
    for categoria in categorias:
        productos = categoria.productos.filter(activo=True, eliminado=False).order_by('nombre')
        if productos.exists():
            categorias_con_productos.append({
                'categoria': categoria,
                'productos': productos
            })
    
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
        'categorias_con_productos': categorias_con_productos,
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
        estado='RECIBIDO'  # Estado inicial
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
    
    # Notificar a cocina sobre nuevo pedido
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info(f"🍔 Enviando notificación de nuevo pedido {pedido.codigo_unico} a cocina...")
    
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'cocina',
            {
                'type': 'nuevo_pedido',
                'pedido_id': pedido.id,
                'codigo_unico': pedido.codigo_unico,
                'cliente_nombre': cliente.nombre,
                'total': str(total)
            }
        )
        logger.info(f"✅ Notificación enviada exitosamente para pedido {pedido.codigo_unico}")
    except Exception as e:
        logger.error(f"❌ Error al enviar notificación: {e}")
    
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


def perfil(request):
    """Vista para ver y actualizar el perfil del cliente"""
    if 'cliente_id' not in request.session:
        messages.warning(request, 'Debes iniciar sesión para ver tu perfil')
        return redirect('login')
    
    cliente = Cliente.objects.get(id=request.session['cliente_id'])
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        password_actual = request.POST.get('password_actual')
        password_nuevo = request.POST.get('password_nuevo')
        password_confirmar = request.POST.get('password_confirmar')
        
        # Validar y actualizar datos básicos
        if nombre and telefono and direccion:
            cliente.nombre = nombre
            cliente.telefono = telefono
            cliente.direccion = direccion
            
            # Si el usuario quiere cambiar la contraseña
            if password_actual and password_nuevo and password_confirmar:
                # Verificar que la contraseña actual es correcta
                if not check_password(password_actual, cliente.password):
                    messages.error(request, 'La contraseña actual es incorrecta')
                    return redirect('perfil')
                
                # Verificar que las contraseñas nuevas coincidan
                if password_nuevo != password_confirmar:
                    messages.error(request, 'Las contraseñas nuevas no coinciden')
                    return redirect('perfil')
                
                # Actualizar contraseña
                cliente.password = make_password(password_nuevo)
                messages.success(request, 'Perfil y contraseña actualizados exitosamente')
            else:
                messages.success(request, 'Perfil actualizado exitosamente')
            
            # Guardar cambios
            cliente.save()
            
            # Actualizar el nombre en la sesión
            request.session['cliente_nombre'] = cliente.nombre
            
            return redirect('perfil')
        else:
            messages.error(request, 'Todos los campos son obligatorios')
    
    # Obtener cantidad de items en el carrito
    cantidad_carrito = 0
    carrito = Carrito.objects.filter(cliente=cliente, activo=True).first()
    if carrito:
        cantidad_carrito = carrito.detalles.aggregate(
            total=Sum('cantidad')
        )['total'] or 0
    
    context = {
        'cliente': cliente,
        'cantidad_carrito': cantidad_carrito,
        'cliente_autenticado': True
    }
    return render(request, 'core/perfil.html', context)
