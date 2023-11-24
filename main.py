from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from models.validations import Token, TokenData, User, UserRegistration, UserRegistrationResponse
from helpers import validate_user_login, user_authentication, user_registration



app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
    title="Identity manager",
    description="API to manage user identifications and other stuff like faceID"
    )

## PUBLIC ROUTES ##

# Token route, returns JWT token, used for authentication
@app.post(
    "/token", 
    response_model=Token, 
    tags=["Obtain JWT token"], 
    summary="Login route to get access token (JWT)"
    )
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return validate_user_login(form_data.username, form_data.password)

## PROTECTED ROUTES ##

# Register new user (only available for admin users)
@app.post(
    "/users",
    tags=["Registration for new user"],
    summary="Register new user",
    response_model=UserRegistrationResponse
    )
async def register_user(user: UserRegistration, authenticate: TokenData = Depends(user_authentication)):
    return user_registration(user)

