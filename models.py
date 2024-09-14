from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy as np
from typing import List

DATABASE_URL = "sqlite:///./test.db"  

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    vector_id = Column(Integer, index=True) 

class UserRequest(Base):
    __tablename__ = "user_request"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    request_count = Column(Integer, default=0)

def init_db():
    Base.metadata.create_all(bind=engine)

def encode_text(text: str) -> List[float]:
    
    return np.random.rand(128).tolist()  
