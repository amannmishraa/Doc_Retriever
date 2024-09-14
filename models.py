from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DocumentMetadata(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    vector_id = Column(Integer)

def get_engine():
    return create_engine('sqlite:///documents.db', connect_args={"check_same_thread": False})

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
