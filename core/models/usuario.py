# -*- coding: utf-8 -*-
"""
Modelo: Usuario (Personal del restaurante)
"""
from django.db import models
from .rol import Rol


class Usuario(models.Model):
    """
    Personal del restaurante. Cada usuario tiene un rol asignado.
    Relación: Muchos usuarios -> Un rol
    """
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name='usuarios')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} ({self.rol.nombre_rol})"
