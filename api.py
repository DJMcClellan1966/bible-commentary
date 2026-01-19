"""
FastAPI application for Bible Commentary Agent
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
from agent import BibleCommentaryAgent
from models import get_db, init_db, SearchHistory
from datetime import datetime
import os

# Import study system
from study_api import router as study_router

# Import quantum study system
try:
    from quantum_study_api import router as quantum_study_router
    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False
    quantum_study_router = None

# Import Bible characters
try:
    from bible_characters_api import router as bible_characters_router
    BIBLE_CHARACTERS_AVAILABLE = True
except ImportError:
    BIBLE_CHARACTERS_AVAILABLE = False
    bible_characters_router = None

# Import quantum AI system
try:
    from quantum_ai_api import router as quantum_ai_router
    QUANTUM_AI_AVAILABLE = True
except ImportError:
    QUANTUM_AI_AVAILABLE = False
    quantum_ai_router = None

# Import kernel-based Bible study
try:
    from bible_app_kernel_api import router as kernel_bible_study_router
    KERNEL_BIBLE_STUDY_AVAILABLE = True
except ImportError:
    KERNEL_BIBLE_STUDY_AVAILABLE = False
    kernel_bible_study_router = None

# Import Bible AI system
try:
    from bible_ai_api import router as bible_ai_router
    BIBLE_AI_AVAILABLE = True
except ImportError:
    BIBLE_AI_AVAILABLE = False
    bible_ai_router = None

app = FastAPI(
    title="Bible Commentary Agent API",
    description="AI-powered agent for building comprehensive Bible commentaries",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent
agent = BibleCommentaryAgent()

# Initialize database
init_db()

# Include study router
app.include_router(study_router)

# Include quantum study router if available
if QUANTUM_AVAILABLE and quantum_study_router:
    app.include_router(quantum_study_router)

# Include Bible characters router if available
if BIBLE_CHARACTERS_AVAILABLE and bible_characters_router:
    app.include_router(bible_characters_router)

# Include quantum AI router if available
if QUANTUM_AI_AVAILABLE and quantum_ai_router:
    app.include_router(quantum_ai_router)

# Include kernel-based Bible study router if available
if KERNEL_BIBLE_STUDY_AVAILABLE and kernel_bible_study_router:
    app.include_router(kernel_bible_study_router)

# Include Bible AI router if available
if BIBLE_AI_AVAILABLE and bible_ai_router:
    app.include_router(bible_ai_router)


# Pydantic models
class CommentaryRequest(BaseModel):
    book: str
    chapter: int
    verse: int
    source_types: Optional[List[str]] = None
    synthesize: bool = True


class CommentaryResponse(BaseModel):
    book: str
    chapter: int
    verse: int
    commentaries: List[dict]
    synthesized: Optional[str] = None


class SearchRequest(BaseModel):
    query: str
    book: Optional[str] = None
    chapter: Optional[int] = None
    verse: Optional[int] = None
    source_types: Optional[List[str]] = None


@app.get("/")
async def root():
    """Root endpoint - serves web interface if available"""
    if os.path.exists("web_interface.html"):
        return FileResponse("web_interface.html")
    return {
        "message": "Bible Commentary Agent API",
        "version": "1.0.0",
        "endpoints": {
            "web_interface": "/web",
            "build_commentary": "/api/commentary",
            "search": "/api/search",
            "get_by_category": "/api/commentary/{book}/{chapter}/{verse}/{category}",
            "suggestions": "/api/suggestions/{book}/{chapter}/{verse}"
        }
    }

@app.get("/web")
async def web_interface():
    """Serve web interface"""
    if os.path.exists("web_interface.html"):
        return FileResponse("web_interface.html")
    raise HTTPException(status_code=404, detail="Web interface not found")

@app.get("/study")
async def bible_study_interface():
    """Serve Bible study interface"""
    if os.path.exists("bible_study.html"):
        return FileResponse("bible_study.html")
    raise HTTPException(status_code=404, detail="Bible study interface not found")

@app.get("/quantum-study")
async def quantum_study_interface():
    """Serve Quantum Bible Study interface"""
    if os.path.exists("quantum_study_interface.html"):
        return FileResponse("quantum_study_interface.html")
    raise HTTPException(status_code=404, detail="Quantum study interface not found")

@app.get("/bible-characters")
async def bible_characters_interface():
    """Serve Bible Characters interface"""
    if os.path.exists("bible_characters_interface.html"):
        return FileResponse("bible_characters_interface.html")
    raise HTTPException(status_code=404, detail="Bible characters interface not found")

@app.get("/quantum-ai")
async def quantum_ai_interface():
    """Serve Quantum AI interface"""
    if os.path.exists("quantum_ai_interface.html"):
        return FileResponse("quantum_ai_interface.html")
    raise HTTPException(status_code=404, detail="Quantum AI interface not found")


@app.post("/api/commentary", response_model=CommentaryResponse)
async def build_commentary(request: CommentaryRequest, db: Session = Depends(get_db)):
    """Build or retrieve commentary for a specific verse"""
    try:
        result = agent.build_commentary(
            book=request.book,
            chapter=request.chapter,
            verse=request.verse,
            source_types=request.source_types,
            synthesize=request.synthesize
        )
        return CommentaryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/commentary/{book}/{chapter}/{verse}")
async def get_commentary(
    book: str,
    chapter: int,
    verse: int,
    source_types: Optional[List[str]] = Query(None),
    synthesize: bool = Query(True)
):
    """Get commentary for a specific verse"""
    try:
        result = agent.build_commentary(
            book=book,
            chapter=chapter,
            verse=verse,
            source_types=source_types,
            synthesize=synthesize
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/commentary/{book}/{chapter}/{verse}/{category}")
async def get_commentary_by_category(
    book: str,
    chapter: int,
    verse: int,
    category: str
):
    """Get commentary filtered by category (church_fathers, middle_ages, modern, jewish, popes)"""
    try:
        result = agent.get_commentary_by_category(book, chapter, verse, category)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/search")
async def search_commentaries(request: SearchRequest, db: Session = Depends(get_db)):
    """Search commentaries using natural language query"""
    try:
        results = agent.search_commentaries(
            query=request.query,
            book=request.book,
            chapter=request.chapter,
            verse=request.verse,
            source_types=request.source_types
        )
        
        # Save search history
        search_history = SearchHistory(
            query=request.query,
            book=request.book,
            chapter=request.chapter,
            verse=request.verse,
            results_count=len(results)
        )
        db.add(search_history)
        db.commit()
        
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/suggestions/{book}/{chapter}/{verse}")
async def get_suggestions(book: str, chapter: int, verse: int):
    """Get AI-powered suggestions for improving commentary collection"""
    try:
        suggestions = agent.suggest_improvements(book, chapter, verse)
        return {"suggestions": suggestions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/books")
async def get_books():
    """Get list of all Bible books"""
    from config import BIBLE_BOOKS
    return {"books": BIBLE_BOOKS}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "agent_initialized": agent.llm is not None}
