"""
Understanding Library API
Step 2: Integrate with app - show understanding when viewing verses
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional, List, Dict
import os

from bible_understanding_library import UnderstandingLibrary, UnderstandingGenerator


app = FastAPI(
    title="Bible Understanding Library API",
    description="API for accessing Bible verse and passage understanding",
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

# Initialize library
library = UnderstandingLibrary()
generator = UnderstandingGenerator()


@app.get("/")
async def root():
    """Serve the web interface"""
    if os.path.exists("understanding_library_web.html"):
        return FileResponse("understanding_library_web.html")
    return {
        "name": "Bible Understanding Library API",
        "version": "1.0.0",
        "stats": library.get_stats(),
        "endpoints": {
            "web_interface": "/",
            "get_verse": "/api/understanding/verse/{verse_ref}",
            "get_passage": "/api/understanding/passage/{passage_ref}",
            "list_verses": "/api/understanding/verses",
            "search_theme": "/api/understanding/search?theme={theme}",
            "generate": "/api/understanding/generate",
            "stats": "/api/understanding/stats"
        }
    }

@app.get("/library")
async def library_interface():
    """Serve the web interface (alternative route)"""
    if os.path.exists("understanding_library_web.html"):
        return FileResponse("understanding_library_web.html")
    raise HTTPException(status_code=404, detail="Web interface not found")


@app.get("/api/understanding/verse/{verse_ref}")
async def get_verse_understanding(verse_ref: str):
    """Get understanding for a specific verse"""
    understanding = library.get_verse_understanding(verse_ref)
    
    if not understanding:
        # Try to generate it on the fly
        # For now, return 404 - in production, could generate automatically
        raise HTTPException(
            status_code=404,
            detail=f"Understanding not found for {verse_ref}. Use /api/understanding/generate to create it."
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


@app.get("/api/understanding/passage/{passage_ref}")
async def get_passage_understanding(passage_ref: str):
    """Get understanding for a passage"""
    understanding = library.get_passage_understanding(passage_ref)
    
    if not understanding:
        raise HTTPException(
            status_code=404,
            detail=f"Understanding not found for passage {passage_ref}"
        )
    
    return understanding


@app.get("/api/understanding/search")
async def search_by_theme(theme: str):
    """Search for verses by theme"""
    results = library.search_by_theme(theme)
    return {
        "theme": theme,
        "count": len(results),
        "results": results
    }


@app.post("/api/understanding/generate")
async def generate_understanding(request: Dict):
    """Generate understanding for a verse or passage"""
    verse_ref = request.get("verse_ref")
    verse_text = request.get("verse_text")
    passage_ref = request.get("passage_ref")
    verses = request.get("verses")  # List of (ref, text) tuples
    
    if verse_ref and verse_text:
        # Generate verse understanding
        understanding = generator.generate_verse_understanding(verse_ref, verse_text)
        library.add_verse_understanding(understanding)
        return {
            "status": "success",
            "message": f"Understanding generated for {verse_ref}",
            "understanding": understanding
        }
    
    elif passage_ref and verses:
        # Generate passage understanding
        understanding = generator.generate_passage_understanding(passage_ref, verses)
        library.add_passage_understanding(understanding)
        return {
            "status": "success",
            "message": f"Understanding generated for passage {passage_ref}",
            "understanding": understanding
        }
    
    else:
        raise HTTPException(
            status_code=400,
            detail="Either (verse_ref and verse_text) or (passage_ref and verses) required"
        )


@app.get("/api/understanding/stats")
async def get_stats():
    """Get library statistics"""
    return library.get_stats()


@app.get("/api/understanding/verse/{verse_ref}/markdown")
async def get_verse_markdown(verse_ref: str):
    """Get verse understanding as markdown file"""
    understanding = library.get_verse_understanding(verse_ref)
    
    if not understanding:
        raise HTTPException(status_code=404, detail=f"Understanding not found for {verse_ref}")
    
    # Get markdown file path
    safe_ref = library._safe_filename(verse_ref)
    md_file = library.verses_path / f"{safe_ref}.md"
    
    if md_file.exists():
        return FileResponse(
            str(md_file),
            media_type="text/markdown",
            filename=f"{safe_ref}.md"
        )
    
    raise HTTPException(status_code=404, detail="Markdown file not found")


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
    print("BIBLE UNDERSTANDING LIBRARY API")
    print("=" * 80)
    print(f"\nStarting server on port {port}...")
    print(f"\nAccess on your computer:")
    print(f"  http://localhost:{port}")
    print(f"\nAccess on your iPad/phone:")
    print(f"  http://{local_ip}:{port}")
    print(f"\nAPI Documentation:")
    print(f"  http://localhost:{port}/docs")
    print("\n" + "=" * 80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)