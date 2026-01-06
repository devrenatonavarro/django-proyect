# -*- coding: utf-8 -*-
"""
WebSocket URL Configuration
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/pedidos/(?P<cliente_id>\w+)/$', consumers.PedidoConsumer.as_asgi()),
    re_path(r'ws/ventas/(?P<usuario_id>\w+)/$', consumers.VentasConsumer.as_asgi()),
]
