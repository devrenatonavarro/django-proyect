# -*- coding: utf-8 -*-
"""
Modelos: Pedido y DetallePedido
Sistema de gestión de pedidos del restaurante.
"""
from django.db import models
from django.utils import timezone
import uuid
from .cliente import Cliente
from .usuario import Usuario
from .producto import Producto


class Pedido(models.Model):
    """
    Pedidos realizados por los clientes.
    - codigo_unico: Se genera automáticamente para identificar el pedido
    - repartidor_id: Permite NULL porque inicialmente no tiene repartidor asignado
    - estado: Sigue el flujo del pedido desde recepción hasta entrega
    
    Flujo de estados:
    1. RECIBIDO: Estado inicial cuando el cliente realiza el pedido
    2. EN_PREPARACION: El cocinero comienza a preparar el pedido
    3. LISTO_ENTREGA: El pedido está listo para ser entregado
    4. EN_CAMINO: El repartidor está en camino con el pedido
    5. ENTREGADO: El pedido fue entregado exitosamente
    6. NO_ENTREGADO: Hubo un problema y el pedido no pudo ser entregado
    
    Relaciones:
    - Un pedido -> Un cliente
    - Un pedido -> Un repartidor (opcional, puede ser NULL)
    """
    ESTADOS = [
        ('RECIBIDO', 'Recibido'),
        ('EN_PREPARACION', 'En preparación'),
        ('LISTO_ENTREGA', 'Listo para entrega'),
        ('EN_CAMINO', 'En camino'),
        ('ENTREGADO', 'Entregado'),
        ('NO_ENTREGADO', 'No entregado'),
    ]

    codigo_unico = models.CharField(max_length=50, unique=True, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    repartidor = models.ForeignKey(
        Usuario, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,     
        related_name='pedidos_asignados',
        limit_choices_to={'rol__nombre_rol': 'Repartidores'}
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='RECIBIDO')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']

    def save(self, *args, **kwargs):
        # Generar código único si no existe
        if not self.codigo_unico:
            self.codigo_unico = f"PED-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo_unico} - {self.cliente.nombre}"


class DetallePedido(models.Model):
    """
    Items de cada pedido con su histórico de precios.
    IMPORTANTE: Se guarda precio_unitario para mantener el precio al momento de la venta,
    ya que los precios en productos pueden cambiar con el tiempo.
    
    Relación: Muchos detalles -> Un pedido
    Relación: Muchos detalles -> Un producto (referencia histórica con SET_NULL)
    ON DELETE CASCADE: Si se elimina el pedido, se eliminan sus detalles
    ON DELETE SET_NULL: Si se elimina el producto, se mantiene el detalle pero sin referencia
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, related_name='en_pedidos')
    producto_nombre = models.CharField(max_length=100, help_text="Nombre del producto al momento de la venta")
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Precio del producto al momento de la venta"
    )

    class Meta:
        db_table = 'detalle_pedido'
        verbose_name = 'Detalle de Pedido'
        verbose_name_plural = 'Detalles de Pedido'

    def subtotal(self):
        """Calcula el subtotal de esta línea del pedido"""
        return self.cantidad * self.precio_unitario

    def __str__(self):
        nombre = self.producto.nombre if self.producto else self.producto_nombre
        return f"{self.cantidad}x {nombre} @ ${self.precio_unitario}"
