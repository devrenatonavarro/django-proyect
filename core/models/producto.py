# -*- coding: utf-8 -*-
"""
Modelo: Producto
Menú de productos disponibles en el restaurante.
"""
from django.db import models
from django.core.files.base import ContentFile
from django.utils import timezone
from PIL import Image
import uuid
import hashlib
import io
from .utils import producto_imagen_path


class Producto(models.Model):
    """
    Menú de productos disponibles en el restaurante.
    El campo 'activo' permite desactivar productos sin eliminarlos.
    El campo 'eliminado' permite soft delete (mantener histórico).
    Las imágenes se convierten automáticamente a WebP con nombres hash únicos.
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to=producto_imagen_path, blank=True, null=True)
    activo = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.nombre} - S/ {self.precio}"
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para convertir la imagen a WebP antes de guardar.
        """
        if self.imagen:
            # Abrir la imagen original
            img = Image.open(self.imagen)
            
            # Convertir a RGB si es necesario (para imágenes con transparencia)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Crear fondo blanco para imágenes con transparencia
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar si la imagen es muy grande (max 1200px en el lado más largo)
            max_size = 1200
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convertir a WebP y guardar en memoria
            output = io.BytesIO()
            img.save(output, format='WEBP', quality=85, optimize=True)
            output.seek(0)
            
            # Generar nombre único con hash
            unique_string = f"{timezone.now().timestamp()}{uuid.uuid4()}"
            hash_name = hashlib.md5(unique_string.encode()).hexdigest()
            
            # Reemplazar el archivo de imagen con la versión WebP
            self.imagen.save(
                f'{hash_name}.webp',
                ContentFile(output.read()),
                save=False
            )
        
        super().save(*args, **kwargs)
