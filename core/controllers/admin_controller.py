# -*- coding: utf-8 -*-
"""
Controllers: Admin Views
Vistas relacionadas con la gestión interna del restaurante.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Sum
from django.utils import timezone
from core.models import Usuario, Rol, Pedido, Producto
import os


def admin_login(request):
    """Vista de login para personal del restaurante"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            usuario = Usuario.objects.select_related('rol').get(email=email)
            if check_password(password, usuario.password):
                # Crear sesión de usuario staff
                request.session['usuario_id'] = usuario.id
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_rol'] = usuario.rol.nombre_rol
                messages.success(request, f'¡Bienvenido {usuario.nombre}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Credenciales incorrectas')
        except Usuario.DoesNotExist:
            messages.error(request, 'Credenciales incorrectas')
    
    return render(request, 'core/admin/login.html')


def admin_logout(request):
    """Vista para cerrar sesión del personal"""
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
        del request.session['usuario_nombre']
        del request.session['usuario_rol']
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('admin_login')


def admin_dashboard(request):
    """Dashboard principal para el personal"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Estadísticas generales
    total_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.filter(
        estado__in=['EN_PREPARACION', 'LISTO_ENTREGA', 'EN_RUTA']
    ).count()
    pedidos_hoy = Pedido.objects.filter(
        fecha_creacion__date=timezone.now().date()
    ).count()
    
    # Ventas totales
    ventas_totales = Pedido.objects.aggregate(
        total=Sum('total_venta')
    )['total'] or 0
    
    # Pedidos recientes
    pedidos_recientes = Pedido.objects.select_related('cliente', 'repartidor').order_by('-fecha_creacion')[:10]
    
    context = {
        'usuario': usuario,
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_hoy': pedidos_hoy,
        'ventas_totales': ventas_totales,
        'pedidos_recientes': pedidos_recientes,
    }
    
    return render(request, 'core/admin/dashboard.html', context)


def admin_mis_entregas(request):
    """Vista para repartidores: ver sus entregas asignadas"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo repartidores pueden ver esta página
    if usuario.rol.nombre_rol != 'Repartidores':
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    # Obtener filtro de ordenamiento
    ordenar = request.GET.get('ordenar', 'fecha')
    
    # Pedidos asignados al repartidor
    pedidos = Pedido.objects.filter(
        repartidor=usuario
    ).select_related('cliente').prefetch_related('detalles__producto')
    
    # Aplicar ordenamiento
    if ordenar == 'fecha':
        pedidos = pedidos.order_by('-fecha_creacion')
    elif ordenar == 'estado':
        # Priorizar EN_RUTA sobre LISTO_ENTREGA y ENTREGADO al final
        pedidos = pedidos.order_by('estado', '-fecha_creacion')
    elif ordenar == 'total':
        pedidos = pedidos.order_by('-total_venta')
    
    context = {
        'usuario': usuario,
        'pedidos': pedidos,
        'ordenar': ordenar,
    }
    
    return render(request, 'core/admin/mis_entregas.html', context)
