"""
API endpoints for Quantum Bible Study System
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models import get_db
from quantum_bible_study import QuantumBibleStudy
from quantum_tokenizer import QuantumTokenizer
import numpy as np

router = APIRouter(prefix="/api/quantum-study", tags=["quantum-study"])


@router.get("/related-verses/{book}/{chapter}/{verse}")
async def find_related_verses(
    book: str,
    chapter: int,
    verse: int,
    top_k: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Find thematically related verses using quantum entanglement"""
    try:
        quantum_study = QuantumBibleStudy(db)
        related = quantum_study.find_thematically_related_verses(book, chapter, verse, top_k)
        return {
            "reference": {"book": book, "chapter": chapter, "verse": verse},
            "related_verses": related,
            "count": len(related)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discover-theme")
async def discover_theme(
    verses: List[dict],  # [{"book": str, "chapter": int, "verse": int}, ...]
    db: Session = Depends(get_db)
):
    """Discover the theme connecting multiple verses"""
    try:
        quantum_study = QuantumBibleStudy(db)
        verse_list = [(v["book"], v["chapter"], v["verse"]) for v in verses]
        theme = quantum_study.discover_theme(verse_list)
        return theme
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def quantum_search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Quantum semantic search for verses"""
    try:
        quantum_study = QuantumBibleStudy(db)
        results = quantum_study.quantum_search(query, top_k)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/commentary-relationships/{book}/{chapter}/{verse}")
async def analyze_commentary_relationships(
    book: str,
    chapter: int,
    verse: int,
    db: Session = Depends(get_db)
):
    """Analyze relationships between commentary sources using quantum methods"""
    try:
        quantum_study = QuantumBibleStudy(db)
        relationships = quantum_study.analyze_commentary_relationships(book, chapter, verse)
        return relationships
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conceptual-connections")
async def find_conceptual_connections(
    concept: str = Query(..., description="Concept to find connections for"),
    top_k: int = Query(15, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Find verses conceptually connected to a concept"""
    try:
        quantum_study = QuantumBibleStudy(db)
        connections = quantum_study.find_conceptual_connections(concept, top_k)
        return {
            "concept": concept,
            "connections": connections,
            "count": len(connections)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/quantum-state/{book}/{chapter}/{verse}")
async def get_quantum_state(
    book: str,
    chapter: int,
    verse: int,
    db: Session = Depends(get_db)
):
    """Get quantum state representation of a verse"""
    try:
        quantum_study = QuantumBibleStudy(db)
        state = quantum_study.get_verse_quantum_state(book, chapter, verse)
        
        if state is None:
            raise HTTPException(status_code=404, detail="Verse not found")
        
        return {
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "quantum_state_dimension": len(state),
            "state_norm": float(np.linalg.norm(state)),
            "state_sample": state[:10].tolist()  # Sample of first 10 values
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
