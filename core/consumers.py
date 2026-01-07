# -*- coding: utf-8 -*-
"""
WebSocket Consumer para actualizaciones de pedidos en tiempo real
"""
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import DenyConnection

logger = logging.getLogger(__name__)


class PedidoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Conectar al WebSocket"""
        try:
            self.cliente_id = self.scope['url_route']['kwargs']['cliente_id']
            self.room_group_name = f'pedidos_cliente_{self.cliente_id}'

            # Unirse al grupo del cliente
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"Cliente {self.cliente_id} conectado al WebSocket")
        except Exception as e:
            logger.error(f"Error al conectar WebSocket: {e}")
            raise DenyConnection("Error en la conexión")

    async def disconnect(self, close_code):
        """Desconectar del WebSocket"""
        try:
            # Salir del grupo
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"Cliente {self.cliente_id} desconectado del WebSocket")
        except Exception as e:
            logger.error(f"Error al desconectar WebSocket: {e}")

    async def receive(self, text_data):
        """Recibir mensaje del WebSocket"""
        pass

    async def pedido_actualizado(self, event):
        """Enviar actualización de pedido al WebSocket"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'pedido_actualizado',
                'pedido_id': event['pedido_id'],
                'estado': event['estado'],
                'codigo_unico': event['codigo_unico']
            }))
        except Exception as e:
            logger.error(f"Error al enviar actualización de pedido: {e}")


class VentasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Conectar al WebSocket para notificaciones de ventas"""
        try:
            self.usuario_id = self.scope['url_route']['kwargs']['usuario_id']
            self.room_group_name = f'ventas_usuario_{self.usuario_id}'

            # Unirse al grupo del usuario
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"Usuario {self.usuario_id} conectado al WebSocket de ventas")
        except Exception as e:
            logger.error(f"Error al conectar WebSocket de ventas: {e}")
            raise DenyConnection("Error en la conexión")

    async def disconnect(self, close_code):
        """Desconectar del WebSocket"""
        try:
            # Salir del grupo
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"Usuario {self.usuario_id} desconectado del WebSocket de ventas")
        except Exception as e:
            logger.error(f"Error al desconectar WebSocket de ventas: {e}")

    async def receive(self, text_data):
        """Recibir mensaje del WebSocket"""
        pass

    async def venta_realizada(self, event):
        """Enviar notificación de venta realizada"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'venta_realizada',
                'pedido_id': event['pedido_id'],
                'codigo_unico': event['codigo_unico'],
                'total': event['total'],
                'repartidor': event['repartidor']
            }))
        except Exception as e:
            logger.error(f"Error al enviar notificación de venta: {e}")
