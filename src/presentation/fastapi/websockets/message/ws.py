import asyncio
from typing import Dict, Optional
from uuid import UUID

from fastapi import APIRouter
from loguru import logger

from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState

from src.application.schemas.message import MessageSchema, MessageWithUsernameSchema

active_connections: Dict[int, Dict[UUID, WebSocket]] = {}

ROUTER = APIRouter(prefix="/message")


async def notify_user(user_id: int, chat_uuid: UUID, message: MessageWithUsernameSchema):
    """Отправить сообщение пользователю, если он подключен."""
    # Получаем соединение пользователя с чатом (если оно существует)
    user_connections = active_connections.get(user_id)
    if not user_connections:
        logger.debug(f"Пользователь {user_id} не найден в active_connections")
        return

    websocket: Optional[WebSocket] = user_connections.get(chat_uuid)
    if not websocket:
        logger.debug(f"Пользователь {user_id} не подключен к чату {chat_uuid}")
        return

    # Проверяем состояние соединения
    if websocket.client_state != WebSocketState.CONNECTED:
        logger.warning(f"Соединение с пользователем {user_id} в чате {chat_uuid} не активно")
        # Удаляем неактивное соединение
        del active_connections[user_id][chat_uuid]
        if not active_connections[user_id]:  # Удаляем пользователя, если нет соединений
            del active_connections[user_id]
        return

    try:
        # Отправляем сообщение
        await websocket.send_json(message.model_dump_json(by_alias=True))
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения пользователю {user_id} в чате {chat_uuid}: {e}", exc_info=True)
        # Удаляем соединение при ошибке
        del active_connections[user_id][chat_uuid]
        if not active_connections[user_id]:
            del active_connections[user_id]


@ROUTER.websocket("/ws/{user_id}/{chat_uuid}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, chat_uuid: UUID):
    await websocket.accept()
    if user_id not in active_connections:
        active_connections[user_id] = {}
    active_connections[user_id][chat_uuid] = websocket
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        active_connections[user_id].pop(chat_uuid, None)
