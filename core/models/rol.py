# -*- coding: utf-8 -*-
"""
Modelo: Rol
Define los diferentes roles que puede tener el personal del restaurante.
"""
from django.db import models


class Rol(models.Model):
    """
    Define los diferentes roles que puede tener el personal del restaurante.
    Ejemplos: Admin, Cajeros, Cocina, Repartidores, Encargados
    """
    nombre_rol = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.nombre_rol
