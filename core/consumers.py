# -*- coding: utf-8 -*-
"""
WebSocket Consumer para actualizaciones de pedidos en tiempo real
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class PedidoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Conectar al WebSocket"""
        self.cliente_id = self.scope['url_route']['kwargs']['cliente_id']
        self.room_group_name = f'pedidos_cliente_{self.cliente_id}'

        # Unirse al grupo del cliente
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Desconectar del WebSocket"""
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recibir mensaje del WebSocket"""
        pass

    async def pedido_actualizado(self, event):
        """Enviar actualización de pedido al WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'pedido_actualizado',
            'pedido_id': event['pedido_id'],
            'estado': event['estado'],
            'codigo_unico': event['codigo_unico']
        }))


class VentasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Conectar al WebSocket para notificaciones de ventas"""
        self.usuario_id = self.scope['url_route']['kwargs']['usuario_id']
        self.room_group_name = f'ventas_usuario_{self.usuario_id}'

        # Unirse al grupo del usuario
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Desconectar del WebSocket"""
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recibir mensaje del WebSocket"""
        pass

    async def venta_realizada(self, event):
        """Enviar notificación de venta realizada"""
        await self.send(text_data=json.dumps({
            'type': 'venta_realizada',
            'pedido_id': event['pedido_id'],
            'codigo_unico': event['codigo_unico'],
            'total': event['total'],
            'repartidor': event['repartidor']
        }))
