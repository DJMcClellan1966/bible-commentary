"""
API endpoints for Bible Character Models
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from bible_characters import get_bible_characters, BIBLE_CHARACTER_TEXTS, CHARACTER_PERSONALITIES

router = APIRouter(prefix="/api/bible-characters", tags=["bible-characters"])


@router.get("/characters")
async def list_characters():
    """List all available Bible characters"""
    return {
        "characters": list(BIBLE_CHARACTER_TEXTS.keys()),
        "count": len(BIBLE_CHARACTER_TEXTS)
    }


@router.get("/characters/{name}")
async def get_character_info(name: str):
    """Get information about a character"""
    system = get_bible_characters()
    info = system.get_character_info(name)
    
    if "error" in info:
        raise HTTPException(status_code=404, detail=info["error"])
    
    return info


@router.post("/characters/{name}/chat")
async def chat_with_character(name: str, message: dict):
    """Chat with a specific Bible character"""
    system = get_bible_characters()
    
    # Initialize if needed
    if not system.initialized:
        system.initialize_characters()
    
    message_text = message.get("message", "") if isinstance(message, dict) else str(message)
    result = system.chat_with_character(name, message_text)
    
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    
    return result


@router.post("/compare")
async def compare_characters(question: str):
    """Get responses from all characters for comparison"""
    system = get_bible_characters()
    
    # Initialize if needed
    if not system.initialized:
        system.initialize_characters()
    
    return system.compare_characters(question)


@router.get("/characters/{name}/personality")
async def get_character_personality(name: str):
    """Get personality traits of a character"""
    if name not in CHARACTER_PERSONALITIES:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return {
        "character": name,
        "personality": CHARACTER_PERSONALITIES[name],
        "description": get_character_description(name)
    }


def get_character_description(name: str) -> str:
    """Get description of character's personality"""
    descriptions = {
        "Moses": "Moses speaks with authority and reverence, emphasizing God's law, commandments, and the importance of obedience. His responses reflect deep wisdom and leadership.",
        "David": "David responds with passion and warmth, often using poetic language. He emphasizes worship, God's mercy, and the relationship between God and His people.",
        "Solomon": "Solomon speaks with great wisdom and practicality. His responses reflect deep reflection on life, wisdom, and the fear of the Lord.",
        "Paul": "Paul responds with passion and theological depth. He emphasizes grace, faith, the gospel, and the work of Christ. His responses are encouraging and zealous.",
        "John": "John speaks with love and warmth, emphasizing God's love, the Word made flesh, and intimate relationship with God. His responses reflect deep spiritual insight."
    }
    return descriptions.get(name, "Character description not available")
