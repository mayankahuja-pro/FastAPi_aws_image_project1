# SQLAlchemy ke zaroori tools import kar rahe hain
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database ka path - local file mein data save hoga
DATABASE_URL = "sqlite:///./test.db"

# Database engine banao - ye actual connection establish karta hai
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite ke liye zaroor chahiye multithreading mein
)

# SessionLocal - har request ke liye naya DB session banane ka zariya
SessionLocal = sessionmaker(bind=engine)

# Base class - saare models isko inherit karenge
Base = declarative_base()