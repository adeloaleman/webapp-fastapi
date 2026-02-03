import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from typing import Annotated, Optional
from pydantic import BaseModel
from jose import jwt, JWTError
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from api.models import User
from api.deps import db_dependency, user_dependency, bcrypt_context


load_dotenv()
AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
AUTH_ALGORITHM = os.getenv('AUTH_ALGORITHM')


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)


class UserResponse(BaseModel):
    id:int
    username:str
    name:Optional[str]

class RegisterUserRequest(BaseModel):
    username:str
    name:str
    password:str

class AccessToken(BaseModel):
    access_token:str
    token_type:str


def authenticate_user(db:db_dependency, username:str, password:str):
    user:User = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(id:str, username:str, name:str, expires_delta:timedelta):
    encode = {'id':id, 'username':username, 'name':name}
    expires = datetime.now(tz=timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, key=AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)

@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(db:db_dependency, register_user_request:RegisterUserRequest):
    db.add(User(
        username = register_user_request.username,
        name = register_user_request.name,
        hashed_password = bcrypt_context.hash(register_user_request.password)
    ))
    db.commit()

@router.post('/token', response_model=AccessToken)
async def login_for_access_token(db:db_dependency, form_data:Annotated[OAuth2PasswordRequestForm, Depends()]):
    user:User = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    return {
        'access_token': create_access_token(id=user.id, username=user.username, name=user.name, expires_delta=timedelta(minutes=20)), 
        'token_type': 'bearer'
    }

@router.get('/me', response_model=UserResponse)
async def get_user_me(user:user_dependency):
    return {'id':user['id'], 'username':user['username'], 'name':user.get('name', None)}