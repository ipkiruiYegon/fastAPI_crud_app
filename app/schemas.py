from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    firstname: str
    othernames: str
    


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    email: str
    is_active: bool
    last_login: str

    class Config:
        orm_mode = True