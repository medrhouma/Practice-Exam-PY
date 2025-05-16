

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, joinedload
from sqlalchemy import Column, Integer, String, ForeignKey, func
from typing import Optional

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:hama@localhost:5432/tp"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()