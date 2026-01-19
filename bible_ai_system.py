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

# Import quantum text generation and translation
try:
    from quantum_text_generation import QuantumTextGenerator, QuantumTranslator
    QUANTUM_TEXT_AVAILABLE = True
except ImportError:
    QUANTUM_TEXT_AVAILABLE = False
    QuantumTextGenerator = None
    QuantumTranslator = None

# Import grounded generation (prevents hallucinations and bias)
try:
    from quantum_grounded_generation import GroundedQuantumGenerator
    GROUNDED_GENERATION_AVAILABLE = True
except ImportError:
    GROUNDED_GENERATION_AVAILABLE = False
    GroundedQuantumGenerator = None

# Import standalone quantum LLM (with progressive learning)
try:
    from quantum_llm_standalone import StandaloneQuantumLLM, create_quantum_llm
    STANDALONE_LLM_AVAILABLE = True
except ImportError:
    STANDALONE_LLM_AVAILABLE = False
    StandaloneQuantumLLM = None
    create_quantum_llm = None

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
        
        # Add quantum text generation and translation
        if QUANTUM_TEXT_AVAILABLE:
            self.text_generator = QuantumTextGenerator(kernel=self.kernel)
            self.translator = QuantumTranslator(kernel=self.kernel)
            # Train on Bible verses
            verses = self.get_verses(limit=100)
            if verses:
                self.text_generator.build_vocab(verses)
            logger.info("Quantum text generation and translation initialized")
        else:
            self.text_generator = None
            self.translator = None
        
        # Add grounded generation (prevents hallucinations and bias)
        if GROUNDED_GENERATION_AVAILABLE:
            verses = self.get_verses(limit=500)  # More verses for better grounding
            if verses:
                self.grounded_generator = GroundedQuantumGenerator(
                    kernel=self.kernel,
                    source_texts=verses
                )
                logger.info(f"Grounded quantum generation initialized with {len(verses)} verified sources")
            else:
                self.grounded_generator = None
        else:
            self.grounded_generator = None
        
        # Add standalone quantum LLM with progressive learning
        if STANDALONE_LLM_AVAILABLE:
            verses = self.get_verses(limit=1000)  # Even more for progressive learning
            if verses:
                self.quantum_llm = create_quantum_llm(
                    kernel=self.kernel,
                    source_texts=verses,
                    config={
                        'confidence_threshold': 0.6,
                        'min_phrase_length': 2,
                        'max_phrase_length': 5,
                        'vocab_expansion_rate': 0.1  # 10% per week
                    }
                )
                logger.info(f"Standalone quantum LLM initialized with {len(verses)} verified sources")
            else:
                self.quantum_llm = None
        else:
            self.quantum_llm = None
        
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
    
    def generate_grounded_text(self, prompt: str, max_length: int = 50, 
                               require_validation: bool = True) -> Dict:
        """
        Generate text grounded in verified Bible sources
        Prevents hallucinations, bias, and misinformation
        Uses standalone quantum LLM if available, otherwise falls back to grounded generator
        """
        # Prefer standalone LLM (has progressive learning)
        if self.quantum_llm:
            return self.quantum_llm.generate_grounded(
                prompt,
                max_length=max_length,
                require_validation=require_validation
            )
        elif self.grounded_generator:
            return self.grounded_generator.generate_grounded(
                prompt, 
                max_length=max_length,
                require_validation=require_validation
            )
        else:
            # Fallback to regular generation if grounded not available
            if self.text_generator:
                result = self.text_generator.generate_text(prompt, max_length=max_length)
                return {
                    "generated": result if isinstance(result, str) else result.get("generated", ""),
                    "confidence": 0.5,  # Lower confidence for ungrounded
                    "is_safe": False,
                    "warning": "Grounded generation not available, using ungrounded method"
                }
            return {
                "error": "No text generation available",
                "is_safe": False
            }
    
    def validate_text(self, text: str) -> Dict:
        """
        Validate text against verified sources
        Detects hallucinations and low-confidence content
        """
        # Use standalone LLM if available, otherwise fallback to grounded generator
        if self.quantum_llm:
            return self.quantum_llm.validate_against_sources(text)
        elif self.grounded_generator:
            return self.grounded_generator.validate_against_sources(text)
        else:
            return {
                "error": "Validation not available",
                "is_safe": False
            }
    
    def detect_bias_in_text(self, text: str) -> Dict:
        """
        Detect potential bias in text
        Checks for one-sided language, missing perspectives, etc.
        """
        # Use standalone LLM if available, otherwise fallback to grounded generator
        if self.quantum_llm:
            return self.quantum_llm.detect_bias(text)
        elif self.grounded_generator:
            return self.grounded_generator.detect_bias(text)
        else:
            return {
                "error": "Bias detection not available",
                "has_bias": False
            }
    
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
    
    def generate_text(self, prompt: str, max_length: int = 50, temperature: float = 0.7) -> Dict:
        """
        Generate text using quantum techniques
        """
        if not self.text_generator:
            return {"error": "Quantum text generation not available"}
        
        generated = self.text_generator.generate_text(prompt, max_length=max_length, temperature=temperature)
        
        return {
            "prompt": prompt,
            "generated": generated,
            "method": "quantum"
        }
    
    def translate_text(self, text: str, source_lang: str = "en", target_lang: str = "es") -> Dict:
        """
        Translate text using quantum techniques
        """
        if not self.translator:
            return {"error": "Quantum translation not available"}
        
        translation = self.translator.translate(text, source_lang=source_lang, target_lang=target_lang)
        
        return {
            "original": text,
            "translation": translation,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "method": "quantum"
        }
    
    def learn_from_llm_output(self, prompt: str, llm_output: str):
        """
        Learn from traditional LLM output to improve quantum generation
        Uses the LLM output as a high-quality example to improve vocabulary and patterns
        """
        if not self.text_generator:
            return {"error": "Quantum text generation not available"}
        
        # Add LLM output as training example (merge with existing vocab)
        # This helps quantum generator learn better patterns from high-quality LLM output
        training_texts = [llm_output]
        self.text_generator.build_vocab(training_texts, merge=True)
        
        # Store prompt-output pairs for better context learning
        if not hasattr(self.text_generator, 'learned_pairs'):
            self.text_generator.learned_pairs = []
        
        self.text_generator.learned_pairs.append((prompt, llm_output))
        
        # Update context window with learned patterns
        # Extract key phrases from LLM output
        import re
        phrases = re.findall(r'\b\w+\s+\w+\b', llm_output.lower())
        if phrases:
            # Add common phrases to context understanding
            for phrase in phrases[:5]:  # Top 5 phrases
                if phrase not in self.text_generator.token_embeddings:
                    self.text_generator.token_embeddings[phrase] = self.kernel.embed(phrase)
        
        return {
            "learned": True,
            "prompt": prompt,
            "example": llm_output[:100] + "...",
            "vocab_size": len(self.text_generator.vocab),
            "learned_pairs": len(self.text_generator.learned_pairs)
        }
    
    def progressive_learning_step(self, new_texts: List[str], week: Optional[int] = None) -> Dict:
        """
        Perform one step of progressive learning
        Gradually expands vocabulary and improves quality
        """
        if not self.quantum_llm:
            return {
                "error": "Standalone quantum LLM not available",
                "suggestion": "Initialize with source texts first"
            }
        
        return self.quantum_llm.progressive_learning_step(new_texts, week)
    
    def get_llm_statistics(self) -> Dict:
        """
        Get statistics about the quantum LLM
        """
        if not self.quantum_llm:
            return {
                "error": "Standalone quantum LLM not available"
            }
        
        return self.quantum_llm.get_statistics()
    
    def save_llm_state(self, filepath: str):
        """
        Save quantum LLM state to file
        """
        if not self.quantum_llm:
            return {"error": "Standalone quantum LLM not available"}
        
        self.quantum_llm.save(filepath)
        return {"success": True, "filepath": filepath}
    
    def load_llm_state(self, filepath: str):
        """
        Load quantum LLM state from file
        """
        if not self.quantum_llm:
            return {"error": "Standalone quantum LLM not available"}
        
        self.quantum_llm.load(filepath)
        return {"success": True, "filepath": filepath}
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        stats = {
            "kernel": self.kernel.get_stats(),
            "ai_system": self.ai.get_stats()
        }
        
        if self.text_generator:
            stats["text_generator"] = {
                "vocab_size": len(self.text_generator.vocab),
                "available": True
            }
        
        if self.translator:
            stats["translator"] = {
                "translation_pairs": len(self.translator.translation_pairs),
                "available": True
            }
        
        if self.quantum_llm:
            stats["quantum_llm"] = self.quantum_llm.get_statistics()
        
        return stats


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
