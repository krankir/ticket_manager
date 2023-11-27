import datetime
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from telegram import Bot

from src.chat.dao import MessageDAO
from src.database import async_session_maker
from src.users.dao import UserDAO

telegram_bot_token = "Наш токен для бота"


def send_telegram_message(user_id, message):
    bot = Bot(token=telegram_bot_token)
    bot.send_message(chat_id=user_id, text=message)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

templates = Jinja2Templates(directory='src/templates')


# @router.get('')
# def get_chat_page(request: Request):
#     return templates.TemplateResponse('chat.html', {'request': request})


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await self.add_messages_to_database(message)
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def broadcast_bytes(self, data: bytes):
        for connection in self.active_connections:
            await connection.send_bytes(data)

    @staticmethod
    async def add_messages_to_database(message: str):
        python_dict = json.loads(message)
        async with async_session_maker() as session:
            sender = await UserDAO.find_one_or_none(id=python_dict['employee_id'])
            sender_name = sender['name']
            await MessageDAO.add(
                ticket_id=python_dict['ticket_id'],
                sender=sender_name,
                message_text=python_dict['text'],
                timestamp=datetime.datetime.utcnow()
            )


manager = ConnectionManager()


@router.websocket("/ws/{uid_ticket}")
async def websocket_endpoint(websocket: WebSocket, uid_ticket: str):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive()
            if 'bytes' in message:
                data = message.get("bytes")
                with open(f"received_file_.bin", "wb") as f:
                    f.write(data)
                await websocket.send_text(f"File received for Client #")
            elif 'text' in message:
                data = message.get("text")
                await manager.send_personal_message(data,
                                                    websocket)
                # user_id = message['text']['telergram_id']
                # text = message['text']['text']
                # send_telegram_message(user_id, text)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

