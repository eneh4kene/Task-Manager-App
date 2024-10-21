# we implement the login route. Both access and refresh tokens will be issued on succesful login.
#  The login route accepts username and password from a formdata

import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import JWTError, jwt
from backend.app.auth_dependency import create_access_token, create_refresh_token
from backend.app.database import get_db
from backend.app.utils import verify_password
from backend.app.models import User
from backend.app.shemas import UserCreate, UserResponse
from backend.app.utils import hash_password



load_dotenv()

ACCESS_EXP_TIME = 30
REFRESH_EXP_TIME = 7
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# Define a model for the refresh token request body
class RefreshTokenRequest(BaseModel):
    refresh_token: str


router = APIRouter()


# For Browser form implentation: when the user types, it's always nice to validate the username's existence while they are typing it
# this is what the front end hits to check it while they are typing
@router.get("/check-availability")
def check_availability(username: str = None, email: str = None, db: Session = Depends(get_db)):
    if username:
        user = db.query(User).filter(User.username == username).first()
        if user:
            return {"available": False}
    if email:
        user = db.query(User).filter(User.email == email).first()
        if user:
            return {"available": False}
    
    return {"available": True}


# create the register route
@router.post('/register', response_model=UserResponse)
def create_user(user_data: UserCreate, db_connection: Session = Depends(get_db)):
    # check if the username or email already exists
    existing_user = db_connection.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        if existing_user.username == user_data.username:
            raise HTTPException(status_code=400, detail="Username already taken")

    hashed_pwd = hash_password(user_data.password)

    # create user based on model
    new_user_row = User(username = user_data.username, 
                    email = user_data.email,
                    hashed_password = hashed_pwd)
    
    # add the user to the db
    db_connection.add(new_user_row)
    db_connection.commit()
    db_connection.refresh(new_user_row)

    return new_user_row


# login route
@router.post("/login", response_model=TokenData)
def user_login(form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    username = form_data.username
    password = form_data.password

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Username or Password", headers={"WWW-Authenticate": "Bearer"})
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is deactivated")
    
    # create access token
    data = {"sub": str(user.id)}
    access_token = create_access_token(data, ACCESS_EXP_TIME)

    refresh_token = create_refresh_token(data, REFRESH_EXP_TIME)

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# refresh route
@router.post("/refresh", response_model=TokenData)
def get_new_access_token(ref_token: RefreshTokenRequest, db: Session=Depends(get_db)):
    credential_exception = HTTPException(status_code=401, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})

    try:
        payload = jwt.decode(ref_token.refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise credential_exception
        
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise credential_exception
        
            # create access token
        data = {"sub": str(user.id)}
        access_token = create_access_token(data, ACCESS_EXP_TIME)
        
        return {"access_token": access_token, "refresh_token": ref_token.refresh_token, "token_type": "bearer"}

    except JWTError:
        raise credential_exception
