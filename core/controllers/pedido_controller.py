# -*- coding: utf-8 -*-
"""
Controllers: Pedido Views
Vistas para gestión de pedidos del restaurante.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from core.models import Usuario, Pedido
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def admin_pedidos(request):
    """Vista para gestionar todos los pedidos"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Filtros
    estado_filtro = request.GET.get('estado', '')
    
    pedidos = Pedido.objects.select_related('cliente', 'repartidor').prefetch_related('detalles__producto')
    
    # Si es Cocina, ver pedidos EN_PREPARACION y LISTO_ENTREGA
    if usuario.rol.nombre_rol == 'Cocina':
        pedidos = pedidos.filter(estado__in=['EN_PREPARACION', 'LISTO_ENTREGA'])
    elif estado_filtro:
        pedidos = pedidos.filter(estado=estado_filtro)
    
    pedidos = pedidos.order_by('-fecha_creacion')
    
    # Obtener repartidores para el select
    repartidores = Usuario.objects.filter(rol__nombre_rol='Repartidores')
    
    context = {
        'usuario': usuario,
        'pedidos': pedidos,
        'estado_filtro': estado_filtro,
        'estados': Pedido.ESTADOS,
        'repartidores': repartidores,
    }
    
    return render(request, 'core/admin/pedidos.html', context)


def admin_cambiar_estado_pedido(request, pedido_id):
    """Vista para cambiar el estado de un pedido"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    if request.method == 'POST':
        usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
        pedido = get_object_or_404(Pedido, id=pedido_id)
        nuevo_estado = request.POST.get('estado')
        
        # Validar permisos de Cocina
        if usuario.rol.nombre_rol == 'Cocina':
            # Cocina solo puede cambiar de EN_PREPARACION a LISTO_ENTREGA
            if pedido.estado != 'EN_PREPARACION':
                messages.error(request, 'Este pedido ya fue marcado como listo y no puede ser modificado')
                return redirect('admin_pedidos')
            if nuevo_estado != 'LISTO_ENTREGA':
                messages.error(request, 'Solo puedes marcar el pedido como "Listo para entrega"')
                return redirect('admin_pedidos')
        
        # Validar permisos de Repartidor
        if usuario.rol.nombre_rol == 'Repartidores':
            # Validar transiciones permitidas
            if pedido.estado == 'LISTO_ENTREGA' and nuevo_estado == 'EN_RUTA':
                # Asignar el repartidor automáticamente
                pedido.repartidor = usuario
            elif pedido.estado == 'EN_RUTA' and nuevo_estado in ['ENTREGADO', 'NO_ENTREGADO']:
                # Verificar que el pedido esté asignado a este repartidor
                if pedido.repartidor != usuario:
                    messages.error(request, 'Este pedido no está asignado a ti')
                    return redirect('admin_mis_entregas')
            else:
                messages.error(request, 'Transición de estado no permitida')
                return redirect('admin_mis_entregas')
        
        if nuevo_estado in dict(Pedido.ESTADOS):
            pedido.estado = nuevo_estado
            
            # Si el estado es ENTREGADO, registrar fecha de entrega
            if nuevo_estado == 'ENTREGADO':
                pedido.fecha_entrega = timezone.now()
            
            pedido.save()
            
            # Enviar notificación WebSocket al cliente
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'pedidos_cliente_{pedido.cliente.id}',
                {
                    'type': 'pedido_actualizado',
                    'pedido_id': pedido.id,
                    'estado': nuevo_estado,
                    'codigo_unico': pedido.codigo_unico
                }
            )
            
            # Si se marca como entregado, notificar a cajeros y admins
            if nuevo_estado == 'ENTREGADO':
                # Notificar a todos los cajeros y admins sobre la entrega
                cajeros_admins = Usuario.objects.filter(
                    rol__nombre_rol__in=['Cajeros', 'Admin']
                )
                for usuario_notif in cajeros_admins:
                    async_to_sync(channel_layer.group_send)(
                        f'ventas_usuario_{usuario_notif.id}',
                        {
                            'type': 'venta_realizada',
                            'pedido_id': pedido.id,
                            'codigo_unico': pedido.codigo_unico,
                            'total': str(pedido.total_venta),
                            'repartidor': pedido.repartidor.nombre if pedido.repartidor else 'N/A'
                        }
                    )
            
            messages.success(request, f'Estado del pedido {pedido.codigo_unico} actualizado')
        else:
            messages.error(request, 'Estado inválido')
    
    # Redirigir según el rol del usuario
    if usuario.rol.nombre_rol == 'Repartidores':
        return redirect('admin_mis_entregas')
    else:
        return redirect('admin_pedidos')


def admin_asignar_repartidor(request, pedido_id):
    """Vista para asignar un repartidor a un pedido"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        repartidor_id = request.POST.get('repartidor_id')
        
        if repartidor_id:
            repartidor = get_object_or_404(Usuario, id=repartidor_id, rol__nombre_rol='Repartidores')
            pedido.repartidor = repartidor
            pedido.save()
            messages.success(request, f'Repartidor {repartidor.nombre} asignado al pedido {pedido.codigo_unico}')
        else:
            pedido.repartidor = None
            pedido.save()
            messages.success(request, f'Repartidor removido del pedido {pedido.codigo_unico}')
        
        # Enviar notificación WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'pedidos_cliente_{pedido.cliente.id}',
            {
                'type': 'pedido_actualizado',
                'pedido_id': pedido.id,
                'estado': pedido.estado,
                'codigo_unico': pedido.codigo_unico
            }
        )
    
    return redirect('admin_pedidos')


def admin_eliminar_pedido(request, pedido_id):
    """Vista para eliminar un pedido"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin puede eliminar pedidos
    if usuario.rol.nombre_rol != 'Admin':
        messages.error(request, 'Solo el Admin puede eliminar pedidos')
        return redirect('admin_pedidos')
    
    pedido = get_object_or_404(Pedido, id=pedido_id)
    codigo = pedido.codigo_unico
    pedido.delete()
    
    messages.success(request, f'Pedido {codigo} eliminado exitosamente')
    return redirect('admin_pedidos')


def admin_reportes_ventas(request):
    """Vista para generar reportes de ventas"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin y Cajeros pueden ver reportes
    if usuario.rol.nombre_rol not in ['Admin', 'Cajeros']:
        messages.error(request, 'No tienes permiso para ver reportes')
        return redirect('admin_dashboard')
    
    # Filtros de fecha
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    
    # Pedidos entregados
    from django.db.models import Sum, Count
    ventas = Pedido.objects.filter(estado='ENTREGADO').select_related(
        'cliente', 'repartidor'
    ).prefetch_related('detalles__producto').order_by('-fecha_entrega')
    
    if fecha_inicio:
        ventas = ventas.filter(fecha_entrega__date__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha_entrega__date__lte=fecha_fin)
    
    # Calcular totales
    total_ventas = ventas.aggregate(Sum('total_venta'))['total_venta__sum'] or 0
    cantidad_pedidos = ventas.count()
    
    context = {
        'usuario': usuario,
        'ventas': ventas,
        'total_ventas': total_ventas,
        'cantidad_pedidos': cantidad_pedidos,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'core/admin/reportes_ventas.html', context)


def admin_reportes_ventas(request):
    """Vista para generar reportes de ventas"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin y Cajeros pueden ver reportes
    if usuario.rol.nombre_rol not in ['Admin', 'Cajeros']:
        messages.error(request, 'No tienes permiso para ver reportes')
        return redirect('admin_dashboard')
    
    # Filtros de fecha
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    
    # Pedidos entregados
    ventas = Pedido.objects.filter(estado='ENTREGADO').select_related(
        'cliente', 'repartidor'
    ).prefetch_related('detalles__producto').order_by('-fecha_entrega')
    
    if fecha_inicio:
        ventas = ventas.filter(fecha_entrega__date__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha_entrega__date__lte=fecha_fin)
    
    # Calcular totales
    from django.db.models import Sum, Count
    total_ventas = ventas.aggregate(Sum('total_venta'))['total_venta__sum'] or 0
    cantidad_pedidos = ventas.count()
    
    context = {
        'usuario': usuario,
        'ventas': ventas,
        'total_ventas': total_ventas,
        'cantidad_pedidos': cantidad_pedidos,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    return render(request, 'core/admin/reportes_ventas.html', context)
