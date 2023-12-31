from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, class_mapper
from sqlalchemy_utils import database_exists, create_database
from contextlib import contextmanager
import sqlalchemy as sa
import json
import configparser

from models.models import Base, Users, hash_password, Statements, UserRankResults
from models.validations import UserRegistration, UserRegistrationResponse, User, Questionnaire, QuestionnaireResults

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
                category=question['category'],
                lection=question['lection']
            )
            session.add_all([new_question])
        session.commit()
        return "Questions saved successfully"

# Get questions from table
def get_questions(num_of_questions):
    with session_scope() as session:
        questions = session.query(Statements).order_by(sa.func.random()).limit(num_of_questions).all()

        # Convert each SQLAlchemy object to a dictionary
        questions_dict_list = [question.as_dict() for question in questions]

        # Convert the list of dictionaries to JSON
        questions_json = json.dumps(questions_dict_list)


        return questions_json

# Save user rank into table
def save_user_rank(results: QuestionnaireResults):
    with session_scope() as session:
        new_user_rank = UserRankResults(
            userid=results['userid'],
            category=results['category'],
            total_questions=results['total_questions'],
            correct_answers=results['correct_answers'],
            incorrect_answers=results['incorrect_answers'],
            percentage_correct=results['percentage_correct']
        )
        session.add_all([new_user_rank])
        session.commit()
        return "User rank saved successfully"