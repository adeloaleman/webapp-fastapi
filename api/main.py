import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware 
from .database import Base, engine
from .routers import auth


load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins = [os.getenv('APP_URL', 'http://localhost:3000')],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.get('/')
def health_check():
    return 'Health check complete'

app.include_router(auth.router) 