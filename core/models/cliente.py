# -*- coding: utf-8 -*-
"""
Modelo: Cliente
Clientes que realizan pedidos en el restaurante.
"""
from django.db import models


class Cliente(models.Model):
    """
    Clientes que realizan pedidos en el restaurante.
    Se autentican con email y password.
    """
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre
