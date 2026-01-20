"""
Bible App API - FastAPI Backend
Provides endpoints for verse reading, AI commentary, and semantic search
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import Bible app
try:
    from hyperlinked_bible_app import HyperlinkedBibleApp
    from load_bible_from_html import load_bible_version
    from quantum_llm_standalone import StandaloneQuantumLLM
    from quantum_kernel import KernelConfig
    BIBLE_APP_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import Bible app: {e}")
    BIBLE_APP_AVAILABLE = False

app = FastAPI(
    title="Bible Study App API",
    description="AI-powered Bible study with cross-references, commentary, and semantic search",
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

# Global Bible app instance (lazy loaded)
_bible_app = None
_llm = None

# Book library instance
try:
    from book_library import BookLibrary, initialize_library_with_existing_books
    _book_library = None
    
    def get_book_library():
        """Get or create book library instance"""
        global _book_library
        if _book_library is None:
            _book_library = initialize_library_with_existing_books()
        return _book_library
    LIBRARY_AVAILABLE = True
except ImportError:
    LIBRARY_AVAILABLE = False
    def get_book_library():
        return None

def get_bible_app():
    """Get or create Bible app instance"""
    global _bible_app
    if _bible_app is None:
        if not BIBLE_APP_AVAILABLE:
            raise HTTPException(status_code=503, detail="Bible app not available")
        
        print("Initializing Bible App...")
        _bible_app = HyperlinkedBibleApp()
        
        # Try to load Bible versions if data exists
        base_path = r'C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions'
        if os.path.exists(base_path):
            try:
                versions = {
                    'asv': 'American Standard Version',
                    'engDBY': 'Darby Bible',
                    'englyt': "Young's Literal Translation"
                }
                
                for version_folder, version_name in versions.items():
                    version_path = os.path.join(base_path, version_folder)
                    if os.path.exists(version_path):
                        print(f"Loading {version_name}...")
                        verses = load_bible_version(base_path, version_folder, version_name)
                        if verses:
                            for book, chapter, verse, text in verses[:1000]:  # Load first 1000 for demo
                                _bible_app.add_verse(book, chapter, verse, text, version=version_folder)
                            print(f"Loaded {min(1000, len(verses))} verses from {version_name}")
            except Exception as e:
                print(f"Warning: Could not load Bible versions: {e}")
        else:
            print("Bible data path not found, using empty app")
    
    return _bible_app

def get_llm():
    """Get or create LLM instance for commentary"""
    global _llm
    if _llm is None:
        try:
            app_instance = get_bible_app()
            # Initialize LLM with sample verses for grounded generation
            sample_verses = []
            for version_dict in app_instance.versions.values():
                sample_verses.extend(list(version_dict.values())[:50])  # First 50 verses
            
            _llm = StandaloneQuantumLLM(
                kernel=app_instance.kernel,
                source_texts=sample_verses if sample_verses else ["God is love"]
            )
        except Exception as e:
            print(f"Warning: Could not initialize LLM: {e}")
            _llm = None
    return _llm


@app.get("/")
async def root():
    """Root endpoint"""
    return FileResponse("bible_app.html") if os.path.exists("bible_app.html") else {
        "message": "Bible Study App API",
        "version": "1.0.0",
        "endpoints": {
            "verse": "/api/verse/{book}/{chapter}/{verse}",
            "commentary": "/api/commentary/{book}/{chapter}/{verse}",
            "search": "/api/search",
            "cross_references": "/api/cross-references/{book}/{chapter}/{verse}",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "bible_app_available": BIBLE_APP_AVAILABLE,
        "app_initialized": _bible_app is not None
    }


@app.get("/api/verse/{book}/{chapter}/{verse}")
async def get_verse(
    book: str,
    chapter: int,
    verse: int,
    version: Optional[str] = Query(None, description="Bible version: asv, engDBY, englyt")
):
    """Get a specific verse"""
    try:
        app_instance = get_bible_app()
        verse_text = app_instance.get_verse_text(book, chapter, verse, version)
        
        if not verse_text:
            raise HTTPException(
                status_code=404,
                detail=f"Verse {book} {chapter}:{verse} not found"
            )
        
        # Get available versions for this verse
        available_versions = []
        for ver_name, ver_dict in app_instance.versions.items():
            ref = app_instance._format_reference(book, chapter, verse)
            if ref in ver_dict:
                available_versions.append(ver_name)
        
        return {
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "text": verse_text,
            "version": version or app_instance.default_version,
            "available_versions": available_versions,
            "reference": f"{book} {chapter}:{verse}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/cross-references/{book}/{chapter}/{verse}")
async def get_cross_references(
    book: str,
    chapter: int,
    verse: int,
    top_k: int = Query(10, ge=1, le=50),
    version: Optional[str] = Query(None)
):
    """Get cross-references for a verse"""
    try:
        app_instance = get_bible_app()
        result = app_instance.discover_cross_references(
            book, chapter, verse, top_k=top_k, version=version
        )
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/commentary/{book}/{chapter}/{verse}")
async def get_commentary(
    book: str,
    chapter: int,
    verse: int,
    version: Optional[str] = Query(None),
    include_context: bool = Query(True)
):
    """Generate AI commentary for a verse"""
    try:
        app_instance = get_bible_app()
        llm = get_llm()
        
        if not llm:
            raise HTTPException(
                status_code=503,
                detail="Commentary generation not available"
            )
        
        # Get verse text
        verse_text = app_instance.get_verse_text(book, chapter, verse, version)
        if not verse_text:
            raise HTTPException(
                status_code=404,
                detail=f"Verse {book} {chapter}:{verse} not found"
            )
        
        # Get context if requested
        context = ""
        if include_context:
            # Get surrounding verses
            context_verses = []
            for v in range(max(1, verse - 2), verse + 3):
                try:
                    ctx_text = app_instance.get_verse_text(book, chapter, v, version)
                    if ctx_text:
                        context_verses.append(f"{book} {chapter}:{v} - {ctx_text}")
                except:
                    pass
            if context_verses:
                context = "\n".join(context_verses)
        
        # Generate commentary using grounded generation
        context_part = f'Context (surrounding verses):\n{context}' if context else ''
        prompt = f"""Provide a brief, theologically sound commentary on this Bible verse:

{book} {chapter}:{verse} - {verse_text}

{context_part}

Commentary should include:
1. Brief explanation of the verse's meaning
2. Key theological concepts
3. Practical application (if applicable)

Keep it concise (2-3 paragraphs)."""
        
        try:
            result = llm.generate_grounded(
                prompt,
                max_length=300,
                require_validation=True
            )
            
            commentary = result.get('generated', 'Commentary generation failed.')
            confidence = result.get('confidence', 0.0)
            is_safe = result.get('is_safe', False)
            
            return {
                "verse": f"{book} {chapter}:{verse}",
                "verse_text": verse_text,
                "commentary": commentary,
                "confidence": confidence,
                "is_safe": is_safe,
                "version": version or app_instance.default_version
            }
        except Exception as e:
            # Fallback to simple summary
            return {
                "verse": f"{book} {chapter}:{verse}",
                "verse_text": verse_text,
                "commentary": f"This verse from {book} discusses important biblical themes. Use the cross-references to explore related passages.",
                "confidence": 0.5,
                "is_safe": True,
                "version": version or app_instance.default_version,
                "note": "Simplified commentary (full generation unavailable)"
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search")
async def search_verses(
    query: str = Query(..., description="Search query (semantic search)"),
    top_k: int = Query(10, ge=1, le=50),
    version: Optional[str] = Query(None)
):
    """Semantic search for verses"""
    try:
        app_instance = get_bible_app()
        
        # Collect all verses for search
        all_verses = []
        all_refs = []
        
        version_to_search = version or app_instance.default_version
        
        if version_to_search in app_instance.versions:
            for ref, text in app_instance.versions[version_to_search].items():
                all_verses.append(text)
                all_refs.append(ref)
        else:
            # Search all versions
            for ver_dict in app_instance.versions.values():
                for ref, text in ver_dict.items():
                    all_verses.append(text)
                    all_refs.append(ref)
        
        if not all_verses:
            return {
                "query": query,
                "results": [],
                "total": 0
            }
        
        # Use kernel's semantic search
        similar_verses = app_instance.kernel.find_similar(
            query,
            all_verses,
            top_k=top_k
        )
        
        # Build results
        results = []
        for verse_text, similarity in similar_verses:
            try:
                idx = all_verses.index(verse_text)
                ref = all_refs[idx]
                
                # Parse reference
                parts = ref.split()
                if len(parts) >= 3:
                    book = " ".join(parts[:-1])
                    chapter_verse = parts[-1].split(":")
                    if len(chapter_verse) == 2:
                        chapter = int(chapter_verse[0])
                        verse = int(chapter_verse[1])
                        
                        results.append({
                            "reference": ref,
                            "book": book,
                            "chapter": chapter,
                            "verse": verse,
                            "text": verse_text,
                            "similarity": float(similarity)
                        })
            except (ValueError, IndexError):
                continue
        
        return {
            "query": query,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/versions")
async def get_versions():
    """Get available Bible versions"""
    try:
        app_instance = get_bible_app()
        versions_info = {}
        
        for version_name, verses_dict in app_instance.versions.items():
            versions_info[version_name] = {
                "name": version_name,
                "verse_count": len(verses_dict)
            }
        
        return {
            "versions": versions_info,
            "default": app_instance.default_version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Book Library Endpoints
try:
    from book_library import BookLibrary, initialize_library_with_existing_books
    _book_library = None
    
    def get_book_library():
        """Get or create book library instance"""
        global _book_library
        if _book_library is None:
            _book_library = initialize_library_with_existing_books()
        return _book_library
    LIBRARY_AVAILABLE = True
except ImportError:
    LIBRARY_AVAILABLE = False
    def get_book_library():
        return None


@app.get("/api/library/books")
async def get_library_books():
    """Get all books in the library"""
    if not LIBRARY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Library not available")
    
    try:
        library = get_book_library()
        books = library.get_all_books()
        return {
            "books": books,
            "total": len(books)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/library/books/{book_id}")
async def get_library_book(book_id: int):
    """Get a specific book from the library"""
    if not LIBRARY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Library not available")
    
    try:
        library = get_book_library()
        book = library.get_book(book_id)
        
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Read book content
        content = library.read_book(book_id)
        
        return {
            "book": book,
            "content": content
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/library/search")
async def search_library(query: str = Query(..., description="Search query")):
    """Search books in the library"""
    if not LIBRARY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Library not available")
    
    try:
        library = get_book_library()
        results = library.search_books(query)
        return {
            "query": query,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/library/categories")
async def get_library_categories():
    """Get all book categories"""
    if not LIBRARY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Library not available")
    
    try:
        library = get_book_library()
        return {
            "categories": library.get_categories()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/library/statistics")
async def get_library_statistics():
    """Get library statistics"""
    if not LIBRARY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Library not available")
    
    try:
        library = get_book_library()
        stats = library.get_statistics()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Relationship Journey Endpoints
try:
    from relationship_bible_journey import RelationshipBibleJourney
    _journey_instance = None
    
    def get_journey():
        """Get or create journey instance"""
        global _journey_instance
        if _journey_instance is None:
            _journey_instance = RelationshipBibleJourney()
        return _journey_instance
    JOURNEY_AVAILABLE = True
except ImportError:
    JOURNEY_AVAILABLE = False
    def get_journey():
        return None


@app.post("/api/journey/start")
async def start_journey(
    life_situation: Optional[str] = None,
    seeking: Optional[str] = None
):
    """Start your personalized Bible journey"""
    if not JOURNEY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Journey not available")
    
    try:
        journey = get_journey()
        result = journey.start_journey(
            current_life_situation=life_situation,
            what_youre_seeking=seeking
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/journey/ask")
async def ask_journey_question(question: str = Query(..., description="Your question")):
    """Ask a question - get personalized answer from Scripture"""
    if not JOURNEY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Journey not available")
    
    try:
        journey = get_journey()
        result = journey.ask_question(question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/journey/explore/{book}/{chapter}/{verse}")
async def explore_journey_verse(book: str, chapter: int, verse: int):
    """Explore connections from a verse"""
    if not JOURNEY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Journey not available")
    
    try:
        journey = get_journey()
        verse_ref = f"{book} {chapter}:{verse}"
        result = journey.explore_connections(verse_ref)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/journey/save-verse")
async def save_journey_verse(
    verse_ref: str = Query(..., description="Verse reference"),
    why: Optional[str] = Query(None, description="Why this verse is meaningful")
):
    """Save a verse to your personal collection"""
    if not JOURNEY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Journey not available")
    
    try:
        journey = get_journey()
        result = journey.save_personal_verse(verse_ref, why)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/journey/continue")
async def continue_journey():
    """Continue your journey - get next personalized discovery"""
    if not JOURNEY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Journey not available")
    
    try:
        journey = get_journey()
        result = journey.continue_journey()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/journey/summary")
async def get_journey_summary():
    """Get your journey summary"""
    if not JOURNEY_AVAILABLE:
        raise HTTPException(status_code=503, detail="Journey not available")
    
    try:
        journey = get_journey()
        result = journey.get_journey_summary()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Understanding Bible Endpoints
try:
    from understanding_bible import UnderstandingBible, THEOLOGICAL_TRADITIONS
    _understanding_bible = None
    
    def get_understanding_bible():
        """Get or create Understanding Bible instance"""
        global _understanding_bible
        if _understanding_bible is None:
            _understanding_bible = UnderstandingBible()
        return _understanding_bible
    UNDERSTANDING_AVAILABLE = True
except ImportError:
    UNDERSTANDING_AVAILABLE = False
    def get_understanding_bible():
        return None


@app.get("/api/understanding/{book}/{chapter}/{verse}")
async def get_verse_understanding(
    book: str,
    chapter: int,
    verse: int,
    thinkers: Optional[str] = Query(None, description="Comma-separated list of thinkers")
):
    """Get deep theological understanding of a verse from great thinkers"""
    if not UNDERSTANDING_AVAILABLE:
        raise HTTPException(status_code=503, detail="Understanding Bible not available")
    
    try:
        understanding = get_understanding_bible()
        
        thinker_list = None
        if thinkers:
            thinker_list = [t.strip() for t in thinkers.split(',')]
        
        result = understanding.get_understanding(book, chapter, verse, thinker_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/understanding/compare/{book}/{chapter}/{verse}")
async def compare_thinkers(
    book: str,
    chapter: int,
    verse: int,
    thinker1: str = Query(..., description="First thinker"),
    thinker2: str = Query(..., description="Second thinker")
):
    """Compare how two thinkers understand the same verse"""
    if not UNDERSTANDING_AVAILABLE:
        raise HTTPException(status_code=503, detail="Understanding Bible not available")
    
    try:
        understanding = get_understanding_bible()
        result = understanding.compare_thinkers(book, chapter, verse, thinker1, thinker2)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/understanding/thinkers")
async def get_available_thinkers():
    """Get list of available theological thinkers"""
    if not UNDERSTANDING_AVAILABLE:
        return {"thinkers": [], "available": False}
    
    return {
        "thinkers": THEOLOGICAL_TRADITIONS,
        "available": True
    }


@app.get("/api/understanding/thinker/{thinker_key}")
async def get_thinker_profile(thinker_key: str):
    """Get profile of a theological thinker"""
    if not UNDERSTANDING_AVAILABLE:
        raise HTTPException(status_code=503, detail="Understanding Bible not available")
    
    try:
        understanding = get_understanding_bible()
        result = understanding.get_thinker_profile(thinker_key)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/understanding/theme/{theme}")
async def explore_theme(theme: str, thinkers: Optional[str] = Query(None)):
    """Explore how different thinkers understand a theological theme"""
    if not UNDERSTANDING_AVAILABLE:
        raise HTTPException(status_code=503, detail="Understanding Bible not available")
    
    try:
        understanding = get_understanding_bible()
        
        thinker_list = None
        if thinkers:
            thinker_list = [t.strip() for t in thinkers.split(',')]
        
        result = understanding.explore_theme(theme, thinker_list)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Serve relationship journey web app
@app.get("/journey")
async def journey_web_app():
    """Serve the relationship journey web app"""
    if os.path.exists("relationship_journey_web.html"):
        return FileResponse("relationship_journey_web.html")
    raise HTTPException(status_code=404, detail="Journey web app not found")


# Serve understanding bible web app
@app.get("/understanding")
async def understanding_web_app():
    """Serve the Understanding Bible web app"""
    if os.path.exists("understanding_bible_web.html"):
        return FileResponse("understanding_bible_web.html")
    raise HTTPException(status_code=404, detail="Understanding Bible web app not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)