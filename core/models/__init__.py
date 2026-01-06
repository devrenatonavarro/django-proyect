# -*- coding: utf-8 -*-
"""
Models Package - MVC Architecture
Importa todos los modelos para que Django los reconozca.
"""

from .rol import Rol
from .usuario import Usuario
from .cliente import Cliente
from .producto import Producto
from .carrito import Carrito, DetalleCarrito
from .pedido import Pedido, DetallePedido

__all__ = [
    'Rol',
    'Usuario',
    'Cliente',
    'Producto',
    'Carrito',
    'DetalleCarrito',
    'Pedido',
    'DetallePedido',
]
