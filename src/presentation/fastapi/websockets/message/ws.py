import asyncio
from typing import Dict
from uuid import UUID

from fastapi import APIRouter

from starlette.websockets import WebSocket, WebSocketDisconnect

from src.application.schemas.message import MessageSchema

active_connections: Dict[int, Dict[UUID, WebSocket]] = {}

ROUTER = APIRouter(prefix="/message")


async def notify_user(user_id: int, chat_uuid: UUID, message: MessageSchema):
    """Отправить сообщение пользователю, если он подключен."""
    if (user_id in active_connections) and (chat_uuid in active_connections[user_id]):
        websocket = active_connections[user_id][chat_uuid]
        await websocket.send_json(message.model_dump_json(by_alias=True))


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
