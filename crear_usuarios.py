# Script para crear roles y usuarios del personal
from core.models import Rol, Usuario
from django.contrib.auth.hashers import make_password

# Crear roles
roles_data = ['Admin', 'Cajeros', 'Cocina', 'Repartidores', 'Encargados']

print("Creando roles...")
for rol_nombre in roles_data:
    rol, created = Rol.objects.get_or_create(nombre_rol=rol_nombre)
    if created:
        print(f"✓ Rol creado: {rol_nombre}")
    else:
        print(f"- Rol ya existe: {rol_nombre}")

# Crear usuarios de ejemplo
usuarios_data = [
    {
        'nombre': 'Admin Principal',
        'email': 'admin@restaurante.com',
        'password': 'admin123',
        'rol': 'Admin'
    },
    {
        'nombre': 'Carlos Cajero',
        'email': 'cajero@restaurante.com',
        'password': 'cajero123',
        'rol': 'Cajeros'
    },
    {
        'nombre': 'Chef Mario',
        'email': 'cocina@restaurante.com',
        'password': 'cocina123',
        'rol': 'Cocina'
    },
    {
        'nombre': 'Juan Repartidor',
        'email': 'repartidor1@restaurante.com',
        'password': 'repartidor123',
        'rol': 'Repartidores'
    },
    {
        'nombre': 'María Repartidor',
        'email': 'repartidor2@restaurante.com',
        'password': 'repartidor123',
        'rol': 'Repartidores'
    },
    {
        'nombre': 'Pedro Encargado',
        'email': 'encargado@restaurante.com',
        'password': 'encargado123',
        'rol': 'Encargados'
    },
]

print("\nCreando usuarios...")
for usuario_data in usuarios_data:
    rol = Rol.objects.get(nombre_rol=usuario_data['rol'])
    usuario, created = Usuario.objects.get_or_create(
        email=usuario_data['email'],
        defaults={
            'nombre': usuario_data['nombre'],
            'password': make_password(usuario_data['password']),
            'rol': rol
        }
    )
    if created:
        print(f"✓ Usuario creado: {usuario_data['nombre']} ({usuario_data['rol']}) - Email: {usuario_data['email']} - Pass: {usuario_data['password']}")
    else:
        print(f"- Usuario ya existe: {usuario_data['nombre']}")

print("\n=== CREDENCIALES DE ACCESO ===")
print("\nADMIN:")
print("Email: admin@restaurante.com")
print("Password: admin123")
print("\nCAJERO:")
print("Email: cajero@restaurante.com")
print("Password: cajero123")
print("\nCOCINA:")
print("Email: cocina@restaurante.com")
print("Password: cocina123")
print("\nREPARTIDOR:")
print("Email: repartidor1@restaurante.com")
print("Password: repartidor123")
print("\nENCARGADO:")
print("Email: encargado@restaurante.com")
print("Password: encargado123")
print("\nAccede al panel en: http://127.0.0.1:8000/admin/login/")
