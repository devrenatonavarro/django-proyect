# -*- coding: utf-8 -*-
"""
Controllers: Producto Views
Vistas para gestión de productos del restaurante.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Usuario, Categoria, Producto


def admin_productos(request):
    """Vista para gestionar productos"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin y Encargados pueden gestionar productos
    if usuario.rol.nombre_rol not in ['Admin', 'Encargados']:
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    productos = Producto.objects.filter(eliminado=False).select_related('categoria').order_by('-fecha_creacion')
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    
    context = {
        'usuario': usuario,
        'productos': productos,
        'categorias': categorias,
    }
    
    return render(request, 'core/admin/productos.html', context)


def admin_crear_producto(request):
    """Vista para crear un nuevo producto"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    if usuario.rol.nombre_rol not in ['Admin', 'Encargados']:
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        imagen = request.FILES.get('imagen')
        categoria_id = request.POST.get('categoria')
        
        # Si no se proporciona categoría, asignar a "Todos"
        if not categoria_id:
            categoria_todos = Categoria.objects.get_or_create(
                nombre='Todos',
                defaults={'descripcion': 'Categoría por defecto', 'activo': True}
            )[0]
            categoria_id = categoria_todos.id
        
        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            imagen=imagen,
            categoria_id=categoria_id,
            activo=True
        )
        
        messages.success(request, f'Producto {producto.nombre} creado exitosamente')
        return redirect('admin_productos')
    
    return redirect('admin_productos')


def admin_editar_producto(request, producto_id):
    """Vista para editar un producto"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    if usuario.rol.nombre_rol not in ['Admin', 'Encargados']:
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        producto = get_object_or_404(Producto, id=producto_id)
        
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        
        # Actualizar categoría
        categoria_id = request.POST.get('categoria')
        if categoria_id:
            producto.categoria_id = categoria_id
        
        # Solo actualizar imagen si se sube una nueva
        if 'imagen' in request.FILES:
            # Cloudinary maneja automáticamente la eliminación de archivos antiguos
            producto.imagen = request.FILES['imagen']
        
        producto.save()
        
        messages.success(request, f'Producto {producto.nombre} actualizado exitosamente')
        return redirect('admin_productos')
    
    return redirect('admin_productos')


def admin_eliminar_producto(request, producto_id):
    """Vista para eliminar un producto (soft delete)"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    if usuario.rol.nombre_rol not in ['Admin', 'Encargados']:
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    producto = get_object_or_404(Producto, id=producto_id)
    nombre = producto.nombre
    
    # Soft delete: marcar como eliminado en lugar de borrar
    producto.eliminado = True
    producto.activo = False
    producto.save()
    
    messages.success(request, f'Producto {nombre} eliminado exitosamente')
    return redirect('admin_productos')


def admin_toggle_producto(request, producto_id):
    """Vista para activar/desactivar un producto"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = not producto.activo
    producto.save()
    
    estado = 'activado' if producto.activo else 'desactivado'
    messages.success(request, f'Producto {producto.nombre} {estado}')
    
    return redirect('admin_productos')
