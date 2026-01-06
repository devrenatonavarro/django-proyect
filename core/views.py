# -*- coding: utf-8 -*-
"""
Views - Punto de entrada principal
Importa todas las vistas desde los controllers organizados en la arquitectura MVC.

Estructura MVC:
- Models (core/models/): Lógica de datos y modelos de base de datos
- Controllers (core/controllers/): Lógica de negocio y procesamiento de requests
- Templates (core/templates/): Presentación y vistas HTML
"""

# Importar todas las vistas desde controllers
from .controllers import *
