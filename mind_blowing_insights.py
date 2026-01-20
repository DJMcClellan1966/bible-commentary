"""
Mind-Blowing Bible Insights
Combines multiple perspectives to reveal the depth and richness of Scripture
Shows how great thinkers, cross-references, and AI analysis reveal layers of meaning
"""
import os
import json
import re
from typing import List, Dict, Optional
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from understanding_bible import UnderstandingBible, THEOLOGICAL_TRADITIONS
from load_bible_from_html import load_all_versions_into_app


class MindBlowingInsights:
    """
    Reveals the depth of Scripture by combining:
    - Multiple theological perspectives
    - Deep cross-references
    - Semantic connections
    - Historical context
    - Layers of meaning
    """
    
    def __init__(self):
        print("Initializing Mind-Blowing Insights Generator...")
        
        # Initialize Bible app
        self.app = HyperlinkedBibleApp()
        
        # Load Bible if needed
        if not self.app.versions.get('asv'):
            print("Loading Bible...")
            bible_path = r"C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions"
            if os.path.exists(bible_path):
                load_all_versions_into_app(self.app, bible_path)
        
        # Initialize Understanding Bible
        try:
            self.understanding = UnderstandingBible()
        except:
            self.understanding = None
            print("Warning: Understanding Bible not available")
    
    def _parse_ref(self, ref: str):
        """Parse verse reference"""
        if '-' in ref:
            ref = ref.split('-')[0]
        match = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
        if match:
            return match.group(1).strip(), int(match.group(2)), int(match.group(3))
        return None, 0, 0
    
    def _get_verse_text(self, ref: str):
        """Get verse text from all versions"""
        book, chapter, verse = self._parse_ref(ref)
        if not book:
            return {}
        
        versions = {}
        for version in ['asv', 'engDBY', 'englyt']:
            text = self.app.get_verse_text(book, chapter, verse, version=version)
            if text:
                versions[version] = text
        
        return versions
    
    def _get_deep_cross_refs(self, ref: str, top_k=10):
        """Get deep cross-references with analysis"""
        book, chapter, verse = self._parse_ref(ref)
        if not book:
            return []
        
        try:
            result = self.app.discover_cross_references(book, chapter, verse, top_k=top_k)
            cross_refs = result.get('cross_references', [])
            
            # Filter for high-quality connections
            quality_refs = [cr for cr in cross_refs if cr.get('similarity', 0) > 0.7]
            
            # Group by relationship type
            grouped = {}
            for cr in quality_refs:
                rel_type = cr.get('relationship_type', 'general')
                if rel_type not in grouped:
                    grouped[rel_type] = []
                grouped[rel_type].append(cr)
            
            return grouped
        except:
            return {}
    
    def _find_thematic_connections(self, verse_text: str, top_k=5):
        """Find verses with similar themes across the Bible"""
        try:
            # Use semantic search to find thematic connections
            all_verses = []
            for version_data in self.app.versions.values():
                all_verses.extend(list(version_data.values())[:1000])
            
            results = self.app.kernel.find_similar(verse_text, all_verses, top_k=top_k)
            
            connections = []
            for verse_text_found, similarity in results:
                # Find the reference
                for ref, text in self.app.versions.get('asv', {}).items():
                    if text == verse_text_found:
                        connections.append({
                            "reference": ref,
                            "text": text,
                            "thematic_similarity": float(similarity)
                        })
                        break
            
            return connections
        except:
            return []
    
    def generate_mind_blowing_insight(self, book: str, chapter: int, verse: int,
                                     thinkers: List[str] = None) -> Dict:
        """
        Generate a mind-blowing insight that combines multiple perspectives
        to reveal the depth of a single verse
        """
        print(f"\n{'='*80}")
        print(f"GENERATING MIND-BLOWING INSIGHT")
        print(f"Verse: {book} {chapter}:{verse}")
        print(f"{'='*80}\n")
        
        verse_ref = f"{book} {chapter}:{verse}"
        
        # Get verse text from all versions
        print("1. Gathering verse text from multiple versions...")
        verse_texts = self._get_verse_text(verse_ref)
        if not verse_texts:
            return {"error": f"Verse {verse_ref} not found"}
        
        asv_text = verse_texts.get('asv', '')
        
        # Get theological insights from great thinkers
        print("2. Gathering insights from great theological thinkers...")
        theological_insights = []
        if self.understanding:
            try:
                understanding = self.understanding.get_understanding(
                    book, chapter, verse,
                    thinkers or ['Keller', 'Benedict', 'Aquinas', 'Lewis']
                )
                theological_insights = understanding.get('thinkers', [])
                synthesis = understanding.get('synthesis', {})
            except:
                synthesis = {}
        else:
            synthesis = {}
        
        # Get deep cross-references
        print("3. Finding deep cross-references throughout Scripture...")
        cross_refs_grouped = self._get_deep_cross_refs(verse_ref, top_k=15)
        
        # Find thematic connections
        print("4. Discovering thematic connections across the Bible...")
        thematic_connections = self._find_thematic_connections(asv_text, top_k=5)
        
        # Analyze layers of meaning
        print("5. Analyzing layers of meaning...")
        layers = self._analyze_layers(asv_text, verse_ref, cross_refs_grouped)
        
        # Create synthesis
        print("6. Synthesizing insights...")
        mind_blowing_synthesis = self._create_mind_blowing_synthesis(
            verse_ref, asv_text, theological_insights, cross_refs_grouped,
            thematic_connections, layers
        )
        
        return {
            "verse": verse_ref,
            "verse_text": {
                "asv": asv_text,
                "all_versions": verse_texts
            },
            "theological_insights": theological_insights,
            "synthesis": synthesis,
            "cross_references": cross_refs_grouped,
            "thematic_connections": thematic_connections,
            "layers_of_meaning": layers,
            "mind_blowing_synthesis": mind_blowing_synthesis,
            "generated_at": datetime.now().isoformat()
        }
    
    def _analyze_layers(self, verse_text: str, verse_ref: str, cross_refs: Dict) -> List[Dict]:
        """Analyze different layers of meaning"""
        layers = []
        
        # Layer 1: Literal meaning
        layers.append({
            "layer": "Literal",
            "description": "What the verse says directly",
            "insight": f"This verse directly states: {verse_text[:100]}..."
        })
        
        # Layer 2: Historical context
        layers.append({
            "layer": "Historical",
            "description": "What it meant in its original context",
            "insight": f"In its historical context, this verse would have been understood in light of the biblical narrative up to that point."
        })
        
        # Layer 3: Theological depth
        layers.append({
            "layer": "Theological",
            "description": "What it reveals about God and His nature",
            "insight": "This verse reveals something profound about God's character, His plan, or His relationship with humanity."
        })
        
        # Layer 4: Cross-referential connections
        if cross_refs:
            total_connections = sum(len(refs) for refs in cross_refs.values())
            layers.append({
                "layer": "Connections",
                "description": "How it connects to other parts of Scripture",
                "insight": f"This verse connects to {total_connections} other verses throughout Scripture, showing it's part of a larger narrative."
            })
        
        # Layer 5: Practical application
        layers.append({
            "layer": "Application",
            "description": "What it means for us today",
            "insight": "This verse is not just ancient text but living truth that transforms how we see God, ourselves, and our purpose."
        })
        
        return layers
    
    def _create_mind_blowing_synthesis(self, verse_ref: str, verse_text: str,
                                      theological_insights: List[Dict],
                                      cross_refs: Dict,
                                      thematic_connections: List[Dict],
                                      layers: List[Dict]) -> str:
        """Create a synthesis that reveals the depth"""
        
        synthesis = f"# Mind-Blowing Insight: {verse_ref}\n\n"
        synthesis += f"**{verse_text}**\n\n"
        synthesis += "---\n\n"
        
        synthesis += "## The Depth Revealed\n\n"
        synthesis += f"When we examine {verse_ref} through multiple lenses, we discover that this single verse contains "
        synthesis += f"layers of meaning that reveal the depth and richness of Scripture. What appears to be a simple "
        synthesis += f"statement is actually a window into profound truth.\n\n"
        
        # Multiple perspectives
        if theological_insights:
            synthesis += "## Through the Eyes of Great Thinkers\n\n"
            synthesis += f"Great theological minds have found deep meaning in this verse:\n\n"
            
            for insight in theological_insights[:3]:
                thinker = insight.get('thinker', 'Unknown')
                tradition = insight.get('tradition', '')
                synthesis += f"**{thinker}** ({tradition}):\n"
                synthesis += f"{insight.get('insight', '')[:200]}...\n\n"
        
        # Cross-referential depth
        if cross_refs:
            synthesis += "## Connections Throughout Scripture\n\n"
            synthesis += f"This verse is not isolated but connected to the entire biblical narrative:\n\n"
            
            for rel_type, refs in list(cross_refs.items())[:3]:
                synthesis += f"**{rel_type.title()} Connections:**\n"
                for ref in refs[:3]:
                    synthesis += f"- {ref.get('reference', 'Unknown')}: {ref.get('summary', ref.get('text', ''))[:80]}...\n"
                synthesis += "\n"
        
        # Thematic connections
        if thematic_connections:
            synthesis += "## Thematic Echoes\n\n"
            synthesis += f"Similar themes echo throughout Scripture:\n\n"
            for conn in thematic_connections[:3]:
                synthesis += f"- **{conn['reference']}**: {conn['text'][:100]}...\n"
            synthesis += "\n"
        
        # Layers of meaning
        synthesis += "## Layers of Meaning\n\n"
        synthesis += f"This verse operates on multiple levels:\n\n"
        for layer in layers:
            synthesis += f"**{layer['layer']} Layer:** {layer['description']}\n"
            synthesis += f"{layer['insight']}\n\n"
        
        # The mind-blowing conclusion
        synthesis += "## Why This Blows Your Mind\n\n"
        synthesis += f"Here's what makes {verse_ref} mind-blowing:\n\n"
        synthesis += f"1. **Multiple Perspectives**: Great thinkers find different but complementary meanings\n"
        synthesis += f"2. **Deep Connections**: It's woven into the fabric of all Scripture\n"
        synthesis += f"3. **Layers of Truth**: It operates on literal, historical, theological, and practical levels\n"
        synthesis += f"4. **Living Word**: It's not just ancient text but truth that transforms\n"
        synthesis += f"5. **Infinite Depth**: The more you explore, the more you discover\n\n"
        
        synthesis += f"This single verse contains more meaning than we could discover in a lifetime. "
        synthesis += f"That's the depth of Scripture—every word is a window into infinite truth.\n\n"
        
        return synthesis
    
    def save_insight(self, insight: Dict, filename: str = None):
        """Save insight to file"""
        if filename is None:
            verse_ref = insight['verse'].replace(' ', '_').replace(':', '_')
            filename = f"mind_blowing_insights_{verse_ref}.md"
        
        output_dir = "mind_blowing_insights"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Save the synthesis
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(insight.get('mind_blowing_synthesis', ''))
        
        # Also save full JSON
        json_path = filepath.replace('.md', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(insight, f, indent=2, ensure_ascii=False)
        
        print(f"\nSaved: {filepath}")
        return filepath


def main():
    """Generate mind-blowing insights"""
    print("="*80)
    print("MIND-BLOWING BIBLE INSIGHTS")
    print("="*80)
    print()
    print("This combines:")
    print("  - Insights from great theological thinkers")
    print("  - Deep cross-references throughout Scripture")
    print("  - Thematic connections across the Bible")
    print("  - Layers of meaning (literal, historical, theological, practical)")
    print("  - Synthesis that reveals the depth")
    print()
    
    generator = MindBlowingInsights()
    
    # Generate insight for John 3:16
    print("Generating mind-blowing insight for John 3:16...")
    insight = generator.generate_mind_blowing_insight("John", 3, 16)
    
    if "error" not in insight:
        # Save it
        filepath = generator.save_insight(insight)
        
        print("\n" + "="*80)
        print("MIND-BLOWING INSIGHT GENERATED!")
        print("="*80)
        print(f"\nFile: {filepath}")
        print("\nThis insight reveals:")
        print("  - How great thinkers understand this verse")
        print("  - Deep connections throughout Scripture")
        print("  - Multiple layers of meaning")
        print("  - Why this verse is mind-blowing")
        print("\nOpen the file to see the full insight!")
    else:
        print(f"Error: {insight['error']}")


if __name__ == "__main__":
    main()