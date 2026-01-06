# -*- coding: utf-8 -*-
"""
Modelos: Carrito y DetalleCarrito
Sistema de carrito de compras antes de realizar el pedido.
"""
from django.db import models
from django.utils import timezone
from .cliente import Cliente
from .producto import Producto


class Carrito(models.Model):
    """
    Carrito de compras de cada cliente.
    Relación: Un carrito -> Un cliente
    """
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='carritos')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'carrito'
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'

    def __str__(self):
        return f"Carrito de {self.cliente.nombre}"


class DetalleCarrito(models.Model):
    """
    Items individuales dentro del carrito.
    Relación: Muchos detalles -> Un carrito
    Relación: Muchos detalles -> Un producto
    ON DELETE CASCADE: Si se elimina el carrito o el producto, se eliminan todos sus detalles
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='en_carritos')
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'detalle_carrito'
        verbose_name = 'Detalle de Carrito'
        verbose_name_plural = 'Detalles de Carrito'
        unique_together = ['carrito', 'producto']

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"
