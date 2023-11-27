from pydantic import BaseModel, conint, constr
from typing import Optional
from datetime import datetime, timedelta

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: int

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

class StatementInput(BaseModel):
    number_of_questions: conint(ge=1, le=10)

class Question(BaseModel):
    statement: constr(min_length=1)
    answer1: constr(min_length=1)
    answer2: constr(min_length=1)
    answer3: constr(min_length=1)
    correct: conint(ge=1, le=3)
    category: constr(min_length=1)

class Questionnaire(BaseModel):
    questions: list[Question]