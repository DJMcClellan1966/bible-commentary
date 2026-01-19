"""
Bible Study Application - Built Around Quantum Kernel
All features use the quantum kernel as the foundation
"""
from quantum_kernel import QuantumKernel, KernelConfig, get_kernel
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Tuple
from models import Commentary
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KernelBasedBibleStudy:
    """
    Bible Study System built around Quantum Kernel
    All operations use the kernel for semantic understanding
    """
    
    def __init__(self, db: Session, kernel: Optional[QuantumKernel] = None):
        self.db = db
        self.kernel = kernel or get_kernel()
        logger.info("Bible Study System initialized with Quantum Kernel")
    
    def search_verses(self, query: str, top_k: int = 20) -> List[Dict]:
        """
        Semantic search for verses using kernel
        """
        # Get all verses from database
        verses = self.db.query(
            Commentary.book, 
            Commentary.chapter, 
            Commentary.verse,
            Commentary.commentary_text
        ).distinct().all()
        
        # Create verse texts for search
        verse_texts = []
        verse_refs = []
        for book, chapter, verse, text in verses:
            verse_text = f"{book} {chapter}:{verse} {text}"
            verse_texts.append(verse_text)
            verse_refs.append((book, chapter, verse, text))
        
        # Use kernel to find similar verses
        results = self.kernel.find_similar(query, verse_texts, top_k=top_k)
        
        # Format results
        formatted_results = []
        for verse_text, similarity in results:
            # Find corresponding reference
            idx = verse_texts.index(verse_text)
            book, chapter, verse, text = verse_refs[idx]
            
            formatted_results.append({
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "similarity": similarity
            })
        
        return formatted_results
    
    def find_cross_references(self, book: str, chapter: int, verse: int, top_k: int = 20) -> List[Dict]:
        """
        Find cross-references using kernel similarity
        """
        # Get the verse text
        commentaries = self.db.query(Commentary).filter(
            Commentary.book == book,
            Commentary.chapter == chapter,
            Commentary.verse == verse
        ).all()
        
        if not commentaries:
            return []
        
        verse_text = " ".join([c.commentary_text for c in commentaries])
        verse_ref = f"{book} {chapter}:{verse}"
        
        # Get all other verses
        all_verses = self.db.query(
            Commentary.book,
            Commentary.chapter,
            Commentary.verse,
            Commentary.commentary_text
        ).filter(
            ~((Commentary.book == book) & 
              (Commentary.chapter == chapter) & 
              (Commentary.verse == verse))
        ).distinct().all()
        
        # Create verse texts
        verse_texts = []
        verse_refs = []
        for b, c, v, text in all_verses:
            full_text = f"{b} {c}:{v} {text}"
            verse_texts.append(full_text)
            verse_refs.append((b, c, v, text))
        
        # Use kernel to find similar
        results = self.kernel.find_similar(verse_text, verse_texts, top_k=top_k)
        
        # Format results
        cross_refs = []
        for verse_text, similarity in results:
            idx = verse_texts.index(verse_text)
            b, c, v, text = verse_refs[idx]
            
            cross_refs.append({
                "book": b,
                "chapter": c,
                "verse": v,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "similarity": similarity,
                "reference": f"{b} {c}:{v}"
            })
        
        return cross_refs
    
    def discover_themes(self, verses: List[Tuple[str, int, int]]) -> List[Dict]:
        """
        Discover themes from verses using kernel
        """
        # Get verse texts
        verse_texts = []
        for book, chapter, verse in verses:
            commentaries = self.db.query(Commentary).filter(
                Commentary.book == book,
                Commentary.chapter == chapter,
                Commentary.verse == verse
            ).all()
            
            if commentaries:
                text = " ".join([c.commentary_text for c in commentaries])
                verse_texts.append(text)
        
        if not verse_texts:
            return []
        
        # Use kernel to discover themes
        themes = self.kernel.discover_themes(verse_texts, min_cluster_size=2)
        
        # Format results with verse references
        formatted_themes = []
        for theme in themes:
            # Map texts back to verse references
            theme_verses = []
            for text in theme['texts']:
                # Find which verse this text came from
                for book, chapter, verse in verses:
                    commentaries = self.db.query(Commentary).filter(
                        Commentary.book == book,
                        Commentary.chapter == chapter,
                        Commentary.verse == verse
                    ).all()
                    if commentaries:
                        verse_text = " ".join([c.commentary_text for c in commentaries])
                        if verse_text == text:
                            theme_verses.append({
                                "book": book,
                                "chapter": chapter,
                                "verse": verse,
                                "reference": f"{book} {chapter}:{verse}"
                            })
                            break
            
            formatted_themes.append({
                "theme": theme['theme'],
                "verses": theme_verses,
                "size": theme['size'],
                "confidence": theme['confidence']
            })
        
        return formatted_themes
    
    def find_conceptual_connections(self, concept: str, top_k: int = 15) -> List[Dict]:
        """
        Find verses related to a concept using kernel
        """
        # Search for concept
        results = self.search_verses(concept, top_k=top_k)
        
        # Build relationship graph for top results
        if results:
            verse_texts = [r["text"] for r in results]
            graph = self.kernel.build_relationship_graph(verse_texts)
            
            # Find most connected verses
            connections = []
            for verse_text, related in graph.items():
                idx = verse_texts.index(verse_text)
                verse_ref = results[idx]
                
                connections.append({
                    "verse": verse_ref,
                    "connections": len(related),
                    "related_verses": [
                        {
                            "text": rel_text,
                            "similarity": sim
                        }
                        for rel_text, sim in related[:5]
                    ]
                })
            
            connections.sort(key=lambda x: x["connections"], reverse=True)
            return connections[:top_k]
        
        return []
    
    def get_kernel_stats(self) -> Dict:
        """Get kernel statistics"""
        return self.kernel.get_stats()


# Initialize kernel-based system
def create_bible_study_system(db: Session) -> KernelBasedBibleStudy:
    """Create Bible study system with kernel"""
    # Configure kernel for Bible study
    config = KernelConfig(
        embedding_dim=256,
        similarity_threshold=0.6,  # Lower threshold for Bible study
        enable_caching=True,
        cache_size=50000  # Larger cache for Bible verses
    )
    
    kernel = get_kernel(config)
    return KernelBasedBibleStudy(db, kernel)
