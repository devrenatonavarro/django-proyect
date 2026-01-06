# Script para crear datos de ejemplo
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante.settings')
django.setup()

from core.models import Producto

# Crear productos de ejemplo
productos = [
    {
        'nombre': 'Pizza Margherita',
        'descripcion': 'Deliciosa pizza con tomate, mozzarella fresca y albahaca',
        'precio': 12.99,
        'imagen_url': 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400',
        'activo': True
    },
    {
        'nombre': 'Hamburguesa Clásica',
        'descripcion': 'Jugosa hamburguesa de carne con lechuga, tomate y queso',
        'precio': 9.99,
        'imagen_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400',
        'activo': True
    },
    {
        'nombre': 'Pasta Carbonara',
        'descripcion': 'Pasta italiana con salsa carbonara cremosa y tocino',
        'precio': 11.50,
        'imagen_url': 'https://images.unsplash.com/photo-1612874742237-6526221588e3?w=400',
        'activo': True
    },
    {
        'nombre': 'Ensalada César',
        'descripcion': 'Fresca ensalada con pollo, crutones y aderezo césar',
        'precio': 8.99,
        'imagen_url': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400',
        'activo': True
    },
    {
        'nombre': 'Tacos al Pastor',
        'descripcion': 'Tradicionales tacos mexicanos con carne al pastor',
        'precio': 7.50,
        'imagen_url': 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400',
        'activo': True
    },
    {
        'nombre': 'Sushi Roll',
        'descripcion': 'Variedad de rolls de sushi fresco con salmón y atún',
        'precio': 15.99,
        'imagen_url': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400',
        'activo': True
    },
]

print("Creando productos...")
for prod_data in productos:
    producto, created = Producto.objects.get_or_create(
        nombre=prod_data['nombre'],
        defaults=prod_data
    )
    if created:
        print(f"✓ Creado: {producto.nombre}")
    else:
        print(f"- Ya existe: {producto.nombre}")

print(f"\nTotal de productos en la base de datos: {Producto.objects.count()}")
