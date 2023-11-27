from sqlalchemy import Column, Integer, String, Enum

from enum import Enum as PythonEnum

from src.database import Base


class RoleEnum(PythonEnum):

    TICKET_INSPECTOR = 'TICKET_INSPECTOR'
    WORKER = 'WORKER'


class Users(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.WORKER)

    def __str__(self):
        return f"Пользователь {self.email}"


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    telegram_id = Column(Integer, unique=True)
