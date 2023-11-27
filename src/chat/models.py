from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP

from src.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    sender = Column(String)
    message_text = Column(String)
    timestamp = Column(TIMESTAMP)


