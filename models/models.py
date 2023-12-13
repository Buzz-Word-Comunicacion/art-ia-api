from sqlalchemy import Column, Integer, String, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

Base = declarative_base()

class Users(Base):
    __tablename__ = 'tb_users'

    idUser = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    email = Column(String(length=255))  
    username = Column(String(length=255), unique=True)
    password = Column(Text)
    active = Column(Boolean, default=True)
    role = Column(Integer)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

class Roles(Base):
    __tablename__ = 'tb_roles'

    idRole = Column(Integer, primary_key=True)
    name = Column(String(length=100))
    description = Column(String(length=255))


class Statements(Base):
    __tablename__ = 'tb_statements'

    idStatement = Column(Integer, primary_key=True)
    statement = Column(Text)
    answer1 = Column(Text)
    answer2 = Column(Text)
    answer3 = Column(Text)
    correct = Column(Integer)
    category = Column(String(length=255))
    lection = Column(Text)


class UserRankResults(Base):
    __tablename__ = 'tb_user_rank_results'

    idUserRankResult = Column(Integer, primary_key=True)
    userid = Column(Integer)
    category = Column(String(length=255))
    total_questions = Column(Integer)
    correct_answers = Column(Integer)
    incorrect_answers = Column(Integer)
    percentage_correct = Column(Float)