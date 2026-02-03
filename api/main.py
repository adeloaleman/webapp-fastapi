import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import auth


load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)  # All your SQLAlchemy model classes (e.g., User, Post) should inherit from Base. metadata is a container that holds all the schema (table and column) information for the models you've defined using Base. Then, create_all(bind=engine) tells SQLAlchemy to create all tables defined in Base.metadata, using the connection provided by engine. So, in short, this line inspect all models that inherit from Base and generate and execute CREATE TABLE SQL statements if the tables do not already exist.

app.add_middleware(  # In general, a middleware class is a component that sits between the client and your application logic. It processes the incoming request before it reaches your main application (routes/controllers),
    CORSMiddleware,  # CORSMiddleware is a middleware class that FastAPI uses to wrap your app and process incoming HTTP requests before they reach your routes. This define how to handle cross-origin requests (requests coming from a different origin, like http://localhost:3000 talking to http://localhost:8000). 
    allow_origins = [os.getenv('API_URL', 'http://localhost:3000')],  # if API_URL is None, it will be http://localhost:3000
    allow_credentials = True,  # Allows cookies, authorization headers, or TLS client certificates to be sent in cross-origin requests. Required if your frontend uses fetch(..., { credentials: 'include' }) to send auth tokens/cookies.
    allow_methods = ['*'],     # Allows all HTTP methods like GET, POST, PUT, DELETE, etc.
    allow_headers = ['*']      # Allows any headers in the request (e.g., custom headers like Authorization or X-CSRF-Token).
)

@app.get('/')  # In Web API's, and endpoint is a specific API route + method that handles a request. It's called like this because it’s the final destination of an HTTP request — the place where the API responds.
def health_check():
    return 'Health check complete'

app.include_router(auth.router)  # In FastAPI, a router is an instance of APIRouter, which lets you define routes (endpoints) 