from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# create the pydantic model for a user (serializer)
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)  # Username between 3 and 50 characters
    email: EmailStr
    password: str = Field(...,min_length=8)


# Define a Pydantic model to control the response fields
class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True




# create the serializer
class TaskCreate(BaseModel):
    title: str = Field(..., max_length=50)
    description: str = Field(..., max_length=500)
    completed: bool
    time_created: datetime


# Define the Pydantic response model
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    time_created: datetime

    class Config:
        orm_mode = True


# Define the model for allowed edit/update fields
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=150)  # Optional title with a max length of 150
    description: Optional[str] = Field(None, max_length=500)  # Optional description, max length of 500
    completed: Optional[bool] = None  # Optional completed status

