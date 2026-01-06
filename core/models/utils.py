# -*- coding: utf-8 -*-
"""
Utilidades para los modelos
"""
from django.utils import timezone
import uuid
import hashlib


def producto_imagen_path(instance, filename):
    """
    Genera un nombre único para la imagen usando hash MD5.
    Convierte la imagen a formato WebP automáticamente.
    """
    # Generar hash único basado en timestamp y uuid
    unique_string = f"{timezone.now().timestamp()}{uuid.uuid4()}"
    hash_name = hashlib.md5(unique_string.encode()).hexdigest()
    
    # Retornar ruta con extensión .webp
    return f'productos/{hash_name}.webp'
