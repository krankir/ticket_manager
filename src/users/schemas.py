from typing import Optional

from pydantic import BaseModel, EmailStr

from src.users.models import RoleEnum


class SUserAuth(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    role: RoleEnum = RoleEnum.WORKER
