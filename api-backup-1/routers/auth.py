from datetime import datetime, timezone, timedelta
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from jose import jwt
from dotenv import load_dotenv
import os
from api.models import User
from api.deps import db_dependency, user_dependency, bcrypt_context
from fastapi import Form

load_dotenv()


router = APIRouter(
    prefix = '/auth',
    tags = ['auth']
)


SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
ALGORITHM = os.getenv('AUTH_ALGORITHM')


class EmailPasswordRequestForm:
    def __init__(
        self, 
        email:str = Form(...), 
        password:str = Form(...), 
        name:Optional[str] = Form(None)
    ):
        self.email = email
        self.password = password
        self.name = name


class UserCreateRequest(BaseModel):
    email:str
    password:str
    name:Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]


class Token(BaseModel):
    access_token:str
    token_type:str


def authenticate_user(email:str, password:str, db):
    user = db.query(User).filter(User.email==email).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(user_id:int, email:str, expires_delta:timedelta, name:str=None):
    encode = {'sub':email, 'id':user_id}  # The "sub" field in the JWT payload stands for "subject" according to the JWT standard. It is typically used to identify the principal (e.g., user, device, or application) that is the subject of the token.
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    if name: encode.update({"name": name})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency, create_user_request:UserCreateRequest):
    create_user_model = User(
        email = create_user_request.email,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        name=create_user_request.name
    )
    db.add(create_user_model)
    db.commit()


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data:Annotated[EmailPasswordRequestForm, Depends()], db:db_dependency):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    token = create_access_token(user.email, user.id, timedelta(minutes=20))
    return {'access_token':token, 'token_type':'bearer'}


@router.get("/me", response_model=UserResponse)
async def get_user_me(user: user_dependency):
    """
    Returns the currently authenticated user's information.
    """
    return {
        'id': user.get('id')
    }
    # return {
    #     "id": user["id"],
    #     "email": user["email"],
    #     "name": user.get("name", None)
    # }

