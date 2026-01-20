"""
Unified Bible API
Combines Understanding Library with Bible Commentary Agent API
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List, Dict
import os
from pathlib import Path

# Import understanding library
from bible_understanding_library import UnderstandingLibrary, UnderstandingGenerator

app = FastAPI(
    title="Bible Commentary Agent API",
    description="Unified API for Bible study, understanding, and commentary",
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

# Initialize understanding library
library = UnderstandingLibrary()
generator = UnderstandingGenerator()


@app.get("/")
async def root():
    """Root endpoint - serves improved interface if available, otherwise web interface"""
    # Check for improved interface
    if os.path.exists("improved_web_interface.html"):
        return FileResponse("improved_web_interface.html")
    elif os.path.exists("understanding_library_web.html"):
        return FileResponse("understanding_library_web.html")
    else:
        return {
            "message": "Bible Commentary Agent API",
            "version": "1.0.0",
            "endpoints": {
                "web_interface": "/web",
                "improved_interface": "/ (if improved_web_interface.html exists)",
                "bible_study": "/bible-study",
                "bible_ai": "/bible-ai",
                "bible_llm": "/bible-llm",
                "build_commentary": "/api/commentary",
                "search": "/api/search",
                "get_by_category": "/api/commentary/{book}/{chapter}/{verse}/{category}",
                "suggestions": "/api/suggestions/{book}/{chapter}/{verse}",
                "understanding": "/api/understanding/verse/{verse_ref}",
                "understanding_list": "/api/understanding/verses",
                "understanding_stats": "/api/understanding/stats"
            }
        }


@app.get("/web")
async def web_interface():
    """Serve the web interface"""
    if os.path.exists("understanding_library_web.html"):
        return FileResponse("understanding_library_web.html")
    raise HTTPException(status_code=404, detail="Web interface not found")


@app.get("/bible-study")
async def bible_study():
    """Bible study interface"""
    if os.path.exists("bible_study.html"):
        return FileResponse("bible_study.html")
    # Fallback to understanding library
    return await web_interface()


@app.get("/bible-ai")
async def bible_ai():
    """Bible AI interface"""
    if os.path.exists("bible_ai.html"):
        return FileResponse("bible_ai.html")
    return {"message": "Bible AI interface", "status": "available"}


@app.get("/bible-llm")
async def bible_llm():
    """Bible LLM interface"""
    if os.path.exists("bible_llm.html"):
        return FileResponse("bible_llm.html")
    return {"message": "Bible LLM interface", "status": "available"}


# Commentary API Endpoints

@app.post("/api/commentary")
async def build_commentary(request: Dict):
    """
    Build commentary for a verse or passage
    
    Request body:
    {
        "book": "John",
        "chapter": 3,
        "verse": 16,
        "text": "For God so loved the world...",
        "category": "theological" (optional)
    }
    """
    book = request.get("book")
    chapter = request.get("chapter")
    verse = request.get("verse")
    verse_text = request.get("text", "")
    category = request.get("category", "general")
    
    if not all([book, chapter, verse]):
        raise HTTPException(
            status_code=400,
            detail="book, chapter, and verse are required"
        )
    
    verse_ref = f"{book} {chapter}:{verse}"
    
    # Get or generate understanding
    understanding = library.get_verse_understanding(verse_ref)
    
    if not understanding and verse_text:
        # Generate understanding
        understanding = generator.generate_verse_understanding(verse_ref, verse_text)
        library.add_verse_understanding(understanding)
    
    if not understanding:
        raise HTTPException(
            status_code=404,
            detail=f"Commentary not found for {verse_ref}. Provide verse text to generate."
        )
    
    return {
        "reference": verse_ref,
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "category": category,
        "commentary": understanding.get("understanding", ""),
        "themes": understanding.get("themes", []),
        "related_verses": understanding.get("related_verses", [])
    }


@app.get("/api/search")
async def search(
    query: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(10, description="Maximum results")
):
    """Search commentary and understanding"""
    results = []
    
    # Search understanding library by theme
    if query:
        theme_results = library.search_by_theme(query)
        for understanding in theme_results[:limit]:
            results.append({
                "reference": understanding.get("verse_reference"),
                "type": "understanding",
                "content": understanding.get("understanding", "")[:200] + "...",
                "themes": understanding.get("themes", [])
            })
    
    return {
        "query": query,
        "category": category,
        "results": results,
        "count": len(results)
    }


@app.get("/api/commentary/{book}/{chapter}/{verse}/{category}")
async def get_by_category(
    book: str,
    chapter: int,
    verse: int,
    category: str
):
    """Get commentary by category"""
    verse_ref = f"{book} {chapter}:{verse}"
    understanding = library.get_verse_understanding(verse_ref)
    
    if not understanding:
        raise HTTPException(
            status_code=404,
            detail=f"Commentary not found for {verse_ref}"
        )
    
    # Filter by category if needed
    commentary = understanding.get("understanding", "")
    
    return {
        "reference": verse_ref,
        "book": book,
        "chapter": chapter,
        "verse": verse,
        "category": category,
        "commentary": commentary,
        "themes": understanding.get("themes", []),
        "related_verses": understanding.get("related_verses", [])
    }


@app.get("/api/suggestions/{book}/{chapter}/{verse}")
async def suggestions(book: str, chapter: int, verse: int):
    """Get suggestions for related verses and themes"""
    verse_ref = f"{book} {chapter}:{verse}"
    understanding = library.get_verse_understanding(verse_ref)
    
    if not understanding:
        # Try to generate if we have the verse text
        return {
            "reference": verse_ref,
            "suggestions": [],
            "message": "Understanding not found. Use /api/commentary to generate."
        }
    
    related = understanding.get("related_verses", [])
    themes = understanding.get("themes", [])
    
    return {
        "reference": verse_ref,
        "suggestions": {
            "related_verses": [
                {
                    "reference": ref,
                    "text": text[:100] + "..." if len(text) > 100 else text,
                    "similarity": sim
                }
                for ref, text, sim in related[:5]
            ],
            "themes": themes,
            "study_paths": [
                f"Explore theme: {theme}" for theme in themes[:3]
            ]
        }
    }


# Understanding Library Endpoints (integrated)

@app.get("/api/understanding/verse/{verse_ref}")
async def get_verse_understanding(verse_ref: str):
    """Get understanding for a specific verse"""
    understanding = library.get_verse_understanding(verse_ref)
    
    if not understanding:
        raise HTTPException(
            status_code=404,
            detail=f"Understanding not found for {verse_ref}"
        )
    
    return understanding


@app.get("/api/understanding/verses")
async def list_all_verses():
    """List all verses in the library"""
    verses = library.list_all_verses()
    return {
        "total": len(verses),
        "verses": verses
    }


@app.get("/api/understanding/stats")
async def get_understanding_stats():
    """Get library statistics"""
    return library.get_stats()


@app.post("/api/understanding/generate")
async def generate_understanding(request: Dict):
    """Generate understanding for a verse"""
    verse_ref = request.get("verse_ref")
    verse_text = request.get("verse_text")
    
    if not verse_ref or not verse_text:
        raise HTTPException(
            status_code=400,
            detail="verse_ref and verse_text are required"
        )
    
    understanding = generator.generate_verse_understanding(verse_ref, verse_text)
    library.add_verse_understanding(understanding)
    
    return {
        "status": "success",
        "understanding": understanding
    }


if __name__ == "__main__":
    import uvicorn
    import socket
    
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    def find_free_port(start_port=8000, max_attempts=50):
        for port in range(start_port, start_port + max_attempts):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('0.0.0.0', port))
                    return port
            except OSError:
                continue
        raise RuntimeError("Could not find free port")
    
    port = find_free_port()
    local_ip = get_local_ip()
    
    print("\n" + "=" * 80)
    print("UNIFIED BIBLE COMMENTARY AGENT API")
    print("=" * 80)
    print(f"\nStarting server on port {port}...")
    print(f"\nAccess on your computer:")
    print(f"  http://localhost:{port}")
    print(f"\nAccess on your iPad/phone:")
    print(f"  http://{local_ip}:{port}")
    print(f"\nAPI Documentation:")
    print(f"  http://localhost:{port}/docs")
    print(f"\nWeb Interface:")
    print(f"  http://localhost:{port}/web")
    print("\n" + "=" * 80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)