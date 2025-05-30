import asyncio
from typing import Dict, Optional
from uuid import UUID

from fastapi import APIRouter
from loguru import logger

from starlette.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from src.core.auth_service import auth_service
from src.application.schemas.message import MessageSchema

active_connections: Dict[int, Dict[UUID, WebSocket]] = {}

ROUTER = APIRouter(prefix="/message")


async def notify_user(user_id: int, chat_uuid: UUID, message: MessageSchema):
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


@ROUTER.websocket("/ws/{chat_uuid}")
async def websocket_endpoint(websocket: WebSocket, chat_uuid: UUID, token: str):
    """
    WebSocket маршрут с проверкой Bearer токена в заголовках.
    """
    try:
        user_id: Optional[int] = auth_service.verify_token(token)
        if not user_id:
            await websocket.close(code=4001)
            return
    except Exception as e:
        logger.warning(f"Неверный токен: {e}")
        await websocket.close(code=4002)
        return

    await websocket.accept()

    if user_id not in active_connections:
        active_connections[user_id] = {}
    active_connections[user_id][chat_uuid] = websocket

    logger.info(f"Пользователь {user_id} подключился к чату {chat_uuid}")

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        if user_id in active_connections and chat_uuid in active_connections[user_id]:
            del active_connections[user_id][chat_uuid]
            if not active_connections[user_id]:
                del active_connections[user_id]
        logger.info(f"Пользователь {user_id} отключился от чата {chat_uuid}")
