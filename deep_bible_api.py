"""
Deep Bible Study API - FastAPI endpoints for the personal Bible study app

Endpoints:
- /api/daily-reading/today - Get today's complete reading
- /api/daily-reading/{day} - Get reading for a specific day
- /api/interconnections/{reference} - Get deep connections for any verse
- /api/twin/ask - Ask your AI Twin a question
- /api/twin/stats - Get your journey statistics
- /api/reading-plan/progress - Get reading plan progress
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date, datetime
import os

# Import our modules
try:
    from interconnection_engine import InterconnectionEngine, get_interconnections
    INTERCONNECTION_AVAILABLE = True
except ImportError:
    INTERCONNECTION_AVAILABLE = False

try:
    from ai_twin import get_twin
    AI_TWIN_AVAILABLE = True
except ImportError:
    AI_TWIN_AVAILABLE = False

try:
    from reading_plan import get_reading_plan, get_todays_reading, get_theme_for_date
    from reading_plan.daily_reading import DailyReadingGenerator
    READING_PLAN_AVAILABLE = True
except ImportError:
    READING_PLAN_AVAILABLE = False


# Create FastAPI app
app = FastAPI(
    title="Deep Bible Study API",
    description="Personal Bible study with deep interconnections, AI Twin, and yearly reading plan",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files directory
interface_dir = os.path.join(os.path.dirname(__file__), 'interface')


# Request/Response Models
class QuestionRequest(BaseModel):
    question: str
    context: Optional[Dict] = None


class QuestionResponse(BaseModel):
    analysis: Dict
    personal_response: str
    answer: Optional[str] = None
    key_verses: Optional[List[Dict]] = None
    church_fathers: Optional[List[Dict]] = None
    typology: Optional[Dict] = None
    confidence: Optional[str] = None
    related_interests: List[Dict]
    suggested_connections: List[str]


# Initialize services
_bible_data = None
_interconnection_engine = None
_twin = None
_reading_generator = None


def get_bible_data():
    """Load Bible data (lazy loading)"""
    global _bible_data
    if _bible_data is None:
        # Try to load from existing cache
        try:
            import pickle
            cache_path = os.path.join(os.path.dirname(__file__), 'bible_app_cache.pkl')
            if os.path.exists(cache_path):
                with open(cache_path, 'rb') as f:
                    data = pickle.load(f)
                    if 'versions' in data:
                        _bible_data = data['versions'].get('asv', {})
        except Exception:
            pass
        
        if _bible_data is None:
            _bible_data = {}
    
    return _bible_data


def get_engine():
    """Get interconnection engine (lazy loading)"""
    global _interconnection_engine
    if _interconnection_engine is None and INTERCONNECTION_AVAILABLE:
        _interconnection_engine = InterconnectionEngine(get_bible_data())
    return _interconnection_engine


def get_ai_twin():
    """Get AI Twin (lazy loading)"""
    global _twin
    if _twin is None and AI_TWIN_AVAILABLE:
        _twin = get_twin()
    return _twin


def get_daily_generator():
    """Get daily reading generator (lazy loading)"""
    global _reading_generator
    if _reading_generator is None and READING_PLAN_AVAILABLE:
        _reading_generator = DailyReadingGenerator(get_bible_data())
    return _reading_generator


# Routes

@app.get("/")
async def root():
    """Serve the main interface"""
    html_path = os.path.join(interface_dir, 'app.html')
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return {
        "message": "Deep Bible Study API",
        "docs": "/docs",
        "status": {
            "interconnection_engine": INTERCONNECTION_AVAILABLE,
            "ai_twin": AI_TWIN_AVAILABLE,
            "reading_plan": READING_PLAN_AVAILABLE
        }
    }


@app.get("/styles.css")
async def get_styles():
    """Serve CSS file"""
    css_path = os.path.join(interface_dir, 'styles.css')
    if os.path.exists(css_path):
        return FileResponse(css_path, media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS not found")


@app.get("/app.js")
async def get_js():
    """Serve JavaScript file"""
    js_path = os.path.join(interface_dir, 'app.js')
    if os.path.exists(js_path):
        return FileResponse(js_path, media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JavaScript not found")


@app.get("/api/status")
async def api_status():
    """Get API status"""
    return {
        "status": "healthy",
        "components": {
            "interconnection_engine": INTERCONNECTION_AVAILABLE,
            "ai_twin": AI_TWIN_AVAILABLE,
            "reading_plan": READING_PLAN_AVAILABLE
        }
    }


# Daily Reading Endpoints

@app.get("/api/daily-reading/today")
async def get_today_reading(client_date: Optional[str] = None):
    """Get today's complete reading with interconnections.
    Use client_date (YYYY-MM-DD) to use the user's local date instead of server date (fixes timezone)."""
    generator = get_daily_generator()
    
    if not generator:
        raise HTTPException(status_code=503, detail="Reading plan not available")
    
    # Use client's date when provided so "today" matches the user's timezone
    if client_date:
        try:
            d = datetime.strptime(client_date, "%Y-%m-%d").date()
            reading = generator.get_reading_for_date(d)
        except (ValueError, TypeError):
            reading = generator.get_todays_reading()
    else:
        reading = generator.get_todays_reading()
    
    if not reading:
        raise HTTPException(status_code=404, detail="No reading found for today")
    
    return format_reading_response(reading)


@app.get("/api/daily-reading/{day_number}")
async def get_day_reading(day_number: int):
    """Get reading for a specific day (1-365)"""
    if not 1 <= day_number <= 365:
        raise HTTPException(status_code=400, detail="Day must be between 1 and 365")
    
    generator = get_daily_generator()
    
    if not generator:
        raise HTTPException(status_code=503, detail="Reading plan not available")
    
    reading = generator.get_reading_for_day(day_number)
    
    if not reading:
        raise HTTPException(status_code=404, detail=f"No reading found for day {day_number}")
    
    return format_reading_response(reading)


def format_reading_response(reading):
    """Format a DailyReading into API response"""
    return {
        "date": reading.date.isoformat() if reading.date else None,
        "day_number": reading.day_number,
        "passages": reading.passages,
        "title": reading.title,
        "passage_text": reading.passage_text,
        "salvation_history_context": reading.salvation_history_context,
        "monthly_theme": {
            "name": reading.monthly_theme.name,
            "description": reading.monthly_theme.description,
            "reflection_questions": reading.monthly_theme.reflection_questions
        } if reading.monthly_theme else None,
        "backward_links": reading.backward_links,
        "forward_links": reading.forward_links,
        "typological": reading.typological,
        "connection_to_christ": reading.connection_to_christ,
        "church_fathers": reading.church_fathers,
        "key_verse": reading.key_verse,
        "patristic_summary": getattr(reading, "patristic_summary", None) or "",
        "reflection_questions": reading.reflection_questions,
        "progress_percentage": reading.progress_percentage,
        "current_period": reading.current_period
    }


# Interconnection Endpoints

@app.get("/api/interconnections/{reference}")
async def get_verse_interconnections(reference: str):
    """Get deep interconnections for any verse reference"""
    engine = get_engine()
    
    if not engine:
        raise HTTPException(status_code=503, detail="Interconnection engine not available")
    
    # Get verse text if available
    bible_data = get_bible_data()
    verse_text = bible_data.get(reference, "")
    
    result = engine.get_interconnections(reference, verse_text)
    
    return {
        "reference": result.reference,
        "text": result.text,
        "themes": result.themes,
        "backward_links": [
            {
                "reference": c.reference,
                "text": c.text,
                "explanation": c.explanation,
                "similarity": c.similarity,
                "church_fathers": getattr(c, 'church_fathers', None) or []
            }
            for c in result.backward_links
        ],
        "forward_links": [
            {
                "reference": c.reference,
                "text": c.text,
                "explanation": c.explanation,
                "similarity": c.similarity,
                "church_fathers": getattr(c, 'church_fathers', None) or []
            }
            for c in result.forward_links
        ],
        "typological": result.typological,
        "church_fathers": result.church_fathers,
        "historical_perspectives": result.historical_perspectives,
        "christ_connection": result.christ_connection
    }


@app.get("/api/moses-to-jesus/{reference}")
async def get_moses_jesus_connection(reference: str):
    """Get specific Moses-to-Jesus connections for a verse"""
    engine = get_engine()
    
    if not engine:
        raise HTTPException(status_code=503, detail="Interconnection engine not available")
    
    bible_data = get_bible_data()
    verse_text = bible_data.get(reference, "")
    
    return engine.get_moses_to_jesus_connection(reference, verse_text)


# AI Twin Endpoints

@app.post("/api/twin/ask", response_model=QuestionResponse)
async def ask_twin(request: QuestionRequest):
    """Ask your AI Twin a question and get an actual answer"""
    twin = get_ai_twin()
    
    if not twin:
        # Provide fallback response with basic answer attempt
        from ai_twin.answer_engine import AnswerEngine
        engine = AnswerEngine()
        answer_data = engine.answer_question(request.question, ["general"])
        
        return QuestionResponse(
            analysis={
                "question": request.question,
                "topics": ["general"],
                "is_struggle": False
            },
            personal_response=answer_data.get('answer', "I'm here to help you explore Scripture."),
            answer=answer_data.get('answer'),
            key_verses=answer_data.get('key_verses', []),
            church_fathers=answer_data.get('church_fathers', []),
            typology=answer_data.get('typology'),
            confidence=answer_data.get('confidence', 'low'),
            related_interests=[],
            suggested_connections=[]
        )
    
    result = twin.ask(request.question, request.context)
    
    return QuestionResponse(
        analysis=result.get("analysis", {}),
        personal_response=result.get("personal_response", ""),
        answer=result.get("answer"),
        key_verses=result.get("key_verses", []),
        church_fathers=result.get("church_fathers", []),
        typology=result.get("typology"),
        confidence=result.get("confidence"),
        related_interests=result.get("related_interests", []),
        suggested_connections=result.get("suggested_connections", [])
    )


@app.get("/api/twin/stats")
async def get_twin_stats():
    """Get your journey statistics from AI Twin"""
    twin = get_ai_twin()
    
    if not twin:
        return {
            "profile_summary": {
                "days_on_journey": 1,
                "verses_read": 0,
                "topics_explored": 0
            },
            "questions_asked": 0,
            "top_interests": [],
            "active_struggles": []
        }
    
    return twin.get_journey_stats()


@app.get("/api/twin/greeting")
async def get_twin_greeting():
    """Get personalized daily greeting from AI Twin"""
    twin = get_ai_twin()
    
    if not twin:
        return {"greeting": "Welcome to your Bible study journey!"}
    
    return {"greeting": twin.get_daily_greeting()}


@app.get("/api/twin/reflection")
async def get_weekly_reflection():
    """Get weekly reflection from AI Twin"""
    twin = get_ai_twin()
    
    if not twin:
        return {"message": "Weekly reflection not available yet."}
    
    return twin.get_weekly_reflection()


# Reading Plan Endpoints

@app.get("/api/reading-plan/progress")
async def get_reading_progress():
    """Get reading plan progress"""
    if not READING_PLAN_AVAILABLE:
        raise HTTPException(status_code=503, detail="Reading plan not available")
    
    plan = get_reading_plan()
    progress = plan.get_progress()
    
    # Add period information
    from reading_plan.chronological_plan import SALVATION_HISTORY_PERIODS
    
    periods = []
    current_day = progress['day_number']
    
    for period_id, period in SALVATION_HISTORY_PERIODS.items():
        start, end = period['days']
        status = 'pending'
        if current_day > end:
            status = 'completed'
        elif start <= current_day <= end:
            status = 'current'
        
        periods.append({
            'id': period_id,
            'name': period['name'],
            'description': period['description'],
            'days': period['days'],
            'status': status
        })
    
    return {
        **progress,
        'periods': periods
    }


@app.get("/api/reading-plan/theme")
async def get_current_theme():
    """Get the current month's theme"""
    if not READING_PLAN_AVAILABLE:
        raise HTTPException(status_code=503, detail="Reading plan not available")
    
    theme = get_theme_for_date()
    
    return {
        "month": theme.month,
        "name": theme.name,
        "description": theme.description,
        "key_concepts": theme.key_concepts,
        "reflection_questions": theme.reflection_questions,
        "key_verses": theme.key_verses
    }


# Typology and Church Fathers Endpoints

@app.get("/api/typology")
async def get_all_typology():
    """Get all typological connections"""
    import json
    typology_path = os.path.join(os.path.dirname(__file__), 'data', 'typology.json')
    
    try:
        with open(typology_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Typology database not found")


@app.get("/api/church-fathers")
async def get_all_church_fathers():
    """Get Church Fathers quotes database"""
    import json
    fathers_path = os.path.join(os.path.dirname(__file__), 'data', 'church_fathers_quotes.json')
    
    try:
        with open(fathers_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Church Fathers database not found")


@app.get("/api/church-fathers/{reference}")
async def get_church_fathers_for_verse(reference: str):
    """Get Church Fathers quotes for a specific verse"""
    import json
    fathers_path = os.path.join(os.path.dirname(__file__), 'data', 'church_fathers_quotes.json')
    
    try:
        with open(fathers_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        quotes = data.get('quotes_by_verse', {}).get(reference, [])
        return {"reference": reference, "quotes": quotes}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Church Fathers database not found")


# External reference data (Encyclopedia, Church Fathers HTM, Summa)
try:
    from external_data_loader import (
        get_article,
        list_entries,
        search_titles,
        get_availability,
        COLLECTIONS,
    )
    EXTERNAL_DATA_LOADER_AVAILABLE = True
except ImportError:
    EXTERNAL_DATA_LOADER_AVAILABLE = False


@app.get("/api/sources/availability")
async def external_sources_availability():
    """Report which external collections (cathen, fathers, summa, etc.) are available."""
    if not EXTERNAL_DATA_LOADER_AVAILABLE:
        return {"available": False, "collections": {}}
    return {"available": True, "collections": get_availability()}


@app.get("/api/sources/{collection}")
async def list_source_entries(collection: str, prefix: str = "", limit: int = 100):
    """List entries in a collection (cathen, fathers, summa, douay, library). Optional prefix filter."""
    if not EXTERNAL_DATA_LOADER_AVAILABLE or collection not in COLLECTIONS:
        raise HTTPException(status_code=404, detail="Collection not found or loader not available")
    entries = list_entries(collection, prefix=prefix, limit=min(limit, 200))
    return {"collection": collection, "entries": entries}


@app.get("/api/sources/{collection}/search")
async def search_source_titles(collection: str, q: str = "", limit: int = 30):
    """Search entries by title substring."""
    if not EXTERNAL_DATA_LOADER_AVAILABLE or collection not in COLLECTIONS:
        raise HTTPException(status_code=404, detail="Collection not found or loader not available")
    entries = search_titles(collection, q, limit=min(limit, 100))
    return {"collection": collection, "entries": entries}


@app.get("/api/sources/{collection}/article/{article_id}")
async def get_source_article(collection: str, article_id: str):
    """Get full article content by collection and filename (e.g. 00001a.htm)."""
    if not EXTERNAL_DATA_LOADER_AVAILABLE or collection not in COLLECTIONS:
        raise HTTPException(status_code=404, detail="Collection not found or loader not available")
    article = get_article(collection, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
