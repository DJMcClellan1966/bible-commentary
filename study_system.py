"""
Bible Study System - Comprehensive study features
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from models import (
    StudyPlan, StudyPlanReading, StudyProgress, UserNote, Bookmark, Highlight,
    WordStudy, Theme, ThemeVerse, CrossReference, MemoryVerse, ReadingSession
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BibleStudySystem:
    """Comprehensive Bible study system"""

    def __init__(self, db: Session):
        self.db = db

    # Study Plans
    def create_study_plan(self, name: str, plan_type: str, description: str = None,
                         duration_days: int = None) -> StudyPlan:
        """Create a new study plan"""
        plan = StudyPlan(
            name=name,
            description=description,
            plan_type=plan_type,
            duration_days=duration_days,
            is_active=True
        )
        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)
        return plan

    def add_reading_to_plan(self, plan_id: int, day_number: int, book: str,
                           start_chapter: int, end_chapter: int,
                           start_verse: int = None, end_verse: int = None,
                           notes: str = None) -> StudyPlanReading:
        """Add a reading assignment to a study plan"""
        reading = StudyPlanReading(
            plan_id=plan_id,
            day_number=day_number,
            book=book,
            start_chapter=start_chapter,
            start_verse=start_verse,
            end_chapter=end_chapter,
            end_verse=end_verse,
            notes=notes
        )
        self.db.add(reading)
        self.db.commit()
        self.db.refresh(reading)
        return reading

    def get_today_reading(self, plan_id: int) -> Optional[Dict]:
        """Get today's reading assignment"""
        # Calculate day number (simplified - you might want to track start date)
        plan = self.db.query(StudyPlan).filter(StudyPlan.id == plan_id).first()
        if not plan:
            return None

        # For now, use a simple day calculation
        # In production, track actual start dates
        readings = self.db.query(StudyPlanReading).filter(
            StudyPlanReading.plan_id == plan_id
        ).order_by(StudyPlanReading.day_number).all()

        if not readings:
            return None

        # Simple: use day of year modulo plan duration
        day_of_year = datetime.now().timetuple().tm_yday
        day_number = (day_of_year % (plan.duration_days or 365)) + 1

        reading = self.db.query(StudyPlanReading).filter(
            and_(
                StudyPlanReading.plan_id == plan_id,
                StudyPlanReading.day_number == day_number
            )
        ).first()

        if reading:
            return {
                "day": day_number,
                "book": reading.book,
                "start_chapter": reading.start_chapter,
                "start_verse": reading.start_verse,
                "end_chapter": reading.end_chapter,
                "end_verse": reading.end_verse,
                "notes": reading.notes
            }
        return None

    def record_progress(self, plan_id: int, book: str, chapter: int,
                       verses_read: int, time_spent_minutes: int = 0,
                       completed: bool = False):
        """Record reading progress"""
        progress = StudyProgress(
            plan_id=plan_id,
            book=book,
            chapter=chapter,
            verses_read=verses_read,
            time_spent_minutes=time_spent_minutes,
            completed=completed
        )
        self.db.add(progress)
        self.db.commit()
        return progress

    # Notes
    def add_note(self, book: str, chapter: int, verse: int, note_text: str,
                 note_type: str = "general", tags: str = None) -> UserNote:
        """Add a user note to a verse"""
        note = UserNote(
            book=book,
            chapter=chapter,
            verse=verse,
            note_text=note_text,
            note_type=note_type,
            tags=tags
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def get_notes(self, book: str = None, chapter: int = None,
                 verse: int = None, note_type: str = None) -> List[UserNote]:
        """Get user notes"""
        query = self.db.query(UserNote)
        
        if book:
            query = query.filter(UserNote.book == book)
        if chapter:
            query = query.filter(UserNote.chapter == chapter)
        if verse:
            query = query.filter(UserNote.verse == verse)
        if note_type:
            query = query.filter(UserNote.note_type == note_type)
        
        return query.order_by(UserNote.created_at.desc()).all()

    # Bookmarks and Highlights
    def add_bookmark(self, book: str, chapter: int, verse: int,
                    label: str = None, color: str = "yellow") -> Bookmark:
        """Add a bookmark"""
        bookmark = Bookmark(
            book=book,
            chapter=chapter,
            verse=verse,
            label=label,
            color=color
        )
        self.db.add(bookmark)
        self.db.commit()
        self.db.refresh(bookmark)
        return bookmark

    def add_highlight(self, book: str, chapter: int, verse: int,
                     highlight_text: str = None, color: str = "yellow") -> Highlight:
        """Add a highlight"""
        highlight = Highlight(
            book=book,
            chapter=chapter,
            verse=verse,
            highlight_text=highlight_text,
            color=color
        )
        self.db.add(highlight)
        self.db.commit()
        self.db.refresh(highlight)
        return highlight

    def get_bookmarks(self) -> List[Bookmark]:
        """Get all bookmarks"""
        return self.db.query(Bookmark).order_by(Bookmark.created_at.desc()).all()

    def get_highlights(self, book: str = None) -> List[Highlight]:
        """Get highlights"""
        query = self.db.query(Highlight)
        if book:
            query = query.filter(Highlight.book == book)
        return query.order_by(Highlight.created_at.desc()).all()

    # Word Studies
    def create_word_study(self, word: str, original_language: str = None,
                         transliteration: str = None, definition: str = None) -> WordStudy:
        """Create or update a word study"""
        existing = self.db.query(WordStudy).filter(WordStudy.word == word).first()
        
        if existing:
            if definition:
                existing.definition = definition
            if transliteration:
                existing.transliteration = transliteration
            if original_language:
                existing.original_language = original_language
            existing.updated_at = datetime.utcnow()
            self.db.commit()
            return existing
        
        word_study = WordStudy(
            word=word,
            original_language=original_language,
            transliteration=transliteration,
            definition=definition
        )
        self.db.add(word_study)
        self.db.commit()
        self.db.refresh(word_study)
        return word_study

    def get_word_study(self, word: str) -> Optional[WordStudy]:
        """Get word study information"""
        return self.db.query(WordStudy).filter(WordStudy.word == word).first()

    # Themes
    def create_theme(self, name: str, description: str = None,
                    category: str = None) -> Theme:
        """Create a new theme"""
        theme = Theme(
            name=name,
            description=description,
            category=category
        )
        self.db.add(theme)
        self.db.commit()
        self.db.refresh(theme)
        return theme

    def add_verse_to_theme(self, theme_id: int, book: str, chapter: int,
                          verse: int, relevance_note: str = None) -> ThemeVerse:
        """Add a verse to a theme"""
        theme_verse = ThemeVerse(
            theme_id=theme_id,
            book=book,
            chapter=chapter,
            verse=verse,
            relevance_note=relevance_note
        )
        self.db.add(theme_verse)
        self.db.commit()
        self.db.refresh(theme_verse)
        return theme_verse

    def get_theme_verses(self, theme_id: int) -> List[ThemeVerse]:
        """Get all verses for a theme"""
        return self.db.query(ThemeVerse).filter(
            ThemeVerse.theme_id == theme_id
        ).order_by(ThemeVerse.order_index).all()

    def get_themes(self, category: str = None) -> List[Theme]:
        """Get all themes"""
        query = self.db.query(Theme)
        if category:
            query = query.filter(Theme.category == category)
        return query.all()

    # Cross References
    def add_cross_reference(self, source_book: str, source_chapter: int,
                           source_verse: int, target_book: str,
                           target_chapter: int, target_verse: int,
                           reference_type: str = "parallel",
                           strength: float = 1.0) -> CrossReference:
        """Add a cross reference"""
        cross_ref = CrossReference(
            source_book=source_book,
            source_chapter=source_chapter,
            source_verse=source_verse,
            target_book=target_book,
            target_chapter=target_chapter,
            target_verse=target_verse,
            reference_type=reference_type,
            strength=strength
        )
        self.db.add(cross_ref)
        self.db.commit()
        self.db.refresh(cross_ref)
        return cross_ref

    def get_cross_references(self, book: str, chapter: int,
                            verse: int) -> List[CrossReference]:
        """Get cross references for a verse"""
        return self.db.query(CrossReference).filter(
            and_(
                CrossReference.source_book == book,
                CrossReference.source_chapter == chapter,
                CrossReference.source_verse == verse
            )
        ).order_by(CrossReference.strength.desc()).all()

    # Memory Verses
    def add_memory_verse(self, book: str, chapter: int, verse: int,
                        verse_text: str = None, target_date: datetime = None) -> MemoryVerse:
        """Add a memory verse"""
        memory_verse = MemoryVerse(
            book=book,
            chapter=chapter,
            verse=verse,
            verse_text=verse_text,
            target_date=target_date
        )
        self.db.add(memory_verse)
        self.db.commit()
        self.db.refresh(memory_verse)
        return memory_verse

    def review_memory_verse(self, verse_id: int, memorized: bool = None):
        """Review a memory verse"""
        verse = self.db.query(MemoryVerse).filter(MemoryVerse.id == verse_id).first()
        if verse:
            verse.last_reviewed = datetime.utcnow()
            verse.review_count += 1
            if memorized is not None:
                verse.memorized = memorized
            self.db.commit()
        return verse

    def get_memory_verses(self, memorized: bool = None) -> List[MemoryVerse]:
        """Get memory verses"""
        query = self.db.query(MemoryVerse)
        if memorized is not None:
            query = query.filter(MemoryVerse.memorized == memorized)
        return query.order_by(MemoryVerse.created_at.desc()).all()

    def get_verses_to_review(self) -> List[MemoryVerse]:
        """Get memory verses that need review"""
        # Get verses that haven't been reviewed recently or aren't memorized
        return self.db.query(MemoryVerse).filter(
            or_(
                MemoryVerse.memorized == False,
                MemoryVerse.last_reviewed == None,
                MemoryVerse.last_reviewed < datetime.utcnow() - timedelta(days=7)
            )
        ).all()

    # Reading Sessions
    def record_reading_session(self, book: str, start_chapter: int,
                              end_chapter: int, verses_read: int,
                              time_spent_minutes: int = 0,
                              notes: str = None) -> ReadingSession:
        """Record a reading session"""
        session = ReadingSession(
            book=book,
            start_chapter=start_chapter,
            end_chapter=end_chapter,
            verses_read=verses_read,
            time_spent_minutes=time_spent_minutes,
            notes=notes
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_reading_statistics(self) -> Dict:
        """Get reading statistics"""
        total_sessions = self.db.query(func.count(ReadingSession.id)).scalar()
        total_verses = self.db.query(func.sum(ReadingSession.verses_read)).scalar() or 0
        total_time = self.db.query(func.sum(ReadingSession.time_spent_minutes)).scalar() or 0
        
        # Books read
        books_read = self.db.query(ReadingSession.book).distinct().count()
        
        return {
            "total_sessions": total_sessions,
            "total_verses_read": total_verses,
            "total_time_minutes": total_time,
            "books_read": books_read,
            "average_verses_per_session": total_verses / total_sessions if total_sessions > 0 else 0
        }
