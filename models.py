"""
Database models for Bible commentaries
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
from config import DATABASE_URL

Base = declarative_base()


class SourceType(enum.Enum):
    CHURCH_FATHERS = "church_fathers"
    MIDDLE_AGES = "middle_ages"
    MODERN = "modern"
    JEWISH = "jewish"
    POPES = "popes"
    OTHER = "other"


class Commentary(Base):
    __tablename__ = "commentaries"

    id = Column(Integer, primary_key=True, index=True)
    book = Column(String(50), index=True, nullable=False)
    chapter = Column(Integer, index=True, nullable=False)
    verse = Column(Integer, index=True, nullable=False)
    commentary_text = Column(Text, nullable=False)
    source_type = Column(Enum(SourceType), index=True, nullable=False)
    source_name = Column(String(200), nullable=False)
    source_url = Column(String(500))
    author = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Commentary({self.book} {self.chapter}:{self.verse} - {self.source_type.value})>"


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String(500), nullable=False)
    book = Column(String(50))
    chapter = Column(Integer)
    verse = Column(Integer)
    results_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize the database with tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
