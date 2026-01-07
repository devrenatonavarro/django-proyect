# -*- coding: utf-8 -*-
"""
Script para crear la categoría por defecto "Todos" y asignar productos sin categoría
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

from core.models import Categoria, Producto


def crear_categoria_todos():
    """Crea la categoría 'Todos' si no existe y asigna productos sin categoría"""
    
    # Crear o obtener la categoría "Todos"
    categoria_todos, created = Categoria.objects.get_or_create(
        nombre='Todos',
        defaults={
            'descripcion': 'Categoría por defecto para todos los productos',
            'activo': True
        }
    )
    
    if created:
        print(f"✓ Categoría '{categoria_todos.nombre}' creada exitosamente")
    else:
        print(f"✓ Categoría '{categoria_todos.nombre}' ya existe")
    
    # Asignar todos los productos sin categoría a "Todos"
    productos_sin_categoria = Producto.objects.filter(categoria__isnull=True)
    count = productos_sin_categoria.count()
    
    if count > 0:
        productos_sin_categoria.update(categoria=categoria_todos)
        print(f"✓ {count} producto(s) asignado(s) a la categoría 'Todos'")
    else:
        print("✓ Todos los productos ya tienen una categoría asignada")
    
    return categoria_todos


if __name__ == '__main__':
    print("=" * 50)
    print("Configurando categoría por defecto...")
    print("=" * 50)
    categoria = crear_categoria_todos()
    print("=" * 50)
    print("Proceso completado exitosamente")
    print("=" * 50)
