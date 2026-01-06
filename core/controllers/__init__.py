# -*- coding: utf-8 -*-
"""
Controllers Package - MVC Architecture
Importa todos los controllers (views) para que Django los reconozca.
"""

from .cliente_controller import (
    index,
    ubicacion,
    registro,
    login,
    logout,
    agregar_al_carrito,
    ver_carrito,
    actualizar_cantidad_carrito,
    eliminar_del_carrito,
    finalizar_compra,
    mis_pedidos
)

from .admin_controller import (
    admin_login,
    admin_logout,
    admin_dashboard,
    admin_mis_entregas
)

from .pedido_controller import (
    admin_pedidos,
    admin_cambiar_estado_pedido,
    admin_asignar_repartidor,
    admin_eliminar_pedido,
    admin_reportes_ventas
)

from .producto_controller import (
    admin_productos,
    admin_crear_producto,
    admin_editar_producto,
    admin_eliminar_producto,
    admin_toggle_producto
)

from .usuario_controller import (
    admin_usuarios,
    admin_crear_usuario,
    admin_editar_usuario,
    admin_eliminar_usuario
)

__all__ = [
    # Cliente views
    'index',
    'ubicacion',
    'registro',
    'login',
    'logout',
    'agregar_al_carrito',
    'ver_carrito',
    'actualizar_cantidad_carrito',
    'eliminar_del_carrito',
    'finalizar_compra',
    'mis_pedidos',
    
    # Admin views
    'admin_login',
    'admin_logout',
    'admin_dashboard',
    'admin_mis_entregas',
    
    # Pedido views
    'admin_pedidos',
    'admin_cambiar_estado_pedido',
    'admin_asignar_repartidor',
    'admin_eliminar_pedido',
    'admin_reportes_ventas',
    
    # Producto views
    'admin_productos',
    'admin_crear_producto',
    'admin_editar_producto',
    'admin_eliminar_producto',
    'admin_toggle_producto',
    
    # Usuario views
    'admin_usuarios',
    'admin_crear_usuario',
    'admin_editar_usuario',
    'admin_eliminar_usuario',
]
