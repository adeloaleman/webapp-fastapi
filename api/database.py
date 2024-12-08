# SQLAlchemy is a Python SQL toolkit and ORM (Object-Relational Mapper)
from sqlalchemy import create_engine     # Create a connection to the database
from sqlalchemy.orm import sessionmaker  # A function for creating new SQLAlchemy session objects that handle database operations (like reading, writing, and querying data)
from sqlalchemy.ext.declarative import declarative_base  # Provides a base class for defining your database models (ORM classes)


SQL_ALCHEMY_DATABASE_URL = 'sqlite:///workout_app.db'
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()