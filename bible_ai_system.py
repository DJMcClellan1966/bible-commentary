"""
Bible App with Complete AI System Integration
Combines Bible study features with AI capabilities
"""
from complete_ai_system import CompleteAISystem
from quantum_kernel import QuantumKernel, KernelConfig, get_kernel
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from models import Commentary
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BibleAISystem:
    """
    Bible App with Complete AI System
    Combines Bible study with AI capabilities (understanding, reasoning, learning, conversation)
    """
    
    def __init__(self, db: Session, kernel: Optional[QuantumKernel] = None):
        """
        Initialize Bible AI System
        
        Args:
            db: Database session
            kernel: Optional kernel instance (will share with AI system)
        """
        self.db = db
        
        # Use provided kernel or get shared instance
        if kernel is None:
            kernel = get_kernel(KernelConfig(
                embedding_dim=256,
                cache_size=50000,
                enable_caching=True
            ))
        
        self.kernel = kernel
        
        # Create AI system with the same kernel (shared cache!)
        self.ai = CompleteAISystem(config=KernelConfig(
            embedding_dim=256,
            cache_size=50000,
            enable_caching=True
        ))
        
        # Ensure they use the same kernel instance
        self.ai.kernel = self.kernel
        
        logger.info("Bible AI System initialized with shared kernel")
    
    def get_verses(self, limit: int = 1000) -> List[str]:
        """Get verses from database as text"""
        verses = self.db.query(
            Commentary.book,
            Commentary.chapter,
            Commentary.verse,
            Commentary.commentary_text
        ).distinct().limit(limit).all()
        
        verse_texts = []
        for book, chapter, verse, text in verses:
            verse_text = f"{book} {chapter}:{verse} {text}"
            verse_texts.append(verse_text)
        
        return verse_texts
    
    def ai_search(self, query: str, top_k: int = 20) -> Dict:
        """
        AI-powered semantic search with understanding and discovery
        """
        verses = self.get_verses()
        
        # Use AI system for intelligent search
        search_result = self.ai.search.search_and_discover(query, verses)
        
        # Format results with verse references
        formatted_results = []
        for result in search_result['results'][:top_k]:
            # Extract verse reference from text
            text = result['text']
            parts = text.split(' ', 2)
            if len(parts) >= 3:
                book = parts[0]
                chapter_verse = parts[1].split(':')
                if len(chapter_verse) == 2:
                    chapter = int(chapter_verse[0])
                    verse = int(chapter_verse[1])
                    verse_text = parts[2] if len(parts) > 2 else text
                    
                    formatted_results.append({
                        "book": book,
                        "chapter": chapter,
                        "verse": verse,
                        "text": verse_text,
                        "similarity": result['similarity'],
                        "reference": f"{book} {chapter}:{verse}"
                    })
        
        return {
            "query": query,
            "results": formatted_results,
            "count": len(formatted_results),
            "themes": search_result.get('themes', []),
            "related_concepts": list(search_result.get('related_concepts', {}).keys())[:5],
            "understanding": self.ai.understanding.understand_intent(query)
        }
    
    def ai_understand_query(self, query: str, context: List[str] = None) -> Dict:
        """
        Understand user query intent and context
        """
        return self.ai.understanding.understand_intent(query, context)
    
    def ai_reason_about_verses(self, verses: List[str], question: str) -> Dict:
        """
        Use AI reasoning to answer questions about verses
        """
        return self.ai.reasoning.reason(verses, question)
    
    def ai_conversation(self, message: str) -> Dict:
        """
        Have a conversation about the Bible
        """
        response = self.ai.conversation.respond(message)
        
        return {
            "message": message,
            "response": response,
            "intent": self.ai.understanding.understand_intent(message)
        }
    
    def ai_build_knowledge_graph(self, verses: List[str] = None) -> Dict:
        """
        Build knowledge graph of Bible verses
        """
        if verses is None:
            verses = self.get_verses(limit=100)
        
        graph = self.ai.knowledge_graph.build_graph(verses)
        
        return {
            "nodes": len(graph['nodes']),
            "edges": len(graph['edges']),
            "themes": len(graph['themes']),
            "graph": graph
        }
    
    def ai_learn_from_examples(self, examples: List[tuple]) -> Dict:
        """
        Learn patterns from Bible study examples
        """
        return self.ai.learning.learn_from_examples(examples)
    
    def ai_discover_themes(self, verses: List[str] = None, min_cluster_size: int = 2) -> Dict:
        """
        Discover themes in Bible verses using AI
        """
        if verses is None:
            verses = self.get_verses(limit=100)
        
        themes = self.kernel.discover_themes(verses, min_cluster_size=min_cluster_size)
        
        return {
            "themes": themes,
            "count": len(themes)
        }
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        return {
            "kernel": self.kernel.get_stats(),
            "ai_system": self.ai.get_stats()
        }


def create_bible_ai_system(db: Session, kernel: Optional[QuantumKernel] = None) -> BibleAISystem:
    """
    Factory function to create Bible AI System
    
    Args:
        db: Database session
        kernel: Optional shared kernel instance
    
    Returns:
        BibleAISystem instance
    """
    return BibleAISystem(db, kernel)
