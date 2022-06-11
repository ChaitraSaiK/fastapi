from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class userInput(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class userOut(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    time_created: datetime

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
