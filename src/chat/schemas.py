import datetime

from pydantic import BaseModel


class MessagesModel(BaseModel):
    ticket_id: int
    sender: int
    message_text: str
    timestamp: datetime
