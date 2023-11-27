from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from models.validations import UserRegistration

from .db import new_user

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to create a new user (non admin user)
def user_registration(user: UserRegistration = Depends(oauth2_scheme)):
    try:
        new_user_reg = new_user(user)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error creating new user: %s" % e.orig.msg
        )
    return new_user_reg