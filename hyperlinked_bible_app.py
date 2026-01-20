"""
Hyperlinked American Standard Bible App
Uses Quantum Kernel + AI System to automatically discover cross-references
and generate concise summaries explaining why verses are linked.
"""
from complete_ai_system import CompleteAISystem
from quantum_kernel import KernelConfig
from typing import List, Dict, Tuple, Optional
import re


class HyperlinkedBibleApp:
    """
    American Standard Bible with AI-powered hyperlinks and summaries
    
    Features:
    - Automatic cross-reference discovery using semantic similarity
    - Concise summaries explaining why verses are linked
    - Relationship strength scoring
    - Theme discovery across verses
    """
    
    def __init__(self):
        """Initialize the hyperlinked Bible app"""
        # Configure for Bible study (larger cache for many verses)
        config = KernelConfig(
            embedding_dim=256,
            cache_size=100000,  # Large cache for entire Bible
            enable_caching=True,
            similarity_threshold=0.6  # Lower threshold to find more connections
        )
        
        self.ai = CompleteAISystem(config)
        self.kernel = self.ai.kernel
        
        # Verse storage: {reference: verse_text}
        # Can store multiple versions: {reference: {version: text}} or {reference: text}
        self.verses = {}
        
        # Version storage: {version_name: {reference: text}}
        self.versions = {}
        
        # Default version (for backward compatibility)
        self.default_version = 'asv'
        
        # Computed relationships: {verse_ref: [(related_ref, similarity, summary)]}
        self.relationships = {}
        
        # Theme clusters
        self.themes = {}
    
    def add_verse(self, book: str, chapter: int, verse: int, text: str, version: str = None):
        """
        Add a Bible verse
        
        Args:
            book: Book name (e.g., "John")
            chapter: Chapter number
            verse: Verse number
            text: Verse text
            version: Optional version identifier (e.g., 'asv', 'engDBY', 'englyt')
        """
        reference = self._format_reference(book, chapter, verse)
        
        if version:
            # Store multiple versions
            if version not in self.versions:
                self.versions[version] = {}
            self.versions[version][reference] = text
            
            # Also store in main verses (use first version as default)
            if reference not in self.verses:
                self.verses[reference] = text
        else:
            # Single version (backward compatible)
            self.verses[reference] = text
        
        return reference
    
    def add_verses_batch(self, verses: List[Tuple[str, int, int, str]]):
        """Add multiple verses at once"""
        references = []
        for book, chapter, verse, text in verses:
            ref = self.add_verse(book, chapter, verse, text)
            references.append(ref)
        return references
    
    def _format_reference(self, book: str, chapter: int, verse: int) -> str:
        """Format verse reference"""
        return f"{book} {chapter}:{verse}"
    
    def _parse_reference(self, reference: str) -> Tuple[str, int, int]:
        """Parse verse reference"""
        match = re.match(r"(.+?)\s+(\d+):(\d+)", reference)
        if match:
            book = match.group(1).strip()
            chapter = int(match.group(2))
            verse = int(match.group(3))
            return book, chapter, verse
        return None, 0, 0
    
    def get_verse_text(self, book: str, chapter: int, verse: int, version: str = None) -> str:
        """
        Get verse text for a specific version
        
        Args:
            book: Book name
            chapter: Chapter number
            verse: Verse number
            version: Version identifier (e.g., 'asv'). If None, uses default.
        
        Returns:
            Verse text
        """
        reference = self._format_reference(book, chapter, verse)
        
        if version and version in self.versions:
            return self.versions[version].get(reference, "")
        
        return self.verses.get(reference, "")
    
    def discover_cross_references(self, book: str, chapter: int, verse: int, 
                                   top_k: int = 10, version: str = None) -> Dict:
        """
        Discover cross-references for a specific verse
        
        Args:
            book: Book name
            chapter: Chapter number
            verse: Verse number
            top_k: Number of cross-references to find
        
        Returns:
            Dictionary with cross-references and summaries
        """
        reference = self._format_reference(book, chapter, verse)
        
        # Get verse text for specified version
        verse_text = self.get_verse_text(book, chapter, verse, version)
        
        if not verse_text:
            return {"error": f"Verse {reference} not found"}
        
        # Find semantically similar verses (search across all versions)
        # Collect all verse texts with their references
        all_verse_data = []
        all_refs = []
        
        # Add verses from specified version first, then others
        if version and version in self.versions:
            for ref, text in self.versions[version].items():
                all_verse_data.append(text)
                all_refs.append(ref)
        else:
            # Use all verses (across all versions)
            for ref, text in self.verses.items():
                all_verse_data.append(text)
                all_refs.append(ref)
        
        similar_verses = self.kernel.find_similar(
            verse_text, 
            all_verse_data, 
            top_k=top_k + 1  # +1 to exclude self
        )
        
        # Filter out the verse itself
        cross_refs = []
        for verse_text_match, similarity in similar_verses:
            # Find reference for this verse
            try:
                idx = all_verse_data.index(verse_text_match)
                ref = all_refs[idx]
            except ValueError:
                continue
            
            if ref != reference and similarity >= 0.6:  # Minimum similarity threshold
                # Generate concise summary of why they're linked
                summary = self._generate_link_summary(verse_text, verse_text_match, reference, ref)
                
                cross_refs.append({
                    "reference": ref,
                    "text": verse_text_match,
                    "similarity": similarity,
                    "summary": summary,
                    "relationship_type": self._classify_relationship(verse_text, verse_text_match)
                })
        
        # Sort by similarity (highest first)
        cross_refs.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Store relationships
        self.relationships[reference] = cross_refs
        
        return {
            "verse": reference,
            "verse_text": verse_text,
            "cross_references": cross_refs[:top_k],
            "total_found": len(cross_refs)
        }
    
    def _generate_link_summary(self, verse1: str, verse2: str, ref1: str, ref2: str) -> str:
        """
        Generate concise summary explaining why two verses are linked
        
        Uses AI reasoning to understand the connection
        """
        # Try multiple strategies to get the best summary
        
        # Strategy 1: Extract key words from both verses
        summary = self._extract_key_connection(verse1, verse2)
        if summary:
            return summary
        
        # Strategy 2: Use AI reasoning to understand the connection
        try:
            premises = [verse1, verse2]
            question = "What is the main theme or concept that connects these verses? Answer in 3-4 words."
            
            reasoning = self.ai.reasoning.reason(premises, question)
            
            # Extract concise summary from reasoning
            if reasoning.get('connections'):
                connections = reasoning.get('connections', [])
                if connections:
                    main_connection = connections[0]
                    theme = main_connection.get('theme', '')
                    
                    # Extract meaningful words
                    words = [w for w in theme.split() if len(w) > 3][:4]  # Max 4 meaningful words
                    if words:
                        summary = " ".join(words).title()
                        return summary[:30]  # Max 30 chars
        except Exception:
            pass
        
        # Strategy 3: Use theme discovery
        try:
            themes = self.kernel.discover_themes([verse1, verse2], min_cluster_size=2)
            if themes:
                theme_name = themes[0].get('theme', '')
                words = [w for w in theme_name.split() if len(w) > 3][:3]
                if words:
                    return " ".join(words).title()[:25]
        except Exception:
            pass
        
        # Strategy 4: Use similarity-based description
        summary = self._similarity_based_summary(verse1, verse2)
        return summary if summary else "Related verse"
    
    def _extract_key_connection(self, verse1: str, verse2: str) -> str:
        """Extract key theological concept that connects the verses"""
        # Priority theological terms
        theological_concepts = {
            'love': 'Love',
            'loved': 'Love',
            'loving': 'Love',
            'faith': 'Faith',
            'believe': 'Faith',
            'believed': 'Faith',
            'grace': 'Grace',
            'god': 'God',
            'christ': 'Christ',
            'jesus': 'Christ',
            'salvation': 'Salvation',
            'saved': 'Salvation',
            'save': 'Salvation',
            'spirit': 'Holy Spirit',
            'peace': 'Peace',
            'hope': 'Hope',
            'truth': 'Truth',
            'life': 'Eternal Life',
            'eternal': 'Eternal Life',
            'death': 'Death',
            'sin': 'Sin',
            'righteous': 'Righteousness',
            'holy': 'Holiness',
            'forgive': 'Forgiveness',
            'mercy': 'Mercy'
        }
        
        # Check both verses for theological concepts
        verse1_lower = verse1.lower()
        verse2_lower = verse2.lower()
        
        concepts_found = set()
        for word, concept in theological_concepts.items():
            if word in verse1_lower and word in verse2_lower:
                concepts_found.add(concept)
        
        if concepts_found:
            # Return the first (most common) concept
            return list(concepts_found)[0]
        
        # Fallback: Find common meaningful words (4+ chars)
        words1 = set(w.lower().strip('.,!?;:') for w in verse1.split() if len(w) > 4)
        words2 = set(w.lower().strip('.,!?;:') for w in verse2.split() if len(w) > 4)
        
        stop_words = {'that', 'which', 'this', 'with', 'from', 'have', 'were', 
                     'been', 'will', 'shall', 'there', 'their', 'these', 'those',
                     'whosoever', 'toward', 'would', 'could', 'should'}
        words1 = words1 - stop_words
        words2 = words2 - stop_words
        
        common = words1 & words2
        if common:
            # Use longest meaningful word
            word = max(common, key=len)
            return word.title()[:15]  # Max 15 chars
        
        return None
    
    def _similarity_based_summary(self, verse1: str, verse2: str) -> str:
        """Generate summary based on word overlap"""
        words1 = set(verse1.lower().split())
        words2 = set(verse2.lower().split())
        
        # Remove common words
        common_words = {'the', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
                       'a', 'an', 'to', 'of', 'in', 'on', 'at', 'for', 'with'}
        
        words1 = words1 - common_words
        words2 = words2 - common_words
        
        # Find common meaningful words
        common = words1 & words2
        
        if common:
            # Use most meaningful common words
            meaningful = sorted(common, key=lambda w: len(w), reverse=True)[:3]
            return " ".join(meaningful[:3]).title()
        
        return "Related concept"
    
    def _classify_relationship(self, verse1: str, verse2: str) -> str:
        """Classify the type of relationship between verses"""
        # Use AI understanding to classify
        combined = f"{verse1} {verse2}"
        
        # Check for common relationship patterns
        if any(word in combined.lower() for word in ['love', 'loved', 'loving']):
            return "Love"
        elif any(word in combined.lower() for word in ['faith', 'believe', 'trust']):
            return "Faith"
        elif any(word in combined.lower() for word in ['grace', 'mercy', 'forgive']):
            return "Grace"
        elif any(word in combined.lower() for word in ['salvation', 'save', 'saved']):
            return "Salvation"
        elif any(word in combined.lower() for word in ['hope', 'hope']):
            return "Hope"
        elif any(word in combined.lower() for word in ['peace', 'peaceful']):
            return "Peace"
        else:
            # Use kernel similarity to find theme
            themes = self.kernel.discover_themes([verse1, verse2], min_cluster_size=2)
            if themes:
                return themes[0].get('theme', 'Theme')[:20]
            return "Concept"
    
    def get_verse_with_hyperlinks(self, book: str, chapter: int, verse: int, 
                                   top_k: int = 10, version: str = None) -> Dict:
        """
        Get a verse with its hyperlinked cross-references and summaries
        
        Returns format suitable for rendering hyperlinks
        """
        reference = self._format_reference(book, chapter, verse)
        
        # Get verse text
        verse_text = self.get_verse_text(book, chapter, verse, version)
        
        if not verse_text:
            return {"error": f"Verse {reference} not found"}
        
        # Get cross-references
        cross_refs_data = self.discover_cross_references(book, chapter, verse, top_k, version)
        
        # Format for hyperlink rendering
        hyperlinks = []
        for ref in cross_refs_data.get('cross_references', []):
            hyperlinks.append({
                "reference": ref['reference'],
                "hyperlink_text": ref['reference'],  # Clickable text
                "summary": ref['summary'],  # Tooltip/sidebar text
                "similarity": ref['similarity'],
                "relationship_type": ref['relationship_type']
            })
        
        return {
            "verse": reference,
            "verse_text": verse_text,
            "version": version or self.default_version,
            "available_versions": list(self.versions.keys()),
            "hyperlinks": hyperlinks,
            "summary_suggestions": self._get_summary_suggestions(cross_refs_data)
        }
    
    def _get_summary_suggestions(self, cross_refs_data: Dict) -> List[str]:
        """Get concise summary suggestions for the big picture"""
        if not cross_refs_data.get('cross_references'):
            return []
        
        # Collect relationship types
        relationship_types = [ref.get('relationship_type', '') 
                            for ref in cross_refs_data.get('cross_references', [])]
        
        # Get unique themes
        unique_themes = list(set(relationship_types))[:5]
        
        return unique_themes
    
    def build_knowledge_graph(self) -> Dict:
        """Build complete knowledge graph of all verses"""
        all_verses = list(self.verses.values())
        graph = self.ai.knowledge_graph.build_graph(all_verses)
        
        # Map back to references
        all_refs = list(self.verses.keys())
        
        graph_with_refs = {
            "nodes": [
                {
                    "reference": all_refs[i],
                    "text": node.get("text", ""),
                    "embedding": node.get("embedding", [])
                }
                for i, node in enumerate(graph.get("nodes", []))
            ],
            "edges": graph.get("edges", []),
            "themes": graph.get("themes", []),
            "total_verses": len(self.verses),
            "total_connections": len(graph.get("edges", []))
        }
        
        return graph_with_refs
    
    def discover_themes(self, verses: Optional[List[str]] = None) -> List[Dict]:
        """
        Discover themes across verses
        
        Args:
            verses: List of verse references. If None, uses all verses.
        """
        if verses is None:
            verse_texts = list(self.verses.values())
        else:
            verse_texts = [self.verses[ref] for ref in verses if ref in self.verses]
        
        themes = self.kernel.discover_themes(verse_texts, min_cluster_size=3)
        
        # Map themes back to references
        themes_with_refs = []
        for theme in themes:
            refs_in_theme = []
            for text in theme.get('texts', []):
                # Find reference for this text
                for ref, verse_text in self.verses.items():
                    if verse_text == text:
                        refs_in_theme.append(ref)
                        break
            
            themes_with_refs.append({
                "theme": theme.get('theme', ''),
                "verses": refs_in_theme,
                "size": len(refs_in_theme),
                "confidence": theme.get('confidence', 0.0)
            })
        
        self.themes = themes_with_refs
        return themes_with_refs
    
    def get_stats(self) -> Dict:
        """Get app statistics"""
        return {
            "total_verses": len(self.verses),
            "verses_with_links": len(self.relationships),
            "total_relationships": sum(len(links) for links in self.relationships.values()),
            "themes_discovered": len(self.themes),
            "kernel_stats": self.kernel.get_stats()
        }


# ==================== Example Usage ====================

def example_usage():
    """Example of using the hyperlinked Bible app"""
    
    print("=" * 80)
    print("HYPERLINKED AMERICAN STANDARD BIBLE APP")
    print("=" * 80)
    
    # Create app
    app = HyperlinkedBibleApp()
    
    # Add some verses (ASV format)
    print("\n[1] Adding verses...")
    app.add_verse("John", 3, 16, 
                  "For God so loved the world, that he gave his only begotten Son, "
                  "that whosoever believeth on him should not perish, but have eternal life.")
    
    app.add_verse("1 John", 4, 8, 
                  "He that loveth not knoweth not God; for God is love.")
    
    app.add_verse("1 John", 4, 16, 
                  "And we know and have believed the love which God hath in us. "
                  "God is love; and he that abideth in love abideth in God, and God abideth in him.")
    
    app.add_verse("Romans", 5, 8, 
                  "But God commendeth his own love toward us, in that, while we were yet sinners, "
                  "Christ died for us.")
    
    app.add_verse("Ephesians", 2, 8, 
                  "For by grace have ye been saved through faith; and that not of yourselves, "
                  "it is the gift of God")
    
    app.add_verse("John", 15, 13, 
                  "Greater love hath no man than this, that a man lay down his life for his friends.")
    
    app.add_verse("1 Corinthians", 13, 4, 
                  "Love is patient, love is kind; love envieth not; love vaunteth not itself, is not puffed up")
    
    app.add_verse("Galatians", 5, 22, 
                  "But the fruit of the Spirit is love, joy, peace, longsuffering, kindness, goodness, faithfulness")
    
    print(f"Added {len(app.verses)} verses")
    
    # Get verse with hyperlinks
    print("\n[2] Getting hyperlinked verse: John 3:16")
    result = app.get_verse_with_hyperlinks("John", 3, 16, top_k=5)
    
    print(f"\nVerse: {result['verse']}")
    print(f"Text: {result['verse_text']}")
    print(f"\nFound {len(result['hyperlinks'])} cross-references:\n")
    
    for i, link in enumerate(result['hyperlinks'], 1):
        print(f"{i}. {link['reference']} (similarity: {link['similarity']:.3f})")
        print(f"   Relationship: {link['relationship_type']}")
        print(f"   Summary: {link['summary']}")
        print()
    
    print(f"Big Picture Themes: {', '.join(result['summary_suggestions'])}")
    
    # Discover themes
    print("\n[3] Discovering themes across all verses...")
    themes = app.discover_themes()
    print(f"Found {len(themes)} themes:\n")
    
    for theme in themes:
        print(f"Theme: {theme['theme']}")
        print(f"  Verses: {', '.join(theme['verses'][:5])}")
        print(f"  Size: {theme['size']} verses")
        print(f"  Confidence: {theme['confidence']:.3f}\n")
    
    # Build knowledge graph
    print("[4] Building knowledge graph...")
    graph = app.build_knowledge_graph()
    print(f"Total verses: {graph['total_verses']}")
    print(f"Total connections: {graph['total_connections']}")
    print(f"Themes: {len(graph['themes'])}")
    
    # Get stats
    print("\n[5] App Statistics:")
    stats = app.get_stats()
    print(f"Verses: {stats['total_verses']}")
    print(f"Verses with links: {stats['verses_with_links']}")
    print(f"Total relationships: {stats['total_relationships']}")
    print(f"Themes: {stats['themes_discovered']}")
    print(f"Cache efficiency: {stats['kernel_stats']['cache_hits']} hits")
    
    print("\n" + "=" * 80)
    print("EXAMPLE COMPLETE")
    print("=" * 80)
    print("""
Your hyperlinked Bible app can now:
- Automatically discover cross-references using semantic similarity
- Generate concise summaries explaining why verses are linked
- Show the big picture themes connecting verses
- Build knowledge graphs of biblical concepts

Perfect for your American Standard Bible with AI-powered hyperlinks!
    """)


if __name__ == "__main__":
    example_usage()
