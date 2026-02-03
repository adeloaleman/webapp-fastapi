import os
from dotenv import load_dotenv  # This line is used to load environment variables from a .env file. You can use os.getenv() directly — but without load_dotenv(), it will only read environment variables that are already set in the system environment or by your shell, not from a .env file.
from typing import Annotated    # Annotated is a generic type whose purpose is to add extra information to a type hint without changing the type itself. Ex. x: Annotated[int, "This is an integer with special meaning"]

from sqlalchemy.orm import Session
from .database import SessionLocal

from passlib.context import CryptContext  # CryptContext helps you: (1) Hash passwords, (2) Verify passwords, (3) Manage different hashing algorithms consistently (e.g. bcrypt, argon2, sha256, etc.)
from jose import jwt, JWTError  # JOSE (JSON Object Signing and Encryption) lets you encode, decode, and verify JSON Web Tokens (JWT)

from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  # OAuth 2.0 (Open Authorization) is a protocol for authorization, not authentication. It lets an application (like a web app or mobile app) access a user’s data from another service without needing the user’s password. A Bearer token is just one type of token used in OAuth2. "Bearer" means whoever holds the token (the bearer) is trusted to use it — no further proof is required.


load_dotenv()
AUTH_SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
AUTH_ALGORITHM = os.getenv('AUTH_ALGORITHM')


def get_db():
    db = SessionLocal()
    try:
        yield db  # The yield keyword turns the function into a generator — specifically, a context generator, It pauses the function at the yield statement and allows the caller to use the yielded value (db) within a managed context. So the function pauses at the yield statement and returns the value (db) to whatever called it.
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]  # Here we are defining a type alias (db_dependency). A type alias is a way to name a type hint (especially if it's long and used repeatedly), so you can reuse it cleanly. For ex., we could do: « Vector = List[float] » and the use the type « Vector: def normalize(v: Vector): ... »

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')  # Setting up a password hashing context

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')  # OAuth2PasswordBearer: (1) Tells FastAPI to expect a token in the Authorization header: « Authorization: Bearer <your-token>» (2) Extracts the token string from the request (3) Handles 401 errors automatically if no token is provided.
oauth2_bearer_dependency = Annotated[str, Depends(oauth2_bearer)]

async def get_current_user(token:oauth2_bearer_dependency):
    try:
        payload = jwt.decode(token=token, key=AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])  # In JWT (JSON Web Token) terminology, the "payload" is the part of the token that contains the data about the user. A JWT has three parts: header.payload.signature. So using payload matches common JWT documentation and examples
        id:int = payload.get('id')
        username:str = payload.get('username')  # 'sub' can also be userd instead of 'username'. 'sub' is the standard JWT claim for the subject
        name:str = payload.get('name')
        if id is None or username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        return {'id':id, 'username':username, 'name':name}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
user_dependency = Annotated[dict, Depends(get_current_user)] 




# In FastAPI, Depends() is a special function that marks something as a dependency — something FastAPI should automatically provide when the endpoint is called.
# So Depends(get_db) tells FastAPI to run get_db() to get the value for that parameter.
# For ex. If we do:
# @app.get("/items")
# def get_items(db: db_dependency):
# ...
# FastAPI needs to resolve all the parameters before calling your function get_items(...).
# So, FastAPI will:
# Detect that db depends on get_db() via Depends(get_db).
# Call get_db() to obtain a Session instance.
# Pass the resulting db session into your function as the argument.


# Password hashing is a one-way encryption technique. Password hashing is the process of turning a password (like "MySecret123") into a scrambled, irreversible string of characters using a mathematical algorithm.
# You can't turn it back into the original password. That's the whole point.
# Why is Hashing Important?
# Security: You don't store passwords directly in your database. That way, if someone hacks your system, they only see the hashes, not the actual passwords.
# Verification without revealing: When someone logs in, their input password is hashed, and you check if it matches the stored hash. You never need to know or store the original password.
# What happens if you just encrypt passwords?
# Encryption is reversible (you can decrypt it), which is dangerous if someone gets the key. Hashing is one-way — even the system storing the hash can't reverse it. Encryption is designed so that only authorized people can reverse it (i.e., decrypt it) using a secret key.
# bcrypt: Blowfish-crypt hashing (Blowfish is the encryption algorithm it's based on)


# A generator is a special type of function in Python that yields values one at a time, instead of returning everything at once. It's created using the yield keyword.

# Example:
# def read_lines(path):
#     with open(path) as f:
#         for line in f:
#             yield line.strip()

# Print each line
# for line in read_lines("data.txt"): print(line)

# Store all lines in a list
# lines = list(read_lines("data.txt"))

# Count number of lines
# line_count = sum(1 for _ in read_lines("data.txt"))

# This function yields one line at a time instead of returning all lines at once.

# Why is this useful?
# * It's memory-efficient: it doesn't load the whole file into memory.
# * It's reusable: the caller decides what to do with each line.
# * It's great for large files, log processing, streaming, etc.


# What is Context
# In Python, context usually refers to a situation where you want to:
# * set something up (like open a file, connect to a database, lock a thread),
# * do something safely with it, and then
# * automatically clean up afterward, even if an error occurs.

# This is handled using the with statement, which is Python's context management syntax.

# Example:
# with open("data.txt") as f:
#     content = f.read()

# Here's what's happening behind the scenes:
# * open() sets up a file object
# * with ensures it's automatically closed, even if read() crashes

# It's shorthand for:
# f = open("data.txt")
# try:
#     content = f.read()
# finally:
#     f.close()

# Context Manager
# Any object that can be used with a «with» statement is a context manager.
# It must implement:
# __enter__() — what happens at the start
# __exit__() — what happens at the end (like cleanup)
# import traceback
# class MyContext:
#     def __enter__(self):
#         print("Entering")
#         return self

#     def __exit__(self, exc_type, exc_val, exc_tb):
#         print("Exiting")
#         if exc_type:
#             print(f"An exception occurred: {exc_type.__name__} -- {exc_val}")
#             traceback.print_tb(exc_tb)
#         return True  # Suppresses the default exception msg because it's been alread printed

# with MyContext():
#     1 / 0  # Boom! ZeroDivisionError

# __enter__ and __exit__ are special methods that make a class a context manager — meaning you can use it with a with statement.

# These two methods define:
# * What to do before the with block starts → __enter__
# * What to do after the with block ends (even on error) → __exit__