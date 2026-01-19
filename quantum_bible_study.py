"""
Quantum-Based Bible Study System
Uses quantum entanglement and superposition to discover deeper meaning
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from quantum_tokenizer import QuantumTokenizer
from sqlalchemy.orm import Session
from models import Commentary, get_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumBibleStudy:
    """Quantum-based Bible study system using entanglement for meaning discovery"""
    
    def __init__(self, db: Session, tokenizer: Optional[QuantumTokenizer] = None):
        self.db = db
        self.tokenizer = tokenizer
        if tokenizer is None:
            self.tokenizer = QuantumTokenizer(vocab_size=10000, dimension=256)
            self._train_on_bible_texts()
    
    def _train_on_bible_texts(self):
        """Train quantum tokenizer on Bible texts and commentaries"""
        logger.info("Training quantum tokenizer on Bible texts...")
        
        # Get all commentaries from database
        commentaries = self.db.query(Commentary).all()
        
        texts = []
        for comm in commentaries:
            texts.append(comm.commentary_text)
        
        # Add some common Bible verses for training
        bible_verses = [
            "In the beginning God created the heavens and the earth.",
            "For God so loved the world that he gave his one and only Son.",
            "The Lord is my shepherd, I shall not want.",
            "Love your neighbor as yourself.",
            "Faith is the assurance of things hoped for.",
            "In the beginning was the Word, and the Word was with God.",
            "Be still and know that I am God.",
            "Trust in the Lord with all your heart.",
        ] * 50
        
        texts.extend(bible_verses)
        
        if texts:
            self.tokenizer.train(texts, min_frequency=2)
            logger.info(f"Quantum tokenizer trained on {len(texts)} texts")
        else:
            logger.warning("No texts found for training, using default tokenizer")
    
    def get_verse_quantum_state(self, book: str, chapter: int, verse: int) -> Optional[np.ndarray]:
        """Get quantum state for a specific verse"""
        # Get commentaries for this verse
        commentaries = self.db.query(Commentary).filter(
            Commentary.book == book,
            Commentary.chapter == chapter,
            Commentary.verse == verse
        ).all()
        
        if not commentaries:
            return None
        
        # Combine all commentary texts
        combined_text = " ".join([c.commentary_text for c in commentaries])
        
        # Get quantum state
        return self._get_text_quantum_state(combined_text)
    
    def _get_text_quantum_state(self, text: str) -> np.ndarray:
        """Get quantum superposition state for text"""
        tokens = self.tokenizer.encode(text)
        
        if not tokens:
            return np.zeros(self.tokenizer.dimension, dtype=complex)
        
        text_state = np.zeros(self.tokenizer.dimension, dtype=complex)
        
        for token_id in tokens:
            token = self.tokenizer.id_to_token.get(token_id)
            if token and token in self.tokenizer.vocab:
                qt = self.tokenizer.vocab[token]
                if qt.quantum_state is not None:
                    text_state += qt.amplitude * qt.quantum_state
        
        norm = np.linalg.norm(text_state)
        if norm > 0:
            text_state = text_state / norm
        
        return text_state
    
    def find_thematically_related_verses(
        self,
        book: str,
        chapter: int,
        verse: int,
        top_k: int = 10
    ) -> List[Dict]:
        """Find verses that are thematically related through quantum entanglement"""
        logger.info(f"Finding thematically related verses for {book} {chapter}:{verse}")
        
        # Get quantum state for reference verse
        ref_state = self.get_verse_quantum_state(book, chapter, verse)
        if ref_state is None:
            return []
        
        # Get all unique verses from database
        verses = self.db.query(Commentary.book, Commentary.chapter, Commentary.verse).distinct().all()
        
        similarities = []
        
        for v_book, v_chapter, v_verse in verses:
            # Skip the reference verse itself
            if v_book == book and v_chapter == chapter and v_verse == verse:
                continue
            
            # Get quantum state for this verse
            verse_state = self.get_verse_quantum_state(v_book, v_chapter, v_verse)
            if verse_state is None:
                continue
            
            # Calculate quantum overlap (semantic similarity)
            overlap = np.abs(np.vdot(ref_state, verse_state))
            
            # Calculate entanglement-based similarity
            entanglement_score = self._calculate_entanglement_similarity(
                book, chapter, verse,
                v_book, v_chapter, v_verse
            )
            
            # Combined semantic similarity
            semantic_similarity = overlap * (1 + entanglement_score)
            
            similarities.append({
                "book": v_book,
                "chapter": v_chapter,
                "verse": v_verse,
                "quantum_overlap": float(overlap),
                "entanglement_score": float(entanglement_score),
                "semantic_similarity": float(semantic_similarity)
            })
        
        # Sort by semantic similarity
        similarities.sort(key=lambda x: x["semantic_similarity"], reverse=True)
        
        return similarities[:top_k]
    
    def _calculate_entanglement_similarity(
        self,
        book1: str, chapter1: int, verse1: int,
        book2: str, chapter2: int, verse2: int
    ) -> float:
        """Calculate entanglement-based similarity between two verses"""
        # Get tokens for both verses
        comms1 = self.db.query(Commentary).filter(
            Commentary.book == book1,
            Commentary.chapter == chapter1,
            Commentary.verse == verse1
        ).all()
        
        comms2 = self.db.query(Commentary).filter(
            Commentary.book == book2,
            Commentary.chapter == chapter2,
            Commentary.verse == verse2
        ).all()
        
        if not comms1 or not comms2:
            return 0.0
        
        text1 = " ".join([c.commentary_text for c in comms1])
        text2 = " ".join([c.commentary_text for c in comms2])
        
        tokens1 = set(self.tokenizer.encode(text1))
        tokens2 = set(self.tokenizer.encode(text2))
        
        # Find entangled pairs
        entanglement_strength = 0.0
        total_pairs = 0
        
        for token_id1 in tokens1:
            token1 = self.tokenizer.id_to_token.get(token_id1)
            if token1 and token1 in self.tokenizer.vocab:
                entangled = self.tokenizer.get_entangled_tokens(token1, top_k=20)
                
                for token_id2 in tokens2:
                    token2 = self.tokenizer.id_to_token.get(token_id2)
                    if token2:
                        for ent_token, strength in entangled:
                            if ent_token == token2:
                                entanglement_strength += strength
                                total_pairs += 1
        
        # Normalize
        if total_pairs > 0:
            return entanglement_strength / total_pairs
        return 0.0
    
    def discover_theme(self, verses: List[Tuple[str, int, int]]) -> Dict:
        """Discover the theme connecting multiple verses using quantum analysis"""
        logger.info(f"Discovering theme from {len(verses)} verses")
        
        # Get quantum states for all verses
        verse_states = []
        verse_texts = []
        
        for book, chapter, verse in verses:
            comms = self.db.query(Commentary).filter(
                Commentary.book == book,
                Commentary.chapter == chapter,
                Commentary.verse == verse
            ).all()
            
            if comms:
                text = " ".join([c.commentary_text for c in comms])
                verse_texts.append(text)
                state = self._get_text_quantum_state(text)
                verse_states.append(state)
        
        if not verse_states:
            return {"theme": "Unknown", "confidence": 0.0, "key_concepts": []}
        
        # Find common quantum patterns (themes)
        # Average quantum state represents the theme
        theme_state = np.mean(verse_states, axis=0)
        theme_state = theme_state / np.linalg.norm(theme_state) if np.linalg.norm(theme_state) > 0 else theme_state
        
        # Find tokens that are most entangled with the theme
        theme_tokens = []
        for token, qt in self.tokenizer.vocab.items():
            if qt.quantum_state is not None:
                overlap = np.abs(np.vdot(theme_state, qt.quantum_state))
                theme_tokens.append((token, float(overlap)))
        
        theme_tokens.sort(key=lambda x: x[1], reverse=True)
        
        # Calculate confidence (how well verses align with theme)
        alignments = [np.abs(np.vdot(theme_state, vs)) for vs in verse_states]
        confidence = float(np.mean(alignments))
        
        return {
            "theme": theme_tokens[0][0] if theme_tokens else "Unknown",
            "confidence": confidence,
            "key_concepts": [t[0] for t in theme_tokens[:10]],
            "concept_strengths": {t[0]: t[1] for t in theme_tokens[:10]}
        }
    
    def quantum_search(self, query: str, top_k: int = 20) -> List[Dict]:
        """Search for verses using quantum semantic search"""
        logger.info(f"Quantum search for: {query}")
        
        # Get quantum state for query
        query_state = self._get_text_quantum_state(query)
        
        # Get all verses
        verses = self.db.query(Commentary.book, Commentary.chapter, Commentary.verse).distinct().all()
        
        results = []
        
        for book, chapter, verse in verses:
            verse_state = self.get_verse_quantum_state(book, chapter, verse)
            if verse_state is None:
                continue
            
            # Quantum similarity
            similarity = np.abs(np.vdot(query_state, verse_state))
            
            # Entanglement-based relevance
            relevance = self._calculate_query_relevance(query, book, chapter, verse)
            
            # Combined score
            score = similarity * (1 + relevance)
            
            results.append({
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "quantum_similarity": float(similarity),
                "relevance": float(relevance),
                "score": float(score)
            })
        
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
    
    def _calculate_query_relevance(self, query: str, book: str, chapter: int, verse: int) -> float:
        """Calculate how relevant a verse is to the query using entanglement"""
        query_tokens = set(self.tokenizer.encode(query))
        
        comms = self.db.query(Commentary).filter(
            Commentary.book == book,
            Commentary.chapter == chapter,
            Commentary.verse == verse
        ).all()
        
        if not comms:
            return 0.0
        
        verse_text = " ".join([c.commentary_text for c in comms])
        verse_tokens = set(self.tokenizer.encode(verse_text))
        
        # Find entangled connections
        entanglement_score = 0.0
        connections = 0
        
        for q_token_id in query_tokens:
            q_token = self.tokenizer.id_to_token.get(q_token_id)
            if q_token and q_token in self.tokenizer.vocab:
                entangled = self.tokenizer.get_entangled_tokens(q_token, top_k=20)
                
                for v_token_id in verse_tokens:
                    v_token = self.tokenizer.id_to_token.get(v_token_id)
                    if v_token:
                        for ent_token, strength in entangled:
                            if ent_token == v_token:
                                entanglement_score += strength
                                connections += 1
        
        return entanglement_score / max(connections, 1)
    
    def analyze_commentary_relationships(
        self,
        book: str,
        chapter: int,
        verse: int
    ) -> Dict:
        """Analyze relationships between different commentary sources using quantum methods"""
        commentaries = self.db.query(Commentary).filter(
            Commentary.book == book,
            Commentary.chapter == chapter,
            Commentary.verse == verse
        ).all()
        
        if len(commentaries) < 2:
            return {"relationships": [], "consensus": 0.0}
        
        # Get quantum states for each commentary
        comm_states = []
        for comm in commentaries:
            state = self._get_text_quantum_state(comm.commentary_text)
            comm_states.append((comm, state))
        
        # Calculate pairwise relationships
        relationships = []
        for i, (comm1, state1) in enumerate(comm_states):
            for j, (comm2, state2) in enumerate(comm_states[i+1:], i+1):
                similarity = np.abs(np.vdot(state1, state2))
                
                relationships.append({
                    "source1": comm1.source_name,
                    "source2": comm2.source_name,
                    "source_type1": comm1.source_type.value,
                    "source_type2": comm2.source_type.value,
                    "quantum_similarity": float(similarity),
                    "relationship": "high" if similarity > 0.7 else "medium" if similarity > 0.4 else "low"
                })
        
        # Calculate consensus (how much do all commentaries agree?)
        if comm_states:
            avg_state = np.mean([s[1] for s in comm_states], axis=0)
            consensus_scores = [np.abs(np.vdot(avg_state, s[1])) for s in comm_states]
            consensus = float(np.mean(consensus_scores))
        else:
            consensus = 0.0
        
        return {
            "relationships": relationships,
            "consensus": consensus,
            "interpretation": "high consensus" if consensus > 0.7 else "moderate consensus" if consensus > 0.4 else "low consensus"
        }
    
    def find_conceptual_connections(
        self,
        concept: str,
        top_k: int = 15
    ) -> List[Dict]:
        """Find verses that are conceptually connected to a given concept"""
        logger.info(f"Finding conceptual connections for: {concept}")
        
        # Get tokens related to concept through entanglement
        concept_tokens = self.tokenizer.encode(concept)
        
        if not concept_tokens:
            return []
        
        # Find all tokens entangled with concept
        all_entangled = []
        for token_id in concept_tokens:
            token = self.tokenizer.id_to_token.get(token_id)
            if token and token in self.tokenizer.vocab:
                entangled = self.tokenizer.get_entangled_tokens(token, top_k=30)
                all_entangled.extend([(t, s) for t, s in entangled])
        
        # Get all verses
        verses = self.db.query(Commentary.book, Commentary.chapter, Commentary.verse).distinct().all()
        
        connections = []
        
        for book, chapter, verse in verses:
            comms = self.db.query(Commentary).filter(
                Commentary.book == book,
                Commentary.chapter == chapter,
                Commentary.verse == verse
            ).all()
            
            if not comms:
                continue
            
            verse_text = " ".join([c.commentary_text for c in comms])
            verse_tokens = set(self.tokenizer.encode(verse_text))
            
            # Count how many entangled tokens appear in verse
            connection_strength = 0.0
            connections_found = 0
            
            for ent_token, strength in all_entangled:
                if ent_token in [self.tokenizer.id_to_token.get(tid) for tid in verse_tokens]:
                    connection_strength += strength
                    connections_found += 1
            
            if connections_found > 0:
                connections.append({
                    "book": book,
                    "chapter": chapter,
                    "verse": verse,
                    "connection_strength": float(connection_strength),
                    "connections_found": connections_found
                })
        
        connections.sort(key=lambda x: x["connection_strength"], reverse=True)
        return connections[:top_k]
