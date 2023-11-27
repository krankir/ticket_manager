from src.chat.models import Message
from src.dao.base import BaseDAO


class MessageDAO(BaseDAO):
    model = Message
