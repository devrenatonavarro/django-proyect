# -*- coding: utf-8 -*-
"""
Modelo: Producto
Menú de productos disponibles en el restaurante.
"""
from django.db import models
from .categoria import Categoria


class Producto(models.Model):
    """
    Menú de productos disponibles en el restaurante.
    El campo 'activo' permite desactivar productos sin eliminarlos.
    El campo 'eliminado' permite soft delete (mantener histórico).
    Cada producto está obligatoriamente asignado a una categoría.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos', null=True, blank=True)
    activo = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.nombre} - S/ {self.precio}"
