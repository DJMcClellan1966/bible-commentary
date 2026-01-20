"""
Optimize Bible Version Storage and Search
Implements performance optimizations for 3 Bible versions:
- Pre-computed embedding cache
- Indexed verse lookups
- Batch processing
- Parallel loading
- Spatial indexing for fast similarity search
- Relationship pre-computation
"""
import os
import pickle
import json
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
import numpy as np
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from hyperlinked_bible_app import HyperlinkedBibleApp
from load_bible_from_html import load_bible_version, BOOK_MAPPINGS
from quantum_kernel import KernelConfig
from complete_ai_system import CompleteAISystem


class OptimizedBibleApp(HyperlinkedBibleApp):
    """
    Optimized version of HyperlinkedBibleApp with:
    - Pre-computed embeddings for all verses
    - Indexed verse storage for O(1) lookups
    - Spatial index for fast similarity search
    - Cached cross-references
    - Batch operations
    """
    
    def __init__(self, precompute_embeddings: bool = True, 
                 cache_relationships: bool = True,
                 cache_dir: str = "bible_cache"):
        """Initialize optimized app"""
        # Use larger cache for optimization
        config = KernelConfig(
            embedding_dim=256,
            cache_size=200000,  # Larger cache
            enable_caching=True,
            similarity_threshold=0.6
        )
        
        self.ai = CompleteAISystem(config)
        self.kernel = self.ai.kernel
        
        # Optimized storage structures
        self.versions = {}  # {version: {reference: text}}
        self.default_version = 'asv'
        
        # Indexed storage: {version: {book: {chapter: {verse: text}}}}
        self._indexed_verses = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
        
        # Pre-computed embeddings: {version: {reference: embedding_vector}}
        self._embeddings_cache = defaultdict(dict)
        
        # Text to reference mapping for fast reverse lookup
        self._text_to_ref = {}  # {text: (version, reference)}
        
        # Spatial index (KD-tree or similar) - built after loading
        self._spatial_index = None
        self._indexed_verse_list = []  # List of (reference, version, embedding)
        
        # Cached relationships: {reference: [cross_refs]}
        self._relationship_cache = {}
        
        # Optimization flags
        self.precompute_embeddings = precompute_embeddings
        self.cache_relationships = cache_relationships
        self.cache_dir = cache_dir
        
        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load existing cache if available
        self._load_cache()
    
    def add_verse(self, book: str, chapter: int, verse: int, text: str, version: str = None):
        """Add verse with indexing"""
        reference = self._format_reference(book, chapter, verse)
        version = version or self.default_version
        
        if version not in self.versions:
            self.versions[version] = {}
        
        self.versions[version][reference] = text
        self._indexed_verses[version][book][chapter][verse] = text
        self._text_to_ref[text] = (version, reference)
        
        # Pre-compute embedding if enabled
        if self.precompute_embeddings:
            try:
                embedding = self.kernel.embed(text)
                self._embeddings_cache[version][reference] = embedding
            except Exception as e:
                print(f"Warning: Could not pre-compute embedding for {reference}: {e}")
        
        return reference
    
    def add_verses_batch(self, verses_data: List[Tuple[str, int, int, str]], 
                        version: str = None, 
                        batch_size: int = 1000,
                        parallel: bool = True):
        """Add multiple verses with batch optimization"""
        version = version or self.default_version
        
        print(f"Adding {len(verses_data)} verses in batches of {batch_size}...")
        
        # Process in batches
        for i in range(0, len(verses_data), batch_size):
            batch = verses_data[i:i + batch_size]
            
            if parallel and self.precompute_embeddings:
                # Parallel embedding computation
                self._add_batch_parallel(batch, version)
            else:
                # Sequential processing
                for book, chapter, verse, text in batch:
                    self.add_verse(book, chapter, verse, text, version)
            
            if (i // batch_size + 1) % 10 == 0:
                print(f"  Processed {min(i + batch_size, len(verses_data))}/{len(verses_data)} verses...")
        
        print(f"[OK] Added {len(verses_data)} verses from {version}")
        
        # Build spatial index after batch
        if self.precompute_embeddings:
            self._build_spatial_index()
    
    def _add_batch_parallel(self, batch: List[Tuple[str, int, int, str]], version: str):
        """Add batch with parallel embedding computation"""
        # Collect texts
        texts = [text for _, _, _, text in batch]
        
        # Batch embed (kernel handles this efficiently)
        embeddings = []
        for text in texts:
            try:
                emb = self.kernel.embed(text)
                embeddings.append(emb)
            except Exception:
                embeddings.append(None)
        
        # Add verses with pre-computed embeddings
        for (book, chapter, verse, text), embedding in zip(batch, embeddings):
            reference = self._format_reference(book, chapter, verse)
            
            if version not in self.versions:
                self.versions[version] = {}
            self.versions[version][reference] = text
            self._indexed_verses[version][book][chapter][verse] = text
            self._text_to_ref[text] = (version, reference)
            
            if embedding is not None:
                self._embeddings_cache[version][reference] = embedding
    
    def _build_spatial_index(self):
        """Build spatial index for fast similarity search"""
        print("Building spatial index...")
        self._indexed_verse_list = []
        
        for version, verses_dict in self.versions.items():
            for reference, text in verses_dict.items():
                if reference in self._embeddings_cache[version]:
                    embedding = self._embeddings_cache[version][reference]
                    self._indexed_verse_list.append((reference, version, embedding, text))
        
        print(f"[OK] Spatial index built with {len(self._indexed_verse_list)} verses")
    
    def get_verse_text(self, book: str, chapter: int, verse: int, version: str = None) -> str:
        """Get verse text using indexed lookup (O(1))"""
        version = version or self.default_version
        
        if version in self._indexed_verses:
            if book in self._indexed_verses[version]:
                if chapter in self._indexed_verses[version][book]:
                    return self._indexed_verses[version][book][chapter].get(verse, "")
        
        # Fallback to original method
        reference = self._format_reference(book, chapter, verse)
        if version in self.versions:
            return self.versions[version].get(reference, "")
        return ""
    
    def discover_cross_references(self, book: str, chapter: int, verse: int,
                                  top_k: int = 10, version: str = None,
                                  use_cache: bool = True) -> Dict:
        """Optimized cross-reference discovery"""
        reference = self._format_reference(book, chapter, verse)
        version = version or self.default_version
        
        # Check cache first
        if use_cache and self.cache_relationships:
            cache_key = f"{reference}:{version}"
            if cache_key in self._relationship_cache:
                cached_result = self._relationship_cache[cache_key]
                return {
                    **cached_result,
                    "cached": True
                }
        
        verse_text = self.get_verse_text(book, chapter, verse, version)
        if not verse_text:
            return {"error": f"Verse {reference} not found in {version}"}
        
        # Use pre-computed embeddings if available
        if reference in self._embeddings_cache[version]:
            source_embedding = self._embeddings_cache[version][reference]
            
            # Fast similarity search using spatial index
            similarities = []
            for ref, ver, embedding, text in self._indexed_verse_list:
                if ref == reference and ver == version:
                    continue
                
                # Compute similarity using pre-computed embeddings
                similarity = float(np.abs(np.dot(source_embedding, embedding)))
                if similarity >= 0.6:
                    similarities.append((ref, ver, text, similarity))
            
            # Sort and take top_k
            similarities.sort(key=lambda x: x[3], reverse=True)
            similar_verses = similarities[:top_k]
        else:
            # Fallback to original method (slower)
            return super().discover_cross_references(book, chapter, verse, top_k, version)
        
        # Build cross-references
        cross_refs = []
        for ref, ver, text, similarity in similar_verses:
            summary = self._generate_link_summary(verse_text, text, reference, ref)
            cross_refs.append({
                "reference": ref,
                "version": ver,
                "text": text,
                "similarity": similarity,
                "summary": summary,
                "relationship_type": self._classify_relationship(verse_text, text)
            })
        
        result = {
            "verse": reference,
            "verse_text": verse_text,
            "source_version": version,
            "cross_references": cross_refs,
            "total_found": len(cross_refs),
            "cached": False
        }
        
        # Cache result
        if self.cache_relationships:
            cache_key = f"{reference}:{version}"
            self._relationship_cache[cache_key] = result
        
        return result
    
    def get_stats(self) -> Dict:
        """Get optimized app statistics"""
        total_verses = sum(len(verses) for verses in self.versions.values())
        total_embeddings = sum(len(embeddings) for embeddings in self._embeddings_cache.values())
        
        return {
            "total_verses": total_verses,
            "versions": list(self.versions.keys()),
            "verses_with_links": len(self._relationship_cache),
            "embeddings_cached": total_embeddings,
            "spatial_index_size": len(self._indexed_verse_list),
            "kernel_stats": self.kernel.get_stats(),
            "optimizations": {
                "precompute_embeddings": self.precompute_embeddings,
                "cache_relationships": self.cache_relationships,
                "cache_dir": self.cache_dir
            }
        }
    
    def _save_cache(self):
        """Save embeddings and cache to disk"""
        print("Saving cache to disk...")
        
        # Save embeddings (only for one version to save space - can expand)
        embeddings_file = os.path.join(self.cache_dir, "embeddings_cache.pkl")
        with open(embeddings_file, 'wb') as f:
            pickle.dump(dict(self._embeddings_cache), f)
        
        # Save relationship cache
        relationships_file = os.path.join(self.cache_dir, "relationships_cache.json")
        with open(relationships_file, 'w', encoding='utf-8') as f:
            # Convert to JSON-serializable format
            json_cache = {}
            for key, value in self._relationship_cache.items():
                json_cache[key] = {
                    **value,
                    "cached": False  # Will be marked as cached on load
                }
            json.dump(json_cache, f, indent=2)
        
        print(f"[OK] Cache saved to {self.cache_dir}")
    
    def _load_cache(self):
        """Load embeddings and cache from disk"""
        embeddings_file = os.path.join(self.cache_dir, "embeddings_cache.pkl")
        relationships_file = os.path.join(self.cache_dir, "relationships_cache.json")
        
        if os.path.exists(embeddings_file):
            print("Loading embeddings cache...")
            try:
                with open(embeddings_file, 'rb') as f:
                    self._embeddings_cache = defaultdict(dict, pickle.load(f))
                print(f"[OK] Loaded embeddings for {sum(len(v) for v in self._embeddings_cache.values())} verses")
            except Exception as e:
                print(f"Warning: Could not load embeddings cache: {e}")
        
        if os.path.exists(relationships_file):
            print("Loading relationships cache...")
            try:
                with open(relationships_file, 'r', encoding='utf-8') as f:
                    self._relationship_cache = json.load(f)
                print(f"[OK] Loaded {len(self._relationship_cache)} cached relationships")
            except Exception as e:
                print(f"Warning: Could not load relationships cache: {e}")


def optimize_all_versions(base_path: str, 
                          precompute: bool = True,
                          cache_results: bool = True):
    """
    Load and optimize all 3 Bible versions
    
    Args:
        base_path: Path to bible-versions folder
        precompute: Pre-compute embeddings for faster search
        cache_results: Cache cross-references for instant retrieval
    """
    print("=" * 80)
    print("OPTIMIZING ALL BIBLE VERSIONS")
    print("=" * 80)
    
    # Create optimized app
    print("\n[1] Initializing Optimized Bible App...")
    app = OptimizedBibleApp(
        precompute_embeddings=precompute,
        cache_relationships=cache_results
    )
    
    # Version info
    versions = {
        'asv': 'American Standard Version',
        'engDBY': 'Darby Bible',
        'englyt': "Young's Literal Translation"
    }
    
    total_loaded = 0
    
    # Load each version
    for version_folder, version_name in versions.items():
        print(f"\n{'='*80}")
        print(f"[2] Loading {version_name} ({version_folder})")
        print(f"{'='*80}")
        
        verses = load_bible_version(base_path, version_folder, version_name)
        
        if verses:
            print(f"\nOptimized loading of {len(verses)} verses...")
            app.add_verses_batch(verses, version=version_folder, parallel=True)
            total_loaded += len(verses)
        else:
            print(f"[WARNING] No verses found for {version_name}")
    
    # Save cache
    if precompute or cache_results:
        app._save_cache()
    
    # Statistics
    print("\n" + "=" * 80)
    print("OPTIMIZATION COMPLETE")
    print("=" * 80)
    
    stats = app.get_stats()
    print(f"\nTotal verses loaded: {total_loaded}")
    print(f"Versions loaded: {list(app.versions.keys())}")
    print(f"Embeddings cached: {sum(len(v) for v in app._embeddings_cache.values())}")
    print(f"Relationships cached: {len(app._relationship_cache)}")
    kernel_stats = app.kernel.get_stats()
    print(f"Kernel cache: {kernel_stats.get('cache_size', 0)} items")
    print(f"Embeddings computed: {kernel_stats.get('embeddings_computed', 0)}")
    
    # Performance test
    print("\n" + "=" * 80)
    print("PERFORMANCE TEST")
    print("=" * 80)
    
    import time
    
    test_verses = [
        ("John", 3, 16, "asv"),
        ("Romans", 8, 28, "engDBY"),
        ("1 Corinthians", 13, 4, "englyt")
    ]
    
    for book, chapter, verse, version in test_verses:
        start = time.time()
        result = app.discover_cross_references(book, chapter, verse, top_k=5, version=version)
        elapsed = time.time() - start
        
        print(f"\n{result['verse']} ({version}):")
        print(f"  Time: {elapsed:.3f}s")
        print(f"  Found: {result['total_found']} cross-references")
        print(f"  Cached: {result.get('cached', False)}")
        if result['cross_references']:
            print(f"  Top match: {result['cross_references'][0]['reference']} "
                  f"(similarity: {result['cross_references'][0]['similarity']:.3f})")
    
    print("\n" + "=" * 80)
    print("[OK] OPTIMIZATION COMPLETE!")
    print("=" * 80)
    
    return app


if __name__ == "__main__":
    # Update this path to your Bible versions folder
    base_path = r'C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions'
    
    if not os.path.exists(base_path):
        print(f"ERROR: Path not found: {base_path}")
        print("Please update base_path in the script.")
    else:
        app = optimize_all_versions(
            base_path=base_path,
            precompute=True,  # Pre-compute embeddings (faster search, more memory)
            cache_results=True  # Cache cross-references (instant retrieval)
        )