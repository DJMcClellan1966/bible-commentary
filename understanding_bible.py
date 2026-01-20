"""
Understanding Bible - Deep Theological Insights
Incorporates insights from great thinkers: Aquinas, Pope Benedict, Tim Keller, etc.
Helps you understand Scripture through the eyes of theological giants
"""
import os
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from quantum_llm_standalone import StandaloneQuantumLLM


# Great theological thinkers and their approaches
THEOLOGICAL_TRADITIONS = {
    "Aquinas": {
        "name": "Thomas Aquinas",
        "tradition": "Scholastic Theology",
        "approach": "Systematic, philosophical, logical analysis",
        "focus": "Reason and faith, systematic theology, natural law",
        "key_themes": ["divine simplicity", "analogy of being", "natural theology", "virtue ethics"]
    },
    "Benedict": {
        "name": "Pope Benedict XVI",
        "tradition": "Catholic Theology",
        "approach": "Historical-critical with deep spiritual insight",
        "focus": "Jesus of Nazareth, love, beauty, truth",
        "key_themes": ["divine love", "incarnation", "church", "liturgy"]
    },
    "Keller": {
        "name": "Tim Keller",
        "tradition": "Reformed Evangelical",
        "approach": "Gospel-centered, culturally engaged",
        "focus": "Gospel, grace, city ministry, apologetics",
        "key_themes": ["gospel", "grace", "idolatry", "justice"]
    },
    "Augustine": {
        "name": "Augustine of Hippo",
        "tradition": "Patristic Theology",
        "approach": "Neo-Platonic, deeply personal",
        "focus": "Grace, predestination, love, city of God",
        "key_themes": ["grace", "love", "will", "time and eternity"]
    },
    "Luther": {
        "name": "Martin Luther",
        "tradition": "Protestant Reformation",
        "approach": "Sola Scriptura, law and gospel",
        "focus": "Justification by faith, priesthood of believers",
        "key_themes": ["faith", "grace", "law and gospel", "freedom"]
    },
    "Calvin": {
        "name": "John Calvin",
        "tradition": "Reformed Theology",
        "approach": "Systematic, God-centered",
        "focus": "Sovereignty of God, predestination, covenant",
        "key_themes": ["sovereignty", "election", "covenant", "glory of God"]
    },
    "Lewis": {
        "name": "C.S. Lewis",
        "tradition": "Anglican Apologetics",
        "approach": "Literary, imaginative, accessible",
        "focus": "Mere Christianity, love, suffering, joy",
        "key_themes": ["love", "suffering", "imagination", "joy"]
    },
    "Bonhoeffer": {
        "name": "Dietrich Bonhoeffer",
        "tradition": "Lutheran Theology",
        "approach": "Costly discipleship, ethics",
        "focus": "Discipleship, community, suffering, grace",
        "key_themes": ["discipleship", "costly grace", "community", "ethics"]
    },
    "Barth": {
        "name": "Karl Barth",
        "tradition": "Neo-Orthodox",
        "approach": "Christocentric, dialectical",
        "focus": "Word of God, revelation, election",
        "key_themes": ["revelation", "election", "christology", "word of God"]
    },
    "Wright": {
        "name": "N.T. Wright",
        "tradition": "New Testament Scholarship",
        "approach": "Historical, narrative, kingdom-focused",
        "focus": "New perspective on Paul, resurrection, kingdom",
        "key_themes": ["resurrection", "kingdom", "covenant", "new creation"]
    }
}


class UnderstandingBible:
    """
    Understanding Bible - Deep theological insights from great thinkers
    Helps you see Scripture through the eyes of theological giants
    """
    
    def __init__(self):
        """Initialize the Understanding Bible"""
        print("Initializing Understanding Bible...")
        
        self.app = HyperlinkedBibleApp()
        self.llm = StandaloneQuantumLLM(
            kernel=self.app.kernel,
            source_texts=list(self.app.versions.get('asv', {}).values())[:100] if self.app.versions else ["God is love"]
        )
        
        self.insights_file = "theological_insights.json"
        self.insights = self._load_insights()
    
    def _load_insights(self) -> Dict:
        """Load saved theological insights"""
        if os.path.exists(self.insights_file):
            try:
                with open(self.insights_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def _save_insights(self):
        """Save theological insights"""
        with open(self.insights_file, 'w', encoding='utf-8') as f:
            json.dump(self.insights, f, indent=2)
    
    def _parse_reference(self, ref: str) -> Tuple[str, int, int]:
        """Parse verse reference"""
        import re
        match = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
        if match:
            book = match.group(1).strip()
            chapter = int(match.group(2))
            verse = int(match.group(3))
            return book, chapter, verse
        return None, 0, 0
    
    def get_understanding(self, book: str, chapter: int, verse: int,
                         thinkers: List[str] = None) -> Dict:
        """
        Get deep understanding of a verse from multiple theological perspectives
        
        Args:
            book: Book name
            chapter: Chapter number
            verse: Verse number
            thinkers: List of thinkers to include (default: all)
        """
        verse_ref = f"{book} {chapter}:{verse}"
        verse_text = self.app.get_verse_text(book, chapter, verse)
        
        if not verse_text:
            return {"error": f"Verse {verse_ref} not found"}
        
        # Check cache
        cache_key = f"{verse_ref}:{','.join(sorted(thinkers or []))}"
        if cache_key in self.insights:
            return self.insights[cache_key]
        
        # Get thinkers to use
        thinkers_to_use = thinkers or list(THEOLOGICAL_TRADITIONS.keys())
        
        # Get cross-references for context
        cross_refs = self.app.discover_cross_references(book, chapter, verse, top_k=5)
        
        # Generate insights from each thinker
        theological_insights = []
        
        for thinker_key in thinkers_to_use:
            if thinker_key in THEOLOGICAL_TRADITIONS:
                insight = self._generate_thinker_insight(
                    verse_ref, verse_text, thinker_key, cross_refs
                )
                theological_insights.append(insight)
        
        # Generate synthesis
        synthesis = self._generate_synthesis(verse_ref, verse_text, theological_insights)
        
        result = {
            "verse": verse_ref,
            "verse_text": verse_text,
            "thinkers": theological_insights,
            "synthesis": synthesis,
            "cross_references": cross_refs.get("cross_references", [])[:3],
            "generated_at": datetime.now().isoformat()
        }
        
        # Cache result
        self.insights[cache_key] = result
        self._save_insights()
        
        return result
    
    def _generate_thinker_insight(self, verse_ref: str, verse_text: str,
                                 thinker_key: str, cross_refs: Dict) -> Dict:
        """Generate insight from a specific theological thinker"""
        thinker = THEOLOGICAL_TRADITIONS[thinker_key]
        
        print(f"  Generating insight from {thinker['name']}...")
        
        # Build context
        context_verses = "\n".join([
            f"{cr['reference']}: {cr['text']}" 
            for cr in cross_refs.get("cross_references", [])[:3]
        ])
        
        prompt = f"""Write a deep theological insight about this Bible verse from the perspective of {thinker['name']}.

Verse: {verse_ref}
Text: {verse_text}

Context (related verses):
{context_verses}

{thinker['name']}'s Approach:
- Tradition: {thinker['tradition']}
- Approach: {thinker['approach']}
- Focus: {thinker['focus']}
- Key Themes: {', '.join(thinker['key_themes'])}

Write as {thinker['name']} would understand this verse:
1. What deep meaning does {thinker['name']} find here?
2. How does this connect to {thinker['name']}'s key themes?
3. What theological insights does {thinker['name']} offer?
4. How does this reveal God's character or plan?

Write in {thinker['name']}'s style - deep, thoughtful, profound.
2-3 paragraphs. Focus on the deep meaning that {thinker['name']} would find."""
        
        try:
            result = self.llm.generate_grounded(
                prompt,
                max_length=400,
                require_validation=True
            )
            
            insight_text = result.get('generated', self._default_insight(thinker, verse_text))
            
            return {
                "thinker": thinker['name'],
                "tradition": thinker['tradition'],
                "approach": thinker['approach'],
                "insight": insight_text,
                "key_themes": thinker['key_themes']
            }
        except Exception as e:
            print(f"    Error: {e}")
            return {
                "thinker": thinker['name'],
                "tradition": thinker['tradition'],
                "approach": thinker['approach'],
                "insight": self._default_insight(thinker, verse_text),
                "key_themes": thinker['key_themes']
            }
    
    def _default_insight(self, thinker: Dict, verse_text: str) -> str:
        """Default insight if generation fails"""
        return f"{thinker['name']} would find deep meaning in this verse, connecting it to {thinker['focus']}. Through {thinker['approach']}, this verse reveals profound truths about God and our relationship with Him."
    
    def _generate_synthesis(self, verse_ref: str, verse_text: str,
                           insights: List[Dict]) -> Dict:
        """Generate a synthesis of all insights"""
        if not insights:
            return {"text": "No insights available", "themes": []}
        
        thinkers_list = ", ".join([i['thinker'] for i in insights])
        
        prompt = f"""Synthesize the theological insights from these great thinkers about this verse.

Verse: {verse_ref}
Text: {verse_text}

Thinkers: {thinkers_list}

Their insights show different but complementary perspectives. Write a synthesis that:
1. Shows how these perspectives complement each other
2. Reveals the deeper meaning that emerges
3. Highlights what makes this verse profound
4. Connects the insights to show the richness of Scripture

2-3 paragraphs. Show how great minds find deep meaning here."""
        
        try:
            result = self.llm.generate_grounded(
                prompt,
                max_length=300,
                require_validation=True
            )
            
            synthesis_text = result.get('generated', self._default_synthesis(insights))
            
            # Extract common themes
            all_themes = []
            for insight in insights:
                all_themes.extend(insight.get('key_themes', []))
            
            common_themes = list(set(all_themes))[:5]
            
            return {
                "text": synthesis_text,
                "themes": common_themes,
                "thinkers_count": len(insights)
            }
        except:
            return {
                "text": self._default_synthesis(insights),
                "themes": [],
                "thinkers_count": len(insights)
            }
    
    def _default_synthesis(self, insights: List[Dict]) -> str:
        """Default synthesis"""
        if not insights:
            return "Multiple perspectives reveal the depth of this verse."
        
        thinkers = ", ".join([i['thinker'] for i in insights[:3]])
        return f"The insights from {thinkers} show how this verse contains profound meaning that can be understood from multiple perspectives, each revealing different aspects of God's truth."
    
    def compare_thinkers(self, book: str, chapter: int, verse: int,
                        thinker1: str, thinker2: str) -> Dict:
        """Compare how two thinkers understand the same verse"""
        understanding = self.get_understanding(book, chapter, verse, [thinker1, thinker2])
        
        insights = understanding.get("thinkers", [])
        insight1 = next((i for i in insights if i['thinker'] == THEOLOGICAL_TRADITIONS[thinker1]['name']), None)
        insight2 = next((i for i in insights if i['thinker'] == THEOLOGICAL_TRADITIONS[thinker2]['name']), None)
        
        # Generate comparison
        comparison = self._generate_comparison(insight1, insight2, understanding['verse_text'])
        
        return {
            "verse": understanding['verse'],
            "verse_text": understanding['verse_text'],
            "thinker1": insight1,
            "thinker2": insight2,
            "comparison": comparison
        }
    
    def _generate_comparison(self, insight1: Dict, insight2: Dict, verse_text: str) -> str:
        """Generate comparison between two insights"""
        if not insight1 or not insight2:
            return "Comparison not available"
        
        prompt = f"""Compare how {insight1['thinker']} and {insight2['thinker']} understand this verse.

Verse: {verse_text}

{insight1['thinker']}'s Understanding:
{insight1['insight']}

{insight2['thinker']}'s Understanding:
{insight2['insight']}

Write a comparison that:
1. Shows what they agree on
2. Highlights their different perspectives
3. Shows how both add to understanding
4. Reveals the richness of multiple perspectives

2-3 paragraphs."""
        
        try:
            result = self.llm.generate_grounded(prompt, max_length=300, require_validation=True)
            return result.get('generated', self._default_comparison(insight1, insight2))
        except:
            return self._default_comparison(insight1, insight2)
    
    def _default_comparison(self, insight1: Dict, insight2: Dict) -> str:
        """Default comparison"""
        return f"{insight1['thinker']} and {insight2['thinker']} approach this verse from different traditions ({insight1['tradition']} vs {insight2['tradition']}), yet both find profound meaning. Their insights complement each other, showing the richness of Scripture."
    
    def explore_theme(self, theme: str, thinkers: List[str] = None) -> Dict:
        """Explore how different thinkers understand a theological theme"""
        thinkers_to_use = thinkers or list(THEOLOGICAL_TRADITIONS.keys())
        
        relevant_thinkers = []
        for thinker_key in thinkers_to_use:
            if thinker_key in THEOLOGICAL_TRADITIONS:
                thinker = THEOLOGICAL_TRADITIONS[thinker_key]
                if theme.lower() in ' '.join(thinker['key_themes']).lower():
                    relevant_thinkers.append(thinker)
        
        # Find verses related to theme
        try:
            results = self.app.kernel.find_similar(
                theme,
                list(self.app.versions.get('asv', {}).values())[:500] if self.app.versions else [],
                top_k=5
            )
            
            verses = []
            for verse_text, similarity in results:
                # Find reference
                for ref, text in self.app.versions.get('asv', {}).items():
                    if text == verse_text:
                        verses.append({
                            "reference": ref,
                            "text": text,
                            "relevance": float(similarity)
                        })
                        break
        except:
            verses = []
        
        return {
            "theme": theme,
            "relevant_thinkers": relevant_thinkers,
            "key_verses": verses,
            "message": f"Explore how {len(relevant_thinkers)} thinkers understand '{theme}'"
        }
    
    def get_thinker_profile(self, thinker_key: str) -> Dict:
        """Get profile of a theological thinker"""
        if thinker_key not in THEOLOGICAL_TRADITIONS:
            return {"error": "Thinker not found"}
        
        thinker = THEOLOGICAL_TRADITIONS[thinker_key]
        
        # Find verses they might focus on
        key_verses = []
        for theme in thinker['key_themes'][:3]:
            try:
                results = self.app.kernel.find_similar(
                    theme,
                    list(self.app.versions.get('asv', {}).values())[:200] if self.app.versions else [],
                    top_k=2
                )
                for verse_text, _ in results:
                    for ref, text in self.app.versions.get('asv', {}).items():
                        if text == verse_text:
                            key_verses.append({"reference": ref, "text": text})
                            break
            except:
                pass
        
        return {
            "thinker": thinker,
            "key_verses": key_verses[:5],
            "suggested_approach": f"Explore verses related to: {', '.join(thinker['key_themes'][:3])}"
        }


def main():
    """Demo the Understanding Bible"""
    print("=" * 80)
    print("UNDERSTANDING BIBLE - DEEP THEOLOGICAL INSIGHTS")
    print("=" * 80)
    print()
    print("See Scripture through the eyes of great theological thinkers:")
    print("  - Thomas Aquinas")
    print("  - Pope Benedict XVI")
    print("  - Tim Keller")
    print("  - Augustine, Luther, Calvin, Lewis, Bonhoeffer, Barth, N.T. Wright")
    print()
    
    understanding = UnderstandingBible()
    
    # Example: Get understanding of John 3:16
    print("Example: Understanding John 3:16 from multiple perspectives...")
    result = understanding.get_understanding("John", 3, 16, ["Keller", "Benedict", "Lewis"])
    
    if "error" in result:
        print(f"Error: {result['error']}")
        print("\nNote: This requires Bible verses to be loaded first.")
        print("Run: python integrate_bible_versions.py")
    else:
        print(f"\nVerse: {result.get('verse', 'N/A')}")
        print(f"Text: {result.get('verse_text', 'N/A')}")
        print(f"\nInsights from {len(result.get('thinkers', []))} thinkers:")
        for insight in result.get('thinkers', []):
            print(f"\n{insight.get('thinker', 'Unknown')} ({insight.get('tradition', 'Unknown')}):")
            print(f"  {insight.get('insight', '')[:200]}...")
        
        if result.get('synthesis'):
            print(f"\nSynthesis:")
            print(f"  {result['synthesis'].get('text', '')[:200]}...")


if __name__ == "__main__":
    main()