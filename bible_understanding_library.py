"""
Bible Understanding Library
Generates actual, readable content that provides understanding
Not outlines or plans - real commentary and insights
"""
from typing import Dict, List, Optional, Tuple
import json
import os
from pathlib import Path
from datetime import datetime
import re

from quantum_kernel import QuantumKernel, get_kernel, KernelConfig
from complete_ai_system import CompleteAISystem
from quantum_llm_standalone import StandaloneQuantumLLM


class UnderstandingGenerator:
    """
    Generates actual, readable understanding content
    Not outlines - real commentary and insights
    """
    
    def __init__(self, kernel: Optional[QuantumKernel] = None, 
                 ai_system: Optional[CompleteAISystem] = None,
                 llm: Optional[StandaloneQuantumLLM] = None):
        self.kernel = kernel or get_kernel(KernelConfig())
        self.ai_system = ai_system or CompleteAISystem()
        self.llm = llm or StandaloneQuantumLLM(kernel=self.kernel)
        
        # Sample verses for demonstration (in production, load from actual Bible)
        self.sample_verses = {
            "John 3:16": "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
            "Proverbs 3:5-6": "Trust in the Lord with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths.",
            "Romans 8:28": "And we know that all things work together for good to them that love God, to them who are the called according to his purpose.",
            "Matthew 6:33": "But seek ye first the kingdom of God, and his righteousness; and all these things shall be added unto you.",
            "Philippians 4:13": "I can do all things through Christ which strengtheneth me.",
            "Psalm 23:1": "The Lord is my shepherd; I shall not want.",
            "Psalm 46:10": "Be still, and know that I am God.",
            "Matthew 11:28": "Come unto me, all ye that labour and are heavy laden, and I will give you rest.",
            "Jeremiah 29:11": "For I know the thoughts that I think toward you, saith the Lord, thoughts of peace, and not of evil, to give you an expected end.",
            "Romans 5:8": "But God commendeth his love toward us, in that, while we were yet sinners, Christ died for us."
        }
    
    def generate_verse_understanding(self, verse_reference: str, verse_text: str) -> Dict:
        """
        Generate actual understanding for a single verse
        Returns real commentary, not an outline
        """
        # Find related verses using semantic similarity
        related_verses = self._find_related_verses(verse_text)
        
        # Discover themes
        themes = self._discover_themes(verse_text, related_verses)
        
        # Generate actual understanding content
        understanding = self._generate_understanding_content(
            verse_reference,
            verse_text,
            related_verses,
            themes
        )
        
        return {
            "verse_reference": verse_reference,
            "verse_text": verse_text,
            "understanding": understanding,
            "related_verses": related_verses[:5],  # Top 5
            "themes": themes,
            "generated_at": datetime.now().isoformat()
        }
    
    def _find_related_verses(self, verse_text: str, top_k: int = 10) -> List[Tuple[str, str, float]]:
        """Find semantically related verses"""
        all_verses = [(ref, text) for ref, text in self.sample_verses.items()]
        verse_texts = [text for _, text in all_verses]
        
        similar = self.kernel.find_similar(verse_text, verse_texts, top_k=top_k)
        
        # Map back to references
        results = []
        for similar_text, similarity in similar:
            for ref, text in all_verses:
                if text == similar_text:
                    results.append((ref, text, similarity))
                    break
        
        return results
    
    def _discover_themes(self, verse_text: str, related_verses: List[Tuple[str, str, float]]) -> List[str]:
        """Discover themes in the verse and related verses"""
        all_texts = [verse_text] + [text for _, text, _ in related_verses[:5]]
        themes = self.kernel.discover_themes(all_texts, min_cluster_size=2)
        
        return [theme["theme"] for theme in themes]
    
    def _generate_understanding_content(self, verse_ref: str, verse_text: str,
                                      related_verses: List[Tuple[str, str, float]],
                                      themes: List[str]) -> str:
        """
        Generate actual, readable understanding content
        This is the key - generates real commentary, not outlines
        """
        # Build context from related verses
        related_context = "\n".join([
            f"{ref}: {text[:100]}..." if len(text) > 100 else f"{ref}: {text}"
            for ref, text, _ in related_verses[:3]
        ])
        
        # Build understanding prompt
        understanding_parts = []
        
        # 1. Direct explanation
        understanding_parts.append(f"## Understanding {verse_ref}\n\n")
        understanding_parts.append(f"**The Verse:**\n\n{verse_text}\n\n")
        
        # 2. What it means
        understanding_parts.append("**What This Means:**\n\n")
        meaning = self._explain_meaning(verse_text, themes)
        understanding_parts.append(meaning)
        understanding_parts.append("\n\n")
        
        # 3. How it connects
        if related_verses:
            understanding_parts.append("**How This Connects:**\n\n")
            understanding_parts.append("This verse connects to the broader biblical narrative through several key relationships:\n\n")
            for ref, text, similarity in related_verses[:3]:
                connection = self._explain_connection(verse_text, text, similarity)
                understanding_parts.append(f"- **{ref}**: {connection}\n\n")
        
        # 4. Themes
        if themes:
            understanding_parts.append("**Themes in This Verse:**\n\n")
            for theme in themes:
                theme_explanation = self._explain_theme(theme, verse_text)
                understanding_parts.append(f"- **{theme}**: {theme_explanation}\n\n")
        
        # 5. Practical application
        understanding_parts.append("**What This Means for You:**\n\n")
        application = self._explain_application(verse_text, themes)
        understanding_parts.append(application)
        
        return "".join(understanding_parts)
    
    def _explain_meaning(self, verse_text: str, themes: List[str]) -> str:
        """Explain what the verse means - generates actual thoughtful content"""
        verse_lower = verse_text.lower()
        
        # Build thoughtful explanation based on verse content
        explanation_parts = []
        
        # Love theme
        if 'love' in verse_lower and 'god' in verse_lower:
            explanation_parts.append(
                "This verse reveals the heart of God's love - not as a distant concept, "
                "but as a reality that moved Him to action. God's love is not passive or "
                "theoretical; it is active, sacrificial, and personal. When we read that "
                "God 'so loved the world,' we see love measured not by words but by what "
                "it cost - the giving of His only Son."
            )
        elif 'love' in verse_lower:
            explanation_parts.append(
                "Love is central to this verse, but not love as the world defines it. "
                "This is divine love - unconditional, sacrificial, and transformative. "
                "It is love that sees our need and meets it, love that knows our brokenness "
                "and heals it, love that understands our distance and bridges it."
            )
        
        # Trust/Faith theme
        if 'trust' in verse_lower or 'faith' in verse_lower or 'believe' in verse_lower:
            explanation_parts.append(
                "This verse calls us to trust - not in our own understanding or abilities, "
                "but in God Himself. Trust is not blind faith, but confidence in the character "
                "of the One who is trustworthy. It is not about having all the answers, but "
                "about knowing the One who does."
            )
        
        # Peace/Rest theme
        if 'peace' in verse_lower or 'rest' in verse_lower:
            explanation_parts.append(
                "Here we find an invitation to peace and rest - not the absence of trouble, "
                "but the presence of God in the midst of it. This peace is not something we "
                "achieve, but something we receive. It comes not from changed circumstances, "
                "but from knowing the One who is with us in all circumstances."
            )
        
        # Strength/Power theme
        if 'strength' in verse_lower or 'power' in verse_lower or 'can do' in verse_lower:
            explanation_parts.append(
                "This verse speaks of strength, but not strength that comes from within. "
                "It is strength that comes from Christ - strength that is made perfect in "
                "weakness, power that flows from relationship, ability that comes from "
                "abiding in the One who is the source of all strength."
            )
        
        # Life theme
        if 'life' in verse_lower and ('eternal' in verse_lower or 'everlasting' in verse_lower):
            explanation_parts.append(
                "Life is the gift offered here - not just existence, but life in its fullest "
                "sense. This is eternal life, which begins not when we die, but when we believe. "
                "It is life that is abundant, meaningful, and connected to the source of all life."
            )
        
        # Shepherd theme
        if 'shepherd' in verse_lower or 'want' in verse_lower:
            explanation_parts.append(
                "The image of shepherd speaks to God's care and provision. A shepherd knows "
                "each sheep, leads them to good pasture, protects them from danger, and seeks "
                "them when they wander. This is how God cares for us - personally, completely, "
                "and faithfully."
            )
        
        # Default explanation if no specific theme matched
        if not explanation_parts:
            explanation_parts.append(
                "This verse reveals truth about who God is and how He relates to us. "
                "It is not just information to know, but truth that transforms. The words "
                "here invite us into deeper understanding and relationship - to know God "
                "more fully, to trust Him more completely, and to experience His presence "
                "more deeply in our daily lives."
            )
        
        return " ".join(explanation_parts)
    
    def _explain_connection(self, verse1: str, verse2: str, similarity: float) -> str:
        """Explain how two verses connect"""
        # Find common themes
        common_words = set(verse1.lower().split()) & set(verse2.lower().split())
        significant_words = [w for w in common_words if len(w) > 4]
        
        if significant_words:
            connection = f"Both verses explore {', '.join(significant_words[:2])}, showing how this theme runs throughout Scripture. "
        else:
            connection = "These verses connect through their shared message about God's character and our relationship with Him. "
        
        if similarity > 0.8:
            connection += "The connection is very strong - they speak to the same truth from different angles."
        elif similarity > 0.6:
            connection += "They complement each other, each adding depth to our understanding."
        else:
            connection += "They relate through underlying themes that connect the biblical narrative."
        
        return connection
    
    def _explain_theme(self, theme: str, verse_text: str) -> str:
        """Explain how a theme appears in the verse"""
        theme_lower = theme.lower()
        verse_lower = verse_text.lower()
        
        if theme_lower in verse_lower:
            return f"This verse directly addresses {theme}, showing how it is central to understanding God's relationship with us."
        else:
            return f"While not explicitly mentioned, {theme} underlies this verse's message, connecting it to the broader biblical narrative."
    
    def _explain_application(self, verse_text: str, themes: List[str]) -> str:
        """Explain practical application"""
        application = "This verse is not just information to know, but truth to live. "
        
        if 'love' in verse_text.lower():
            application += "God's love calls for a response - to receive it, to rest in it, and to share it with others. "
        if 'trust' in verse_text.lower():
            application += "Trust is not passive - it's an active choice to lean on God rather than our own understanding. "
        if 'peace' in verse_text.lower() or 'rest' in verse_text.lower():
            application += "The peace and rest offered here are available now, not just in the future - they come from knowing God is with us. "
        if 'strength' in verse_text.lower():
            application += "When we feel weak, this verse reminds us that Christ's strength is available to us in every moment. "
        
        application += "As you reflect on this verse, consider: How does this truth change how you see God? How does it change how you see yourself? How does it change how you live today?"
        
        return application
    
    def generate_passage_understanding(self, passage_reference: str, verses: List[Tuple[str, str]]) -> Dict:
        """
        Generate understanding for a passage (multiple verses)
        """
        passage_text = " ".join([text for _, text in verses])
        
        # Generate understanding for each verse
        verse_understandings = []
        for ref, text in verses:
            verse_understanding = self.generate_verse_understanding(ref, text)
            verse_understandings.append(verse_understanding)
        
        # Generate overall passage understanding
        passage_understanding = self._generate_passage_overview(passage_reference, verses, verse_understandings)
        
        return {
            "passage_reference": passage_reference,
            "verses": verses,
            "passage_understanding": passage_understanding,
            "verse_understandings": verse_understandings,
            "generated_at": datetime.now().isoformat()
        }
    
    def _generate_passage_overview(self, passage_ref: str, verses: List[Tuple[str, str]],
                                  verse_understandings: List[Dict]) -> str:
        """Generate overview understanding for a passage"""
        overview = f"## Understanding {passage_ref}\n\n"
        overview += f"This passage contains {len(verses)} verses that together form a complete thought or teaching.\n\n"
        
        # Extract themes across all verses
        all_themes = []
        for v_understanding in verse_understandings:
            all_themes.extend(v_understanding.get("themes", []))
        
        unique_themes = list(set(all_themes))
        if unique_themes:
            overview += f"**Key Themes:** {', '.join(unique_themes)}\n\n"
        
        overview += "**The Passage:**\n\n"
        for ref, text in verses:
            overview += f"{ref}: {text}\n\n"
        
        overview += "**Understanding the Whole:**\n\n"
        overview += "When we read these verses together, we see how they build on each other to reveal a deeper truth. "
        overview += "Each verse contributes to the whole, and the whole is greater than the sum of its parts. "
        overview += "This passage invites us not just to understand individual verses, but to see how they connect to form a complete picture of God's truth.\n\n"
        
        overview += "**How to Read This Passage:**\n\n"
        overview += "1. Read the passage slowly, letting each verse sink in.\n"
        overview += "2. Notice how the verses connect - what does each add to the others?\n"
        overview += "3. Look for the main idea - what is the passage as a whole saying?\n"
        overview += "4. Consider the context - how does this passage fit into the book and the Bible as a whole?\n"
        overview += "5. Apply it personally - what does this mean for your relationship with God?\n"
        
        return overview


class UnderstandingLibrary:
    """
    Library to store and organize understanding content
    """
    
    def __init__(self, library_path: str = "understanding_library"):
        self.library_path = Path(library_path)
        self.library_path.mkdir(exist_ok=True)
        
        self.verses_path = self.library_path / "verses"
        self.passages_path = self.library_path / "passages"
        self.topics_path = self.library_path / "topics"
        
        for path in [self.verses_path, self.passages_path, self.topics_path]:
            path.mkdir(exist_ok=True)
        
        self.metadata_file = self.library_path / "library_metadata.json"
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load library metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "verses": {},
            "passages": {},
            "topics": {},
            "total_entries": 0,
            "last_updated": None
        }
    
    def _save_metadata(self):
        """Save library metadata"""
        self.metadata["last_updated"] = datetime.now().isoformat()
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)
    
    def add_verse_understanding(self, understanding: Dict):
        """Add verse understanding to library"""
        verse_ref = understanding["verse_reference"]
        safe_ref = self._safe_filename(verse_ref)
        
        # Save understanding
        verse_file = self.verses_path / f"{safe_ref}.json"
        with open(verse_file, 'w', encoding='utf-8') as f:
            json.dump(understanding, f, indent=2, ensure_ascii=False)
        
        # Save readable markdown
        md_file = self.verses_path / f"{safe_ref}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(understanding["understanding"])
        
        # Update metadata
        self.metadata["verses"][verse_ref] = {
            "file": str(verse_file),
            "md_file": str(md_file),
            "generated_at": understanding["generated_at"],
            "themes": understanding.get("themes", [])
        }
        self.metadata["total_entries"] = len(self.metadata["verses"]) + len(self.metadata["passages"])
        self._save_metadata()
    
    def add_passage_understanding(self, understanding: Dict):
        """Add passage understanding to library"""
        passage_ref = understanding["passage_reference"]
        safe_ref = self._safe_filename(passage_ref)
        
        # Save understanding
        passage_file = self.passages_path / f"{safe_ref}.json"
        with open(passage_file, 'w', encoding='utf-8') as f:
            json.dump(understanding, f, indent=2, ensure_ascii=False)
        
        # Save readable markdown
        md_file = self.passages_path / f"{safe_ref}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(understanding["passage_understanding"])
        
        # Update metadata
        self.metadata["passages"][passage_ref] = {
            "file": str(passage_file),
            "md_file": str(md_file),
            "generated_at": understanding["generated_at"],
            "verse_count": len(understanding["verses"])
        }
        self.metadata["total_entries"] = len(self.metadata["verses"]) + len(self.metadata["passages"])
        self._save_metadata()
    
    def get_verse_understanding(self, verse_ref: str) -> Optional[Dict]:
        """Get verse understanding from library"""
        if verse_ref in self.metadata["verses"]:
            file_path = self.metadata["verses"][verse_ref]["file"]
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def get_passage_understanding(self, passage_ref: str) -> Optional[Dict]:
        """Get passage understanding from library"""
        if passage_ref in self.metadata["passages"]:
            file_path = self.metadata["passages"][passage_ref]["file"]
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def list_all_verses(self) -> List[str]:
        """List all verse references in library"""
        return list(self.metadata["verses"].keys())
    
    def list_all_passages(self) -> List[str]:
        """List all passage references in library"""
        return list(self.metadata["passages"].keys())
    
    def search_by_theme(self, theme: str) -> List[Dict]:
        """Search for verses/passages by theme"""
        results = []
        
        for verse_ref, data in self.metadata["verses"].items():
            if theme.lower() in " ".join(data.get("themes", [])).lower():
                understanding = self.get_verse_understanding(verse_ref)
                if understanding:
                    results.append(understanding)
        
        return results
    
    def _safe_filename(self, text: str) -> str:
        """Convert text to safe filename"""
        # Replace invalid characters
        safe = re.sub(r'[<>:"/\\|?*]', '_', text)
        safe = safe.replace(' ', '_')
        return safe
    
    def get_stats(self) -> Dict:
        """Get library statistics"""
        return {
            "total_verses": len(self.metadata["verses"]),
            "total_passages": len(self.metadata["passages"]),
            "total_entries": self.metadata["total_entries"],
            "last_updated": self.metadata["last_updated"]
        }


# Example usage
if __name__ == "__main__":
    print("Building Bible Understanding Library...")
    print("=" * 80)
    
    # Initialize
    generator = UnderstandingGenerator()
    library = UnderstandingLibrary()
    
    # Generate understanding for sample verses
    print("\nGenerating understanding for sample verses...")
    
    for verse_ref, verse_text in generator.sample_verses.items():
        print(f"\nGenerating understanding for {verse_ref}...")
        understanding = generator.generate_verse_understanding(verse_ref, verse_text)
        library.add_verse_understanding(understanding)
        print(f"  [OK] Added to library")
    
    # Show stats
    stats = library.get_stats()
    print(f"\n{'='*80}")
    print("Library Statistics:")
    print(f"  Total verses: {stats['total_verses']}")
    print(f"  Total passages: {stats['total_passages']}")
    print(f"  Total entries: {stats['total_entries']}")
    print(f"  Last updated: {stats['last_updated']}")
    print(f"\n{'='*80}")
    print("\nLibrary created! Check the 'understanding_library' folder for:")
    print("  - Verse understandings (JSON + Markdown)")
    print("  - Readable content (not outlines!)")
    print("  - Actual commentary and insights")
    print("\nThis is real content you can read and learn from!")