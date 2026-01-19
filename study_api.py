"""
API endpoints for Bible Study System
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from models import get_db
from study_system import BibleStudySystem

router = APIRouter(prefix="/api/study", tags=["study"])


# Pydantic models
class StudyPlanCreate(BaseModel):
    name: str
    plan_type: str
    description: Optional[str] = None
    duration_days: Optional[int] = None


class ReadingAdd(BaseModel):
    day_number: int
    book: str
    start_chapter: int
    end_chapter: int
    start_verse: Optional[int] = None
    end_verse: Optional[int] = None
    notes: Optional[str] = None


class NoteCreate(BaseModel):
    book: str
    chapter: int
    verse: int
    note_text: str
    note_type: Optional[str] = "general"
    tags: Optional[str] = None


class BookmarkCreate(BaseModel):
    book: str
    chapter: int
    verse: int
    label: Optional[str] = None
    color: Optional[str] = "yellow"


class HighlightCreate(BaseModel):
    book: str
    chapter: int
    verse: int
    highlight_text: Optional[str] = None
    color: Optional[str] = "yellow"


class WordStudyCreate(BaseModel):
    word: str
    original_language: Optional[str] = None
    transliteration: Optional[str] = None
    definition: Optional[str] = None


class ThemeCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


class ThemeVerseAdd(BaseModel):
    book: str
    chapter: int
    verse: int
    relevance_note: Optional[str] = None


class MemoryVerseCreate(BaseModel):
    book: str
    chapter: int
    verse: int
    verse_text: Optional[str] = None
    target_date: Optional[datetime] = None


class ReadingSessionCreate(BaseModel):
    book: str
    start_chapter: int
    end_chapter: int
    verses_read: int
    time_spent_minutes: Optional[int] = 0
    notes: Optional[str] = None


# Study Plans
@router.post("/plans")
async def create_study_plan(plan: StudyPlanCreate, db: Session = Depends(get_db)):
    """Create a new study plan"""
    study = BibleStudySystem(db)
    result = study.create_study_plan(
        name=plan.name,
        plan_type=plan.plan_type,
        description=plan.description,
        duration_days=plan.duration_days
    )
    return {"id": result.id, "name": result.name, "plan_type": result.plan_type}


@router.get("/plans")
async def get_study_plans(active_only: bool = Query(True), db: Session = Depends(get_db)):
    """Get all study plans"""
    from models import StudyPlan
    query = db.query(StudyPlan)
    if active_only:
        query = query.filter(StudyPlan.is_active == True)
    plans = query.all()
    return [{"id": p.id, "name": p.name, "plan_type": p.plan_type, 
             "description": p.description, "duration_days": p.duration_days} for p in plans]


@router.post("/plans/{plan_id}/readings")
async def add_reading(plan_id: int, reading: ReadingAdd, db: Session = Depends(get_db)):
    """Add a reading to a study plan"""
    study = BibleStudySystem(db)
    result = study.add_reading_to_plan(
        plan_id=plan_id,
        day_number=reading.day_number,
        book=reading.book,
        start_chapter=reading.start_chapter,
        end_chapter=reading.end_chapter,
        start_verse=reading.start_verse,
        end_verse=reading.end_verse,
        notes=reading.notes
    )
    return {"id": result.id, "day_number": result.day_number, "book": result.book}


@router.get("/plans/{plan_id}/today")
async def get_today_reading(plan_id: int, db: Session = Depends(get_db)):
    """Get today's reading assignment"""
    study = BibleStudySystem(db)
    reading = study.get_today_reading(plan_id)
    if not reading:
        raise HTTPException(status_code=404, detail="No reading found for today")
    return reading


@router.post("/plans/{plan_id}/progress")
async def record_progress(plan_id: int, book: str, chapter: int, 
                         verses_read: int, time_spent_minutes: int = 0,
                         completed: bool = False, db: Session = Depends(get_db)):
    """Record reading progress"""
    study = BibleStudySystem(db)
    result = study.record_progress(plan_id, book, chapter, verses_read, 
                                   time_spent_minutes, completed)
    return {"id": result.id, "book": result.book, "chapter": result.chapter}


# Notes
@router.post("/notes")
async def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    """Add a note to a verse"""
    study = BibleStudySystem(db)
    result = study.add_note(
        book=note.book,
        chapter=note.chapter,
        verse=note.verse,
        note_text=note.note_text,
        note_type=note.note_type,
        tags=note.tags
    )
    return {"id": result.id, "book": result.book, "chapter": result.chapter, 
            "verse": result.verse}


@router.get("/notes")
async def get_notes(book: Optional[str] = None, chapter: Optional[int] = None,
                   verse: Optional[int] = None, note_type: Optional[str] = None,
                   db: Session = Depends(get_db)):
    """Get notes"""
    study = BibleStudySystem(db)
    notes = study.get_notes(book, chapter, verse, note_type)
    return [{"id": n.id, "book": n.book, "chapter": n.chapter, "verse": n.verse,
             "note_text": n.note_text, "note_type": n.note_type, "tags": n.tags,
             "created_at": n.created_at.isoformat()} for n in notes]


# Bookmarks and Highlights
@router.post("/bookmarks")
async def add_bookmark(bookmark: BookmarkCreate, db: Session = Depends(get_db)):
    """Add a bookmark"""
    study = BibleStudySystem(db)
    result = study.add_bookmark(
        book=bookmark.book,
        chapter=bookmark.chapter,
        verse=bookmark.verse,
        label=bookmark.label,
        color=bookmark.color
    )
    return {"id": result.id, "book": result.book, "chapter": result.chapter,
            "verse": result.verse}


@router.get("/bookmarks")
async def get_bookmarks(db: Session = Depends(get_db)):
    """Get all bookmarks"""
    study = BibleStudySystem(db)
    bookmarks = study.get_bookmarks()
    return [{"id": b.id, "book": b.book, "chapter": b.chapter, "verse": b.verse,
             "label": b.label, "color": b.color} for b in bookmarks]


@router.post("/highlights")
async def add_highlight(highlight: HighlightCreate, db: Session = Depends(get_db)):
    """Add a highlight"""
    study = BibleStudySystem(db)
    result = study.add_highlight(
        book=highlight.book,
        chapter=highlight.chapter,
        verse=highlight.verse,
        highlight_text=highlight.highlight_text,
        color=highlight.color
    )
    return {"id": result.id, "book": result.book, "chapter": result.chapter,
            "verse": result.verse}


@router.get("/highlights")
async def get_highlights(book: Optional[str] = None, db: Session = Depends(get_db)):
    """Get highlights"""
    study = BibleStudySystem(db)
    highlights = study.get_highlights(book)
    return [{"id": h.id, "book": h.book, "chapter": h.chapter, "verse": h.verse,
             "color": h.color} for h in highlights]


# Word Studies
@router.post("/word-studies")
async def create_word_study(word_study: WordStudyCreate, db: Session = Depends(get_db)):
    """Create or update a word study"""
    study = BibleStudySystem(db)
    result = study.create_word_study(
        word=word_study.word,
        original_language=word_study.original_language,
        transliteration=word_study.transliteration,
        definition=word_study.definition
    )
    return {"id": result.id, "word": result.word, "definition": result.definition}


@router.get("/word-studies/{word}")
async def get_word_study(word: str, db: Session = Depends(get_db)):
    """Get word study information"""
    study = BibleStudySystem(db)
    word_study = study.get_word_study(word)
    if not word_study:
        raise HTTPException(status_code=404, detail="Word study not found")
    return {"id": word_study.id, "word": word_study.word, 
            "original_language": word_study.original_language,
            "transliteration": word_study.transliteration,
            "definition": word_study.definition}


# Themes
@router.post("/themes")
async def create_theme(theme: ThemeCreate, db: Session = Depends(get_db)):
    """Create a theme"""
    study = BibleStudySystem(db)
    result = study.create_theme(
        name=theme.name,
        description=theme.description,
        category=theme.category
    )
    return {"id": result.id, "name": result.name, "category": result.category}


@router.get("/themes")
async def get_themes(category: Optional[str] = None, db: Session = Depends(get_db)):
    """Get themes"""
    study = BibleStudySystem(db)
    themes = study.get_themes(category)
    return [{"id": t.id, "name": t.name, "description": t.description,
             "category": t.category} for t in themes]


@router.post("/themes/{theme_id}/verses")
async def add_verse_to_theme(theme_id: int, verse: ThemeVerseAdd, 
                            db: Session = Depends(get_db)):
    """Add a verse to a theme"""
    study = BibleStudySystem(db)
    result = study.add_verse_to_theme(
        theme_id=theme_id,
        book=verse.book,
        chapter=verse.chapter,
        verse=verse.verse,
        relevance_note=verse.relevance_note
    )
    return {"id": result.id, "book": result.book, "chapter": result.chapter,
            "verse": result.verse}


@router.get("/themes/{theme_id}/verses")
async def get_theme_verses(theme_id: int, db: Session = Depends(get_db)):
    """Get verses for a theme"""
    study = BibleStudySystem(db)
    verses = study.get_theme_verses(theme_id)
    return [{"id": v.id, "book": v.book, "chapter": v.chapter, "verse": v.verse,
             "relevance_note": v.relevance_note} for v in verses]


# Cross References
@router.get("/cross-references")
async def get_cross_references(book: str, chapter: int, verse: int,
                              db: Session = Depends(get_db)):
    """Get cross references for a verse"""
    study = BibleStudySystem(db)
    refs = study.get_cross_references(book, chapter, verse)
    return [{"id": r.id, "target_book": r.target_book, 
             "target_chapter": r.target_chapter, "target_verse": r.target_verse,
             "reference_type": r.reference_type, "strength": r.strength} for r in refs]


# Memory Verses
@router.post("/memory-verses")
async def add_memory_verse(verse: MemoryVerseCreate, db: Session = Depends(get_db)):
    """Add a memory verse"""
    study = BibleStudySystem(db)
    result = study.add_memory_verse(
        book=verse.book,
        chapter=verse.chapter,
        verse=verse.verse,
        verse_text=verse.verse_text,
        target_date=verse.target_date
    )
    return {"id": result.id, "book": result.book, "chapter": result.chapter,
            "verse": result.verse}


@router.get("/memory-verses")
async def get_memory_verses(memorized: Optional[bool] = None,
                           db: Session = Depends(get_db)):
    """Get memory verses"""
    study = BibleStudySystem(db)
    verses = study.get_memory_verses(memorized)
    return [{"id": v.id, "book": v.book, "chapter": v.chapter, "verse": v.verse,
             "memorized": v.memorized, "last_reviewed": v.last_reviewed.isoformat() if v.last_reviewed else None,
             "review_count": v.review_count} for v in verses]


@router.post("/memory-verses/{verse_id}/review")
async def review_memory_verse(verse_id: int, memorized: bool,
                              db: Session = Depends(get_db)):
    """Review a memory verse"""
    study = BibleStudySystem(db)
    result = study.review_memory_verse(verse_id, memorized)
    if not result:
        raise HTTPException(status_code=404, detail="Memory verse not found")
    return {"id": result.id, "memorized": result.memorized, 
            "review_count": result.review_count}


@router.get("/memory-verses/to-review")
async def get_verses_to_review(db: Session = Depends(get_db)):
    """Get memory verses that need review"""
    study = BibleStudySystem(db)
    verses = study.get_verses_to_review()
    return [{"id": v.id, "book": v.book, "chapter": v.chapter, "verse": v.verse,
             "verse_text": v.verse_text} for v in verses]


# Reading Sessions and Statistics
@router.post("/reading-sessions")
async def record_reading_session(session: ReadingSessionCreate,
                                 db: Session = Depends(get_db)):
    """Record a reading session"""
    study = BibleStudySystem(db)
    result = study.record_reading_session(
        book=session.book,
        start_chapter=session.start_chapter,
        end_chapter=session.end_chapter,
        verses_read=session.verses_read,
        time_spent_minutes=session.time_spent_minutes,
        notes=session.notes
    )
    return {"id": result.id, "book": result.book, "verses_read": result.verses_read}


@router.get("/statistics")
async def get_statistics(db: Session = Depends(get_db)):
    """Get reading statistics"""
    study = BibleStudySystem(db)
    stats = study.get_reading_statistics()
    return stats
