# -*- coding: utf-8 -*-
"""
Controllers: Categoria Views
Vistas para gestión de categorías del restaurante (Solo Admin).
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Usuario, Categoria, Producto


def admin_categorias(request):
    """Vista para gestionar categorías (solo Admin)"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin puede gestionar categorías
    if usuario.rol.nombre_rol != 'Admin':
        messages.error(request, 'Acceso denegado. Solo administradores pueden gestionar categorías.')
        return redirect('admin_dashboard')
    
    categorias = Categoria.objects.all().order_by('nombre')
    
    # Contar productos por categoría
    for categoria in categorias:
        categoria.total_productos = categoria.productos.filter(eliminado=False).count()
    
    context = {
        'usuario': usuario,
        'categorias': categorias,
    }
    
    return render(request, 'core/admin/categorias.html', context)


def admin_crear_categoria(request):
    """Vista para crear una nueva categoría (solo Admin)"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    if usuario.rol.nombre_rol != 'Admin':
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        
        # Validar que el nombre no exista
        if Categoria.objects.filter(nombre=nombre).exists():
            messages.error(request, f'Ya existe una categoría con el nombre "{nombre}"')
            return redirect('admin_categorias')
        
        categoria = Categoria.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            activo=True
        )
        
        messages.success(request, f'Categoría "{categoria.nombre}" creada exitosamente')
        return redirect('admin_categorias')
    
    return redirect('admin_categorias')


def admin_editar_categoria(request, categoria_id):
    """Vista para editar una categoría (solo Admin)"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    if usuario.rol.nombre_rol != 'Admin':
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        categoria = get_object_or_404(Categoria, id=categoria_id)
        
        nuevo_nombre = request.POST.get('nombre')
        
        # Validar que el nombre no exista en otra categoría
        if Categoria.objects.filter(nombre=nuevo_nombre).exclude(id=categoria_id).exists():
            messages.error(request, f'Ya existe una categoría con el nombre "{nuevo_nombre}"')
            return redirect('admin_categorias')
        
        categoria.nombre = nuevo_nombre
        categoria.descripcion = request.POST.get('descripcion', '')
        categoria.save()
        
        messages.success(request, f'Categoría "{categoria.nombre}" actualizada exitosamente')
        return redirect('admin_categorias')
    
    return redirect('admin_categorias')


def admin_eliminar_categoria(request, categoria_id):
    """Vista para eliminar una categoría (solo Admin)"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    if usuario.rol.nombre_rol != 'Admin':
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    # Verificar que no sea la categoría "Todos"
    if categoria.nombre == 'Todos':
        messages.error(request, 'No se puede eliminar la categoría "Todos"')
        return redirect('admin_categorias')
    
    # Verificar si tiene productos asociados
    productos_asociados = categoria.productos.filter(eliminado=False).count()
    
    if productos_asociados > 0:
        messages.error(request, f'No se puede eliminar la categoría "{categoria.nombre}" porque tiene {productos_asociados} producto(s) asociado(s). Reasigne los productos primero.')
        return redirect('admin_categorias')
    
    nombre_categoria = categoria.nombre
    categoria.delete()
    
    messages.success(request, f'Categoría "{nombre_categoria}" eliminada exitosamente')
    return redirect('admin_categorias')


def admin_toggle_categoria(request, categoria_id):
    """Vista para activar/desactivar una categoría (solo Admin)"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    if usuario.rol.nombre_rol != 'Admin':
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    # No permitir desactivar la categoría "Todos"
    if categoria.nombre == 'Todos' and categoria.activo:
        messages.error(request, 'No se puede desactivar la categoría "Todos"')
        return redirect('admin_categorias')
    
    categoria.activo = not categoria.activo
    categoria.save()
    
    estado = 'activada' if categoria.activo else 'desactivada'
    messages.success(request, f'Categoría "{categoria.nombre}" {estado} exitosamente')
    
    return redirect('admin_categorias')
