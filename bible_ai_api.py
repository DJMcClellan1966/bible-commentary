"""
API endpoints for Bible App with Complete AI System
"""
from fastapi import APIRouter, HTTPException, Depends, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from pydantic import BaseModel
from models import get_db
from bible_ai_system import BibleAISystem, create_bible_ai_system
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/bible-ai", tags=["bible-ai"])


# Pydantic models
class ConversationRequest(BaseModel):
    message: str


class ReasoningRequest(BaseModel):
    verses: List[str]
    question: str


class LearningRequest(BaseModel):
    examples: List[List[str]]  # List of [input, output] pairs


class TextGenerationRequest(BaseModel):
    prompt: str
    max_length: int = 50
    temperature: float = 0.7


class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "es"


class LearnFromLLMRequest(BaseModel):
    prompt: str
    llm_output: str


@router.get("/search")
async def ai_search(
    query: str = Query(..., description="Search query"),
    top_k: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """AI-powered semantic search with understanding and discovery"""
    try:
        system = create_bible_ai_system(db)
        result = system.ai_search(query, top_k=top_k)
        return result
    except Exception as e:
        logger.error(f"Error in AI search: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/understand")
async def ai_understand(
    query: str = Query(..., description="Query to understand"),
    context: Optional[List[str]] = Query(None, description="Context for understanding"),
    db: Session = Depends(get_db)
):
    """Understand user query intent and context"""
    try:
        system = create_bible_ai_system(db)
        result = system.ai_understand_query(query, context)
        return result
    except Exception as e:
        logger.error(f"Error in understanding: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reason")
async def ai_reason(
    request: ReasoningRequest,
    db: Session = Depends(get_db)
):
    """Use AI reasoning to answer questions about verses"""
    try:
        system = create_bible_ai_system(db)
        result = system.ai_reason_about_verses(request.verses, request.question)
        return result
    except Exception as e:
        logger.error(f"Error in reasoning: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversation")
async def ai_conversation(
    request: ConversationRequest,
    db: Session = Depends(get_db)
):
    """Have a conversation about the Bible"""
    try:
        system = create_bible_ai_system(db)
        result = system.ai_conversation(request.message)
        return result
    except Exception as e:
        logger.error(f"Error in conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/knowledge-graph")
async def ai_knowledge_graph(
    limit: int = Query(100, ge=10, le=500, description="Number of verses to include"),
    db: Session = Depends(get_db)
):
    """Build knowledge graph of Bible verses"""
    try:
        system = create_bible_ai_system(db)
        verses = system.get_verses(limit=limit)
        result = system.ai_build_knowledge_graph(verses)
        return result
    except Exception as e:
        logger.error(f"Error building knowledge graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn")
async def ai_learn(
    request: LearningRequest,
    db: Session = Depends(get_db)
):
    """Learn patterns from Bible study examples"""
    try:
        system = create_bible_ai_system(db)
        # Convert to tuples
        examples = [(ex[0], ex[1]) for ex in request.examples if len(ex) >= 2]
        result = system.ai_learn_from_examples(examples)
        return result
    except Exception as e:
        logger.error(f"Error in learning: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/themes")
async def ai_themes(
    limit: int = Query(100, ge=10, le=500, description="Number of verses to analyze"),
    min_cluster_size: int = Query(2, ge=2, le=10, description="Minimum cluster size"),
    db: Session = Depends(get_db)
):
    """Discover themes in Bible verses using AI"""
    try:
        system = create_bible_ai_system(db)
        verses = system.get_verses(limit=limit)
        result = system.ai_discover_themes(verses, min_cluster_size=min_cluster_size)
        return result
    except Exception as e:
        logger.error(f"Error discovering themes: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-text")
async def ai_generate_text(
    request: TextGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate text using quantum techniques"""
    try:
        system = create_bible_ai_system(db)
        result = system.generate_text(
            request.prompt,
            max_length=request.max_length,
            temperature=request.temperature
        )
        return result
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate")
async def ai_translate(
    request: TranslationRequest,
    db: Session = Depends(get_db)
):
    """Translate text using quantum techniques"""
    try:
        system = create_bible_ai_system(db)
        result = system.translate_text(
            request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        return result
    except Exception as e:
        logger.error(f"Error translating: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn-from-llm")
async def ai_learn_from_llm(
    request: LearnFromLLMRequest,
    db: Session = Depends(get_db)
):
    """Learn from traditional LLM output to improve quantum generation"""
    try:
        system = create_bible_ai_system(db)
        result = system.learn_from_llm_output(request.prompt, request.llm_output)
        return result
    except Exception as e:
        logger.error(f"Error learning from LLM: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def ai_stats(
    db: Session = Depends(get_db)
):
    """Get AI system and kernel statistics"""
    try:
        system = create_bible_ai_system(db)
        stats = system.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
