"""
API endpoints for Bible LLM Integration
Best LLM + Quantum learning system
"""
from fastapi import APIRouter, HTTPException, Depends, Query, Body
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from models import get_db
from bible_ai_system import create_bible_ai_system
from bible_llm_integration import create_bible_llm_integration
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/bible-llm", tags=["bible-llm"])


# Pydantic models
class GenerationRequest(BaseModel):
    prompt: str
    context: Optional[str] = None
    use_llm: bool = True
    use_quantum: bool = True


class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "es"
    use_llm: bool = True


class MultiLLMLearningRequest(BaseModel):
    prompt: str
    max_llms: int = 3


@router.get("/status")
async def llm_status(db: Session = Depends(get_db)):
    """Get LLM integration status"""
    try:
        bible_ai = create_bible_ai_system(db)
        llm_integration = create_bible_llm_integration(bible_ai)
        status = llm_integration.get_status()
        return status
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate")
async def llm_generate(
    request: GenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate text using best available LLM (with quantum learning)"""
    try:
        bible_ai = create_bible_ai_system(db)
        llm_integration = create_bible_llm_integration(bible_ai)
        
        if request.use_llm and request.use_quantum:
            result = llm_integration.generate_hybrid(
                request.prompt,
                use_llm=request.use_llm,
                use_quantum=request.use_quantum
            )
        elif request.use_llm:
            result = llm_integration.generate_with_llm(request.prompt, request.context)
        else:
            result = bible_ai.generate_text(request.prompt)
        
        return result
    except Exception as e:
        logger.error(f"Error generating: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate")
async def llm_translate(
    request: TranslationRequest,
    db: Session = Depends(get_db)
):
    """Translate using best available method (LLM preferred, quantum fallback)"""
    try:
        bible_ai = create_bible_ai_system(db)
        llm_integration = create_bible_llm_integration(bible_ai)
        
        if request.use_llm:
            result = llm_integration.translate_with_llm(
                request.text,
                request.source_lang,
                request.target_lang
            )
        else:
            result = bible_ai.translate_text(
                request.text,
                request.source_lang,
                request.target_lang
            )
        
        return result
    except Exception as e:
        logger.error(f"Error translating: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn-from-llm")
async def learn_from_llm(
    prompt: str = Body(...),
    llm_output: str = Body(...),
    db: Session = Depends(get_db)
):
    """Manually trigger learning from LLM output"""
    try:
        bible_ai = create_bible_ai_system(db)
        result = bible_ai.learn_from_llm_output(prompt, llm_output)
        return result
    except Exception as e:
        logger.error(f"Error learning: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn-from-multiple")
async def learn_from_multiple_llms(
    request: MultiLLMLearningRequest,
    db: Session = Depends(get_db)
):
    """Learn from multiple LLMs simultaneously for faster convergence"""
    try:
        bible_ai = create_bible_ai_system(db)
        llm_integration = create_bible_llm_integration(bible_ai)
        result = llm_integration.learn_from_multiple_llms(
            request.prompt,
            max_llms=request.max_llms
        )
        return result
    except Exception as e:
        logger.error(f"Error learning from multiple LLMs: {e}")
        raise HTTPException(status_code=500, detail=str(e))
