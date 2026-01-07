# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Categoria, Producto, Cliente, Usuario, Rol, Pedido, DetallePedido, Carrito, DetalleCarrito


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    ordering = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'activo', 'eliminado', 'fecha_creacion']
    list_filter = ['activo', 'eliminado', 'categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    ordering = ['-fecha_creacion']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'fecha_registro']
    search_fields = ['nombre', 'email', 'telefono']
    ordering = ['-fecha_registro']


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre_rol']
    search_fields = ['nombre_rol']


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'rol']
    list_filter = ['rol']
    search_fields = ['nombre', 'email']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['codigo_unico', 'cliente', 'total_venta', 'estado', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['codigo_unico', 'cliente__nombre', 'cliente__email']
    ordering = ['-fecha_creacion']


@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto_nombre', 'cantidad', 'precio_unitario', 'subtotal']
    search_fields = ['pedido__codigo_unico', 'producto_nombre']


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['cliente__nombre']


@admin.register(DetalleCarrito)
class DetalleCarritoAdmin(admin.ModelAdmin):
    list_display = ['carrito', 'producto', 'cantidad']
    search_fields = ['carrito__cliente__nombre', 'producto__nombre']
