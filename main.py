from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.validations import Token, TokenData, User, UserRegistration, UserRegistrationResponse, Questionnaire, StatementInput
from helpers import validate_user_login, user_authentication, user_registration, generate_questions_openai

# Create FastAPI instance
app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    title="ART AI API",
    description="API to manage the backend of ART AI application",
    version="0.1.0",
)

## ############# ##
## PUBLIC ROUTES ##
## ############# ##

# Token route, returns JWT token, used for authentication


@app.post(
    "/token",
    response_model=Token,
    tags=["Obtain JWT token"],
    summary="Login route to get access token (JWT)"
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return validate_user_login(form_data.username, form_data.password)


## ################ ##
## PROTECTED ROUTES ##
## ################ ##


# Register new user (only available for admin users)
@app.post(
    "/users",
    tags=["Users ABC"],
    summary="Register new user",
    response_model=UserRegistrationResponse
)
async def register_user(user: UserRegistration, authenticate: TokenData = Depends(user_authentication)):
    # Check if user's role is admin, if not, throw exception
    if authenticate.role != 1:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to register new users",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await user_registration(user)


# Obtain N number of questions from OpenAI
@app.post(
    "/ai/questions",
    tags=["OpenAI API requests"],
    summary="Obtain N number of questions from OpenAI [financial statements]",
    response_model=Questionnaire
)
async def generate_questions(number: StatementInput, authenticate: TokenData = Depends(user_authentication)):
    return await generate_questions_openai(number)
