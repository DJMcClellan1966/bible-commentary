"""
API endpoints for Kernel-Based Bible Study System
All endpoints use the quantum kernel
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from models import get_db
from bible_app_kernel import KernelBasedBibleStudy, create_bible_study_system
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/kernel-bible-study", tags=["kernel-bible-study"])


@router.get("/search")
async def kernel_search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Semantic search using quantum kernel"""
    try:
        study = create_bible_study_system(db)
        results = study.search_verses(query, top_k=top_k)
        return {
            "query": query,
            "results": results,
            "count": len(results),
            "kernel_stats": study.get_kernel_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cross-references/{book}/{chapter}/{verse}")
async def kernel_cross_references(
    book: str,
    chapter: int,
    verse: int,
    top_k: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Find cross-references using kernel"""
    try:
        study = create_bible_study_system(db)
        cross_refs = study.find_cross_references(book, chapter, verse, top_k=top_k)
        return {
            "reference": {"book": book, "chapter": chapter, "verse": verse},
            "cross_references": cross_refs,
            "count": len(cross_refs),
            "kernel_stats": study.get_kernel_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discover-themes")
async def kernel_discover_themes(
    verses: List[dict],  # [{"book": str, "chapter": int, "verse": int}, ...]
    db: Session = Depends(get_db)
):
    """Discover themes using kernel"""
    try:
        study = create_bible_study_system(db)
        
        # Convert to tuples
        verse_tuples = [
            (v["book"], v["chapter"], v["verse"])
            for v in verses
        ]
        
        themes = study.discover_themes(verse_tuples)
        
        return {
            "themes": themes,
            "count": len(themes),
            "kernel_stats": study.get_kernel_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conceptual-connections")
async def kernel_conceptual_connections(
    concept: str = Query(..., description="Concept to find connections for"),
    top_k: int = Query(15, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Find conceptual connections using kernel"""
    try:
        study = create_bible_study_system(db)
        connections = study.find_conceptual_connections(concept, top_k=top_k)
        
        return {
            "concept": concept,
            "connections": connections,
            "count": len(connections),
            "kernel_stats": study.get_kernel_stats()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/kernel-stats")
async def get_kernel_stats(db: Session = Depends(get_db)):
    """Get kernel statistics"""
    try:
        study = create_bible_study_system(db)
        stats = study.get_kernel_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
