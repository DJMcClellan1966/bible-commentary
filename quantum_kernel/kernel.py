"""
Quantum-Inspired Kernel - Universal Processing Layer
Reusable kernel for any application requiring semantic understanding,
similarity computation, and relationship discovery.

This kernel can be used in any application that needs:
- Semantic search
- Similarity computation
- Relationship discovery
- Parallel processing
- Caching and optimization
"""
import numpy as np
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict
import logging
from multiprocessing import Pool, cpu_count
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KernelConfig:
    """Configuration for quantum kernel"""
    embedding_dim: int = 256
    num_parallel_workers: int = None
    similarity_threshold: float = 0.7
    enable_caching: bool = True
    cache_size: int = 10000


class QuantumKernel:
    """
    Quantum-Inspired Kernel
    Core processing layer providing:
    - Semantic embeddings
    - Parallel processing
    - Similarity computation
    - Relationship discovery
    - Caching and optimization
    """
    
    def __init__(self, config: KernelConfig = None):
        self.config = config or KernelConfig()
        self.num_workers = self.config.num_parallel_workers or cpu_count()
        
        # Core data structures
        self.embeddings_cache = {}  # Text -> embedding
        self.similarity_cache = {}  # (text1, text2) -> similarity
        self.relationship_graph = defaultdict(list)  # Text -> related texts
        
        # Statistics
        self.stats = {
            'embeddings_computed': 0,
            'similarities_computed': 0,
            'cache_hits': 0,
            'parallel_operations': 0
        }
    
    def embed(self, text: str, use_cache: bool = True) -> np.ndarray:
        """
        Create semantic embedding for text
        Core operation used by all features
        """
        # Check cache
        if use_cache and self.config.enable_caching:
            if text in self.embeddings_cache:
                self.stats['cache_hits'] += 1
                return self.embeddings_cache[text]
        
        # Create embedding (in production, use proper embeddings like BERT)
        embedding = self._create_embedding(text)
        
        # Cache
        if use_cache and self.config.enable_caching:
            if len(self.embeddings_cache) < self.config.cache_size:
                self.embeddings_cache[text] = embedding
        
        self.stats['embeddings_computed'] += 1
        return embedding
    
    def _create_embedding(self, text: str) -> np.ndarray:
        """Create semantic embedding (simplified - use BERT/Word2Vec in production)"""
        embedding = np.zeros(self.config.embedding_dim)
        
        # Simple hash-based embedding
        for i, char in enumerate(text[:self.config.embedding_dim]):
            embedding[i] = ord(char) / 255.0
        
        # Add semantic features
        words = text.lower().split()
        for word in words[:50]:  # Limit words
            hash_val = hash(word) % self.config.embedding_dim
            embedding[hash_val] += 0.1
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def similarity(self, text1: str, text2: str, use_cache: bool = True) -> float:
        """
        Compute semantic similarity between two texts
        Core operation for search, cross-references, etc.
        """
        # Check cache
        cache_key = tuple(sorted([text1, text2]))
        if use_cache and self.config.enable_caching:
            if cache_key in self.similarity_cache:
                self.stats['cache_hits'] += 1
                return self.similarity_cache[cache_key]
        
        # Compute similarity
        emb1 = self.embed(text1, use_cache=use_cache)
        emb2 = self.embed(text2, use_cache=use_cache)
        similarity = float(np.abs(np.dot(emb1, emb2)))
        
        # Cache
        if use_cache and self.config.enable_caching:
            if len(self.similarity_cache) < self.config.cache_size:
                self.similarity_cache[cache_key] = similarity
        
        self.stats['similarities_computed'] += 1
        return similarity
    
    def find_similar(self, query: str, candidates: List[str], top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Find most similar texts to query
        Used by search, cross-references, theme discovery
        """
        query_embedding = self.embed(query)
        
        # Parallel similarity computation
        similarities = self._parallel_similarity(query_embedding, candidates)
        
        # Sort and return top-k
        results = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
        return results
    
    def _parallel_similarity(self, query_embed: np.ndarray, candidates: List[str]) -> List[Tuple[str, float]]:
        """Compute similarities in parallel"""
        # For small lists, use sequential (overhead not worth it)
        # Also use sequential for now to avoid pickling issues
        # In production, use proper parallel implementation with module-level functions
        if len(candidates) < 100:
            results = []
            for candidate in candidates:
                candidate_embed = self.embed(candidate)
                sim = float(np.abs(np.dot(query_embed, candidate_embed)))
                results.append((candidate, sim))
            return results
        
        # For larger lists, still use sequential for now
        # TODO: Implement proper parallel processing with module-level functions
        results = []
        for candidate in candidates:
            candidate_embed = self.embed(candidate)
            sim = float(np.abs(np.dot(query_embed, candidate_embed)))
            results.append((candidate, sim))
        
        self.stats['parallel_operations'] += 1
        return results
    
    def build_relationship_graph(self, texts: List[str], threshold: float = None) -> Dict[str, List[Tuple[str, float]]]:
        """
        Build relationship graph between texts
        Used for cross-references, theme discovery, connections
        """
        threshold = threshold or self.config.similarity_threshold
        
        # For small lists, use sequential (parallel overhead not worth it)
        if len(texts) < 10:
            results = []
            for text in texts:
                related = []
                text_embed = self.embed(text)
                for other_text in texts:
                    if other_text == text:
                        continue
                    other_embed = self.embed(other_text)
                    similarity = float(np.abs(np.dot(text_embed, other_embed)))
                    if similarity >= threshold:
                        related.append((other_text, similarity))
                results.append((text, related))
        else:
            # Sequential for now (parallel version needs refactoring for pickling)
            # In production, use proper parallel implementation
            results = []
            for text in texts:
                related = []
                text_embed = self.embed(text)
                for other_text in texts:
                    if other_text == text:
                        continue
                    other_embed = self.embed(other_text)
                    similarity = float(np.abs(np.dot(text_embed, other_embed)))
                    if similarity >= threshold:
                        related.append((other_text, similarity))
                results.append((text, related))
        
        # Build graph
        graph = {}
        for text, related in results:
            graph[text] = sorted(related, key=lambda x: x[1], reverse=True)
            self.relationship_graph[text] = related
        
        self.stats['parallel_operations'] += 1
        return graph
    
    def discover_themes(self, texts: List[str], min_cluster_size: int = 3) -> List[Dict]:
        """
        Discover themes by clustering similar texts
        Used for automatic theme discovery
        """
        # Build relationship graph
        graph = self.build_relationship_graph(texts)
        
        # Cluster by similarity
        clusters = []
        processed = set()
        
        for text in texts:
            if text in processed:
                continue
            
            # Start new cluster
            cluster = [text]
            processed.add(text)
            
            # Add related texts
            for related_text, similarity in graph.get(text, []):
                if related_text not in processed and similarity >= self.config.similarity_threshold:
                    cluster.append(related_text)
                    processed.add(related_text)
            
            if len(cluster) >= min_cluster_size:
                # Extract theme
                theme = self._extract_theme(cluster)
                clusters.append({
                    'theme': theme,
                    'texts': cluster,
                    'size': len(cluster),
                    'confidence': self._compute_cluster_confidence(cluster)
                })
        
        return clusters
    
    def _extract_theme(self, texts: List[str]) -> str:
        """Extract theme name from cluster of texts"""
        # Simple: find common words
        words = defaultdict(int)
        for text in texts:
            for word in text.lower().split():
                if len(word) > 3:  # Skip short words
                    words[word] += 1
        
        # Get most common words
        common_words = sorted(words.items(), key=lambda x: x[1], reverse=True)[:3]
        theme = " ".join([word for word, _ in common_words])
        return theme.title() if theme else "Unknown Theme"
    
    def _compute_cluster_confidence(self, cluster: List[str]) -> float:
        """Compute confidence score for cluster"""
        if len(cluster) < 2:
            return 0.0
        
        # Average similarity within cluster
        similarities = []
        for i, text1 in enumerate(cluster):
            for text2 in cluster[i+1:]:
                sim = self.similarity(text1, text2)
                similarities.append(sim)
        
        return float(np.mean(similarities)) if similarities else 0.0
    
    def batch_process(self, items: List[Any], process_func, parallel: bool = True) -> List[Any]:
        """
        Generic batch processing with parallelization
        Used by all features for efficient processing
        """
        if not parallel or len(items) < 10:
            return [process_func(item) for item in items]
        
        # Parallel processing
        with Pool(processes=self.num_workers) as pool:
            results = pool.map(process_func, items)
        
        self.stats['parallel_operations'] += 1
        return results
    
    def get_stats(self) -> Dict:
        """Get kernel statistics"""
        return {
            **self.stats,
            'cache_size': len(self.embeddings_cache),
            'similarity_cache_size': len(self.similarity_cache),
            'num_workers': self.num_workers
        }
    
    def clear_cache(self):
        """Clear caches"""
        self.embeddings_cache.clear()
        self.similarity_cache.clear()
        logger.info("Kernel caches cleared")


# Global kernel instance (singleton pattern)
_kernel_instance: Optional[QuantumKernel] = None


def get_kernel(config: KernelConfig = None) -> QuantumKernel:
    """Get or create global kernel instance"""
    global _kernel_instance
    if _kernel_instance is None:
        _kernel_instance = QuantumKernel(config)
    return _kernel_instance


def reset_kernel():
    """Reset global kernel (for testing)"""
    global _kernel_instance
    _kernel_instance = None
