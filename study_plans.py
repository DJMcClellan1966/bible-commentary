"""
Pre-built study plans for Bible study
"""
from typing import List, Dict
from study_system import BibleStudySystem
from sqlalchemy.orm import Session
from config import BIBLE_BOOKS

def create_bible_in_year_plan(study: BibleStudySystem, db: Session) -> int:
    """Create a 'Bible in a Year' reading plan"""
    plan = study.create_study_plan(
        name="Bible in a Year",
        plan_type="reading",
        description="Read through the entire Bible in 365 days",
        duration_days=365
    )
    
    # Simplified plan - in production, use a proper Bible reading plan
    # This creates a basic plan reading one chapter per day
    day = 1
    for book in BIBLE_BOOKS:
        # Assume average of 20 chapters per book (simplified)
        for chapter in range(1, 21):  # Adjust based on actual chapter counts
            study.add_reading_to_plan(
                plan_id=plan.id,
                day_number=day,
                book=book,
                start_chapter=chapter,
                end_chapter=chapter
            )
            day += 1
            if day > 365:
                break
        if day > 365:
            break
    
    return plan.id


def create_psalms_proverbs_plan(study: BibleStudySystem, db: Session) -> int:
    """Create a Psalms and Proverbs reading plan (31 days)"""
    plan = study.create_study_plan(
        name="Psalms & Proverbs in a Month",
        plan_type="reading",
        description="Read through Psalms and Proverbs in 31 days",
        duration_days=31
    )
    
    # Psalms has 150 chapters, Proverbs has 31
    # Read 5 Psalms + 1 Proverb per day
    day = 1
    psalm_chapter = 1
    
    for day in range(1, 32):
        # Read 5 Psalms chapters
        readings = []
        for i in range(5):
            if psalm_chapter <= 150:
                readings.append((psalm_chapter, psalm_chapter))
                psalm_chapter += 1
        
        # Add Psalms readings
        for start, end in readings:
            study.add_reading_to_plan(
                plan_id=plan.id,
                day_number=day,
                book="Psalms",
                start_chapter=start,
                end_chapter=end
            )
        
        # Add one Proverb chapter
        if day <= 31:
            study.add_reading_to_plan(
                plan_id=plan.id,
                day_number=day,
                book="Proverbs",
                start_chapter=day,
                end_chapter=day
            )
    
    return plan.id


def create_new_testament_plan(study: BibleStudySystem, db: Session) -> int:
    """Create a New Testament in 90 days plan"""
    plan = study.create_study_plan(
        name="New Testament in 90 Days",
        plan_type="reading",
        description="Read through the New Testament in 90 days",
        duration_days=90
    )
    
    new_testament_books = [
        "Matthew", "Mark", "Luke", "John", "Acts",
        "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians",
        "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy",
        "2 Timothy", "Titus", "Philemon", "Hebrews", "James",
        "1 Peter", "2 Peter", "1 John", "2 John", "3 John",
        "Jude", "Revelation"
    ]
    
    # Simplified: distribute chapters across 90 days
    day = 1
    for book in new_testament_books:
        # Assume average chapters - adjust based on actual counts
        chapters_per_book = {
            "Matthew": 28, "Mark": 16, "Luke": 24, "John": 21, "Acts": 28,
            "Romans": 16, "1 Corinthians": 16, "2 Corinthians": 13, 
            "Galatians": 6, "Ephesians": 6, "Philippians": 4, "Colossians": 4,
            "1 Thessalonians": 5, "2 Thessalonians": 3, "1 Timothy": 6,
            "2 Timothy": 4, "Titus": 3, "Philemon": 1, "Hebrews": 13,
            "James": 5, "1 Peter": 5, "2 Peter": 3, "1 John": 5,
            "2 John": 1, "3 John": 1, "Jude": 1, "Revelation": 22
        }
        
        chapters = chapters_per_book.get(book, 10)
        chapters_per_day = max(1, chapters // 3)  # Rough distribution
        
        for chapter in range(1, chapters + 1):
            if day <= 90:
                study.add_reading_to_plan(
                    plan_id=plan.id,
                    day_number=day,
                    book=book,
                    start_chapter=chapter,
                    end_chapter=chapter
                )
                # Advance day every few chapters
                if chapter % chapters_per_day == 0:
                    day += 1
    
    return plan.id


def create_gospels_plan(study: BibleStudySystem, db: Session) -> int:
    """Create a 30-day Gospels study plan"""
    plan = study.create_study_plan(
        name="30 Days in the Gospels",
        plan_type="book_study",
        description="Deep study of the four Gospels over 30 days",
        duration_days=30
    )
    
    gospels = [
        ("Matthew", 28),
        ("Mark", 16),
        ("Luke", 24),
        ("John", 21)
    ]
    
    day = 1
    for book, chapters in gospels:
        chapters_per_day = max(1, chapters // 7)  # Roughly a week per Gospel
        for chapter in range(1, chapters + 1):
            if day <= 30:
                study.add_reading_to_plan(
                    plan_id=plan.id,
                    day_number=day,
                    book=book,
                    start_chapter=chapter,
                    end_chapter=chapter,
                    notes=f"Study {book} chapter {chapter}"
                )
                if chapter % chapters_per_day == 0:
                    day += 1
    
    return plan.id


def create_topical_plan(study: BibleStudySystem, db: Session, topic: str) -> int:
    """Create a topical study plan"""
    plan = study.create_study_plan(
        name=f"Study: {topic}",
        plan_type="topical",
        description=f"Topical study on {topic}",
        duration_days=30
    )
    
    # This would be populated with relevant verses based on the topic
    # For now, it's a template
    return plan.id


def initialize_default_plans(db: Session):
    """Initialize default study plans"""
    study = BibleStudySystem(db)
    
    plans_created = []
    
    try:
        # Check if plans already exist
        from models import StudyPlan
        existing = db.query(StudyPlan).filter(StudyPlan.name == "Bible in a Year").first()
        if not existing:
            plan_id = create_bible_in_year_plan(study, db)
            plans_created.append(plan_id)
            print(f"Created 'Bible in a Year' plan (ID: {plan_id})")
    except Exception as e:
        print(f"Error creating Bible in a Year plan: {e}")
    
    try:
        existing = db.query(StudyPlan).filter(StudyPlan.name == "Psalms & Proverbs in a Month").first()
        if not existing:
            plan_id = create_psalms_proverbs_plan(study, db)
            plans_created.append(plan_id)
            print(f"Created 'Psalms & Proverbs in a Month' plan (ID: {plan_id})")
    except Exception as e:
        print(f"Error creating Psalms & Proverbs plan: {e}")
    
    try:
        existing = db.query(StudyPlan).filter(StudyPlan.name == "New Testament in 90 Days").first()
        if not existing:
            plan_id = create_new_testament_plan(study, db)
            plans_created.append(plan_id)
            print(f"Created 'New Testament in 90 Days' plan (ID: {plan_id})")
    except Exception as e:
        print(f"Error creating New Testament plan: {e}")
    
    try:
        existing = db.query(StudyPlan).filter(StudyPlan.name == "30 Days in the Gospels").first()
        if not existing:
            plan_id = create_gospels_plan(study, db)
            plans_created.append(plan_id)
            print(f"Created '30 Days in the Gospels' plan (ID: {plan_id})")
    except Exception as e:
        print(f"Error creating Gospels plan: {e}")
    
    return plans_created
