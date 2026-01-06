# Mama Neme - Sistema de Gestión de Restaurante

Sistema completo de gestión de pedidos para restaurante con tracking en tiempo real usando Django y WebSocket.

## 🚀 Características

- ✅ Sistema de pedidos con código único
- ✅ Gestión de estados en tiempo real (WebSocket)
- ✅ Panel administrativo para diferentes roles
- ✅ Reportes de ventas automáticos
- ✅ Asignación de repartidores
- ✅ Timeline visual de seguimiento de pedidos
- ✅ Notificaciones push en navegador
- ✅ Optimización automática de imágenes a WebP
- ✅ Soft delete para mantener historial

## 📋 Requisitos

- Python 3.14+
- PostgreSQL 12+

## 🛠️ Instalación Local

1. Clonar el repositorio:
```bash
git clone <tu-repo>
cd django-restaurante
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

5. Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Crear datos iniciales (opcional):
```bash
python crear_usuarios.py
python crear_productos.py
```

7. Iniciar servidor:
```bash
python manage.py runserver
```

Acceder a: http://localhost:8000

## 🌐 Deployment en Render

### 1. Preparar el repositorio
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Crear base de datos PostgreSQL en Render
1. Ir a https://dashboard.render.com
2. New → PostgreSQL
3. Nombre: `mama-neme-db`
4. Copiar la `Internal Database URL`

### 3. Crear Web Service en Render
1. New → Web Service
2. Conectar tu repositorio de GitHub
3. Configuración:
   - **Name**: `mama-neme`
   - **Environment**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn restaurante.wsgi:application`

### 4. Variables de Entorno en Render
Agregar en "Environment Variables":

```
SECRET_KEY=genera-una-clave-secreta-fuerte-aqui
DEBUG=False
DATABASE_URL=[pegar Internal Database URL de PostgreSQL]
ALLOWED_HOSTS=mama-neme.onrender.com
```

**Generar SECRET_KEY segura:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Deploy
- Click en "Create Web Service"
- Render ejecutará automáticamente:
  - `build.sh` (instala dependencias, migraciones, collectstatic)
  - Iniciará con gunicorn

### 6. Configuración Post-Deploy
Ejecutar en Render Shell (Dashboard → Shell):
```bash
python crear_usuarios.py
python crear_productos.py
```

## 👥 Usuarios por Defecto

Después de ejecutar `crear_usuarios.py`:

- **Admin**: admin@restaurante.com / admin123
- **Cajero**: cajero@restaurante.com / cajero123
- **Cocina**: cocina@restaurante.com / cocina123
- **Repartidor**: repartidor@restaurante.com / repartidor123

## 📁 Estructura del Proyecto

```
django-restaurante/
├── core/
│   ├── models/          # Modelos de datos
│   ├── controllers/     # Lógica de negocio
│   ├── views/          # Templates HTML
│   ├── consumers.py    # WebSocket handlers
│   └── routing.py      # WebSocket routing
├── restaurante/
│   ├── settings.py     # Configuración
│   └── asgi.py        # ASGI config para WebSocket
├── media/             # Archivos subidos
├── staticfiles/       # Archivos estáticos compilados
├── requirements.txt   # Dependencias Python
├── build.sh          # Script de build para Render
└── Procfile          # Comando de inicio
```

## 🔧 Variables de Entorno

| Variable | Descripción | Requerida |
|----------|-------------|-----------|
| `SECRET_KEY` | Clave secreta de Django | ✅ |
| `DEBUG` | Modo debug (False en producción) | ✅ |
| `DATABASE_URL` | URL de PostgreSQL | ✅ |
| `ALLOWED_HOSTS` | Dominios permitidos | ✅ |

## 📝 Licencia

MIT

## 👨‍💻 Autor

Desarrollado con ❤️ para Mama Neme
