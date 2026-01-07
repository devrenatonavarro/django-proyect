# -*- coding: utf-8 -*-
"""
Modelo: Categoria
Categorías de productos del restaurante.
"""
from django.db import models


class Categoria(models.Model):
    """
    Categorías de productos disponibles en el restaurante.
    Cada producto debe estar asignado a una categoría obligatoriamente.
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
