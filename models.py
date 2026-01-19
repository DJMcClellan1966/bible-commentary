"""
Database models for Bible commentaries
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Enum, Boolean, Float, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
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


# Bible Study Models
class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    plan_type = Column(String(50), nullable=False)  # reading, topical, book_study, etc.
    duration_days = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    readings = relationship("StudyPlanReading", back_populates="plan", cascade="all, delete-orphan")
    progress = relationship("StudyProgress", back_populates="plan")


class StudyPlanReading(Base):
    __tablename__ = "study_plan_readings"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False)
    day_number = Column(Integer, nullable=False)
    book = Column(String(50), nullable=False)
    start_chapter = Column(Integer, nullable=False)
    start_verse = Column(Integer)
    end_chapter = Column(Integer, nullable=False)
    end_verse = Column(Integer)
    notes = Column(Text)
    order_index = Column(Integer, default=0)
    
    plan = relationship("StudyPlan", back_populates="readings")


class StudyProgress(Base):
    __tablename__ = "study_progress"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    book = Column(String(50), nullable=False)
    chapter = Column(Integer, nullable=False)
    verses_read = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    
    plan = relationship("StudyPlan", back_populates="progress")


class UserNote(Base):
    __tablename__ = "user_notes"

    id = Column(Integer, primary_key=True, index=True)
    book = Column(String(50), nullable=False, index=True)
    chapter = Column(Integer, nullable=False, index=True)
    verse = Column(Integer, nullable=False, index=True)
    note_text = Column(Text, nullable=False)
    note_type = Column(String(50), default="general")  # general, insight, question, prayer, etc.
    tags = Column(String(500))  # comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    book = Column(String(50), nullable=False, index=True)
    chapter = Column(Integer, nullable=False, index=True)
    verse = Column(Integer, nullable=False, index=True)
    label = Column(String(200))
    color = Column(String(20), default="yellow")  # yellow, blue, green, red, etc.
    created_at = Column(DateTime, default=datetime.utcnow)


class Highlight(Base):
    __tablename__ = "highlights"

    id = Column(Integer, primary_key=True, index=True)
    book = Column(String(50), nullable=False, index=True)
    chapter = Column(Integer, nullable=False, index=True)
    verse = Column(Integer, nullable=False, index=True)
    highlight_text = Column(Text)
    color = Column(String(20), default="yellow")
    created_at = Column(DateTime, default=datetime.utcnow)


class WordStudy(Base):
    __tablename__ = "word_studies"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False, index=True)
    original_language = Column(String(20))  # hebrew, greek, aramaic
    transliteration = Column(String(200))
    definition = Column(Text)
    usage_count = Column(Integer, default=0)
    verses = Column(JSON)  # List of verse references where word appears
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    category = Column(String(100))  # love, faith, salvation, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    verses = relationship("ThemeVerse", back_populates="theme", cascade="all, delete-orphan")


class ThemeVerse(Base):
    __tablename__ = "theme_verses"

    id = Column(Integer, primary_key=True, index=True)
    theme_id = Column(Integer, ForeignKey("themes.id"), nullable=False)
    book = Column(String(50), nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    relevance_note = Column(Text)
    order_index = Column(Integer, default=0)
    
    theme = relationship("Theme", back_populates="verses")


class CrossReference(Base):
    __tablename__ = "cross_references"

    id = Column(Integer, primary_key=True, index=True)
    source_book = Column(String(50), nullable=False, index=True)
    source_chapter = Column(Integer, nullable=False, index=True)
    source_verse = Column(Integer, nullable=False, index=True)
    target_book = Column(String(50), nullable=False, index=True)
    target_chapter = Column(Integer, nullable=False, index=True)
    target_verse = Column(Integer, nullable=False, index=True)
    reference_type = Column(String(50))  # parallel, quote, theme, etc.
    strength = Column(Float, default=1.0)  # 0.0 to 1.0
    created_at = Column(DateTime, default=datetime.utcnow)


class MemoryVerse(Base):
    __tablename__ = "memory_verses"

    id = Column(Integer, primary_key=True, index=True)
    book = Column(String(50), nullable=False, index=True)
    chapter = Column(Integer, nullable=False, index=True)
    verse = Column(Integer, nullable=False, index=True)
    verse_text = Column(Text)
    memorized = Column(Boolean, default=False)
    last_reviewed = Column(DateTime)
    review_count = Column(Integer, default=0)
    difficulty_level = Column(Integer, default=3)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    target_date = Column(DateTime)  # Target date for memorization


class ReadingSession(Base):
    __tablename__ = "reading_sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    book = Column(String(50), nullable=False)
    start_chapter = Column(Integer, nullable=False)
    end_chapter = Column(Integer, nullable=False)
    verses_read = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    notes = Column(Text)


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
