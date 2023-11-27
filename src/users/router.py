from fastapi import APIRouter, Response, Depends

from src.exceptions import CannotAddDataToDatabase, UserAlreadyExistsException
from src.users.auth import (
    get_password_hash, authenticate_user, create_access_token
)
from src.users.dao import UserDAO
from src.users.dependencies import get_current_user
from src.users.models import Users
from src.users.schemas import SUserAuth


router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name,
        role=user_data.role
    )
    if not new_user:
        raise CannotAddDataToDatabase


@router_auth.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("manage_ticket_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("manage_ticket_access_token")


@router_users.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
