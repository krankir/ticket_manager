from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt

from src.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException, UserIsNotTicketInspectorException,
)
from src.users.dao import UserDAO

from src.config import SECRET_KEY, ALGORITHM
from src.users.models import Users, RoleEnum


def get_token(request: Request):
    token = request.cookies.get("manage_ticket_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, ALGORITHM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def get_ticket_inspector_user(current_user: Users = Depends(get_current_user)):
    if current_user.role != RoleEnum.TICKET_INSPECTOR:
        raise UserIsNotTicketInspectorException
    return current_user
