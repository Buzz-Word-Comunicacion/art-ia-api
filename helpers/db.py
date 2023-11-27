from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from contextlib import contextmanager
import json
import configparser

from models.models import Base, Users, hash_password, Statements
from models.validations import UserRegistration, UserRegistrationResponse, User, Questionnaire

config = configparser.ConfigParser()
config.read("config.ini")

# Database connection settings
connection_string = f'mysql+mysqlconnector://{config["database"]["username"]}:{config["database"]["password"]}@{config["database"]["host"]}/{config["database"]["database"]}'
engine = create_engine(
    connection_string, pool_pre_ping=True, pool_recycle=3600)

# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)


# Create tables and session
Base.metadata.create_all(engine)
# db_session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    db_session = sessionmaker(bind=engine)
    session = db_session()
    try:
        yield session
        # session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# Add default values to database
with session_scope() as session:
    is_users_empty = session.query(Users).count()
    if is_users_empty == 0:
        base_user = Users(
            name='Admin', email='user@example.com',
            username='admin', password=hash_password('admin'), role=1
        )
        session.add_all([base_user])
        session.commit()

## ###################### ##
## REGION USER OPERATIONS ##
## ###################### ##

# Search for a user in the database by username


def search_user(username):
    with session_scope() as session:
        user = session.query(Users).filter(
            Users.username == username).first()
        return user

# Search for a user no passwd in User validation schema


def search_user_schema(username):
    with session_scope() as session:
        user = session.query(Users).filter(
            Users.username == username).first()
        return User(
            idUser=user.idUser,
            name=user.name,
            username=user.username,
            email=user.email
        )

# Creare new user in the database


def new_user(user: UserRegistration):
    with session_scope() as session:
        new_user_data = Users(
            name=user.name, email=user.email, username=user.username,
            password=hash_password(user.password), role=2
        )
        session.add_all([new_user_data])
        session.commit()
        return UserRegistrationResponse(
            message="User created successfully",
            user_data=search_user_schema(user.username)
        )


## ##################### ##
## REGION GAME FUNCTIONS ##
## ##################### ##

# Save questions into table
def save_questions(questions: Questionnaire):
    # print(questions)
    with session_scope() as session:
        for question in questions['questions']:
            print(question)
            new_question = Statements(
                statement=question['statement'],
                answer1=question['answer1'],
                answer2=question['answer2'],
                answer3=question['answer3'],
                correct=question['correct'],
                category=question['category']
            )
            session.add_all([new_question])
        session.commit()
        return "Questions saved successfully"
