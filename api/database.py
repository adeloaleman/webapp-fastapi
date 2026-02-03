from sqlalchemy import create_engine     # # SQLAlchemy is a Python SQL toolkit and ORM (Object-Relational Mapper) - create_engine is a function to create a connection to the database
from sqlalchemy.orm import sessionmaker  # A class for creating new SQLAlchemy session objects that handle database operations (like reading, writing, and querying data)
from sqlalchemy.ext.declarative import declarative_base  # Provides a base class for defining your database models (ORM classes)


DATABASE_URL = 'sqlite:///workout_app.db'
engine = create_engine(url=DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base() 