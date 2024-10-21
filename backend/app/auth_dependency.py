# here we create the dependencies for authorization including functions for
# creating refresh and access tokens, as well as verifying the tokens

import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from .models import User
from .database import get_db

load_dotenv()

ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"



# create token
def create_access_token(user_data: dict, expiration_time):
    to_encode = user_data.copy()
    
    if expiration_time:
        exp = datetime.now(timezone.utc) + timedelta(minutes=expiration_time)
    else:
        exp = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": exp})
    # encode the data
    access_token = jwt.encode(to_encode, ACCESS_SECRET_KEY, algorithm=ALGORITHM)

    return access_token


def create_refresh_token(user_data: dict, expiration_time):
    to_encode = user_data.copy()
    
    if expiration_time:
        exp = datetime.now(timezone.utc) + timedelta(days=expiration_time)
    else:
        exp = datetime.now(timezone.utc) + timedelta(days=3)

    to_encode.update({"exp": exp})
    # encode the data
    refresh_token = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return refresh_token


# function to get user credentials from the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    # Check if the user account is active
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User account is deactivated")
    
    return current_user
