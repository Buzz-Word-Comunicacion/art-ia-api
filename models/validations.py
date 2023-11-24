from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class User(BaseModel):
    idUser: int
    name: str
    username: str 
    email: str

class UserRegistration(BaseModel):
    name: str
    username: str
    email: str
    password: str

class UserRegistrationResponse(BaseModel):
    message: str
    user_data: User