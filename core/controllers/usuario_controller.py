# -*- coding: utf-8 -*-
"""
Controllers: Usuario Views
Vistas para gestión de usuarios del personal.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from core.models import Usuario, Rol


def admin_usuarios(request):
    """Vista para gestionar usuarios del personal"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin y Encargados pueden gestionar usuarios
    if usuario.rol.nombre_rol not in ['Admin', 'Encargados']:
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    usuarios = Usuario.objects.select_related('rol').all().order_by('rol__nombre_rol', 'nombre')
    roles = Rol.objects.all()
    
    context = {
        'usuario': usuario,
        'usuarios': usuarios,
        'roles': roles,
    }
    
    return render(request, 'core/admin/usuarios.html', context)


def admin_crear_usuario(request):
    """Vista para crear un nuevo usuario del personal"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin y Encargados pueden crear usuarios
    if usuario.rol.nombre_rol not in ['Admin', 'Encargados']:
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol_id = request.POST.get('rol_id')
        
        # Validaciones
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está registrado')
            return redirect('admin_usuarios')
        
        rol = get_object_or_404(Rol, id=rol_id)
        
        # Crear usuario
        nuevo_usuario = Usuario.objects.create(
            nombre=nombre,
            email=email,
            password=make_password(password),
            rol=rol
        )
        
        messages.success(request, f'Usuario {nuevo_usuario.nombre} creado exitosamente')
        return redirect('admin_usuarios')
    
    return redirect('admin_usuarios')


def admin_editar_usuario(request, usuario_id):
    """Vista para editar un usuario del personal"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario_actual = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin y Encargados pueden editar usuarios
    if usuario_actual.rol.nombre_rol not in ['Admin', 'Encargados']:
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        usuario_editar = get_object_or_404(Usuario, id=usuario_id)
        
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        rol_id = request.POST.get('rol_id')
        password = request.POST.get('password')
        
        # Validar email único
        if Usuario.objects.filter(email=email).exclude(id=usuario_id).exists():
            messages.error(request, 'El email ya está en uso por otro usuario')
            return redirect('admin_usuarios')
        
        usuario_editar.nombre = nombre
        usuario_editar.email = email
        usuario_editar.rol = get_object_or_404(Rol, id=rol_id)
        
        # Solo cambiar password si se proporciona uno nuevo
        if password:
            usuario_editar.password = make_password(password)
        
        usuario_editar.save()
        
        messages.success(request, f'Usuario {usuario_editar.nombre} actualizado exitosamente')
        return redirect('admin_usuarios')
    
    return redirect('admin_usuarios')


def admin_eliminar_usuario(request, usuario_id):
    """Vista para eliminar un usuario del personal"""
    if 'usuario_id' not in request.session:
        return redirect('admin_login')
    
    usuario_actual = Usuario.objects.select_related('rol').get(id=request.session['usuario_id'])
    
    # Solo Admin puede eliminar usuarios
    if usuario_actual.rol.nombre_rol != 'Admin':
        messages.error(request, 'Acceso denegado')
        return redirect('admin_dashboard')
    
    # No puede eliminarse a sí mismo
    if usuario_actual.id == usuario_id:
        messages.error(request, 'No puedes eliminar tu propio usuario')
        return redirect('admin_usuarios')
    
    usuario_eliminar = get_object_or_404(Usuario, id=usuario_id)
    nombre = usuario_eliminar.nombre
    usuario_eliminar.delete()
    
    messages.success(request, f'Usuario {nombre} eliminado exitosamente')
    return redirect('admin_usuarios')
