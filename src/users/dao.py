from src.dao.base import BaseDAO
from src.users.models import Users, Client


class UserDAO(BaseDAO):
    model = Users


class ClientDAO(BaseDAO):
    model = Client
