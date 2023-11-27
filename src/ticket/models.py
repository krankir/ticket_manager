import uuid
from enum import Enum as PythonEnum

from sqlalchemy import (
    Column, Integer, TIMESTAMP, ForeignKey, text, Enum, String
)

from src.database import Base


class StatusEnum(PythonEnum):

    OPENED = 'OPENED'
    PROGRESS = 'PROGRESS'
    CLOSED = 'CLOSED'


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))
    status = Column(Enum(StatusEnum), default=StatusEnum.OPENED)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=True)
    closed_at = Column(TIMESTAMP, nullable=True)
    uid_ticket = Column(String, default=lambda: str(uuid.uuid4()), unique=True)


class TicketRule(Base):
    __tablename__ = "ticket_rules"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    employee_id = Column(Integer, ForeignKey("employees.id"))