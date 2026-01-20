"""
Relationship Bible Journey - An Engaging, Unique Bible Experience
Not just reading - a personalized journey that builds relationship with God
"""
import os
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
from hyperlinked_bible_app import HyperlinkedBibleApp
from quantum_llm_standalone import StandaloneQuantumLLM


class RelationshipBibleJourney:
    """
    A unique, engaging Bible experience focused on building relationship with God
    Not a reading plan - a personalized journey of discovery
    """
    
    def __init__(self):
        """Initialize the journey"""
        self.app = HyperlinkedBibleApp()
        self.llm = StandaloneQuantumLLM(
            kernel=self.app.kernel,
            source_texts=list(self.app.versions.get('asv', {}).values())[:100] if self.app.versions else ["God is love"]
        )
        
        self.journey_file = "bible_journey.json"
        self.journey = self._load_journey()
    
    def _load_journey(self) -> Dict:
        """Load or create journey"""
        if os.path.exists(self.journey_file):
            try:
                with open(self.journey_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "started": datetime.now().isoformat(),
            "current_theme": None,
            "discoveries": [],
            "conversations": [],
            "personal_verses": [],
            "journey_path": [],
            "relationship_milestones": [],
            "current_question": None,
            "life_situations": []
        }
    
    def _save_journey(self):
        """Save journey progress"""
        with open(self.journey_file, 'w', encoding='utf-8') as f:
            json.dump(self.journey, f, indent=2)
    
    def start_journey(self, current_life_situation: str = None, 
                     what_youre_seeking: str = None) -> Dict:
        """
        Start your personalized Bible journey
        
        Not a reading plan - a discovery adventure tailored to you
        """
        print("=" * 80)
        print("STARTING YOUR BIBLE JOURNEY")
        print("=" * 80)
        print()
        
        # Understand where they are
        if current_life_situation:
            self.journey["life_situations"].append({
                "date": datetime.now().isoformat(),
                "situation": current_life_situation
            })
        
        # Find starting point based on their need
        starting_verse = self._find_starting_verse(what_youre_seeking or current_life_situation)
        
        # Create first discovery
        discovery = self._create_discovery(starting_verse, "Your journey begins here")
        
        self.journey["current_theme"] = discovery.get("theme", "Getting to Know God")
        self.journey["discoveries"].append(discovery)
        self.journey["journey_path"].append({
            "date": datetime.now().isoformat(),
            "type": "start",
            "verse": starting_verse["reference"],
            "theme": discovery["theme"]
        })
        
        self._save_journey()
        
        return {
            "message": "Your journey has begun!",
            "starting_verse": starting_verse,
            "discovery": discovery,
            "next_step": "Ask a question or explore the connections"
        }
    
    def _find_starting_verse(self, context: str = None) -> Dict:
        """Find the perfect starting verse based on what they need"""
        if not context:
            # Default: God's love
            return {
                "reference": "John 3:16",
                "text": self.app.get_verse_text("John", 3, 16),
                "why": "A beautiful starting point - God's love for you"
            }
        
        # Use AI to find relevant verse
        try:
            results = self.app.kernel.find_similar(
                context,
                list(self.app.versions.get('asv', {}).values())[:1000] if self.app.versions else [],
                top_k=1
            )
            
            if results:
                verse_text, similarity = results[0]
                # Find reference
                for ref, text in self.app.versions.get('asv', {}).items():
                    if text == verse_text:
                        return {
                            "reference": ref,
                            "text": text,
                            "why": f"Relevant to what you're experiencing: {context}"
                        }
        except:
            pass
        
        # Fallback
        return {
            "reference": "John 3:16",
            "text": self.app.get_verse_text("John", 3, 16),
            "why": "A beautiful starting point"
        }
    
    def _create_discovery(self, verse: Dict, context: str) -> Dict:
        """Create an engaging discovery experience"""
        ref = verse["reference"]
        book, chapter, verse_num = self._parse_reference(ref)
        
        # Get cross-references
        cross_refs = self.app.discover_cross_references(book, chapter, verse_num, top_k=5)
        
        # Generate personalized insight
        insight = self._generate_insight(verse, cross_refs, context)
        
        # Find theme
        theme = self._extract_theme(verse["text"])
        
        return {
            "verse": verse,
            "theme": theme,
            "insight": insight,
            "cross_references": cross_refs.get("cross_references", [])[:3],
            "discovered_at": datetime.now().isoformat(),
            "connections_found": len(cross_refs.get("cross_references", []))
        }
    
    def _generate_insight(self, verse: Dict, cross_refs: Dict, context: str) -> str:
        """Generate a personal, engaging insight"""
        prompt = f"""Write a brief, personal insight about this Bible verse that helps someone build relationship with God.

Verse: {verse['reference']} - {verse['text']}
Context: {context}

Write as if you're a friend helping them discover something beautiful about God.
Keep it conversational, warm, and focused on relationship - not just information.
Make it feel like a discovery, not a lesson.
2-3 sentences max."""
        
        try:
            result = self.llm.generate_grounded(prompt, max_length=200, require_validation=True)
            return result.get('generated', self._default_insight(verse))
        except:
            return self._default_insight(verse)
    
    def _default_insight(self, verse: Dict) -> str:
        """Default insight if generation fails"""
        return f"This verse reveals something beautiful about God's heart. As you read it, let it speak to you personally. What is God saying to you through these words?"
    
    def _extract_theme(self, text: str) -> str:
        """Extract theme from verse"""
        themes = {
            'love': 'God\'s Love',
            'faith': 'Faith and Trust',
            'grace': 'Grace and Mercy',
            'hope': 'Hope and Encouragement',
            'peace': 'Peace and Comfort',
            'joy': 'Joy and Rejoicing',
            'salvation': 'Salvation',
            'prayer': 'Prayer',
            'wisdom': 'Wisdom',
            'strength': 'Strength and Courage'
        }
        
        text_lower = text.lower()
        for word, theme in themes.items():
            if word in text_lower:
                return theme
        
        return "God's Character"
    
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
    
    def ask_question(self, question: str) -> Dict:
        """
        Ask a question - get a personalized response with verses
        
        This is like having a conversation with God through His Word
        """
        print(f"\nYour question: {question}")
        print("Finding answers in Scripture...")
        
        # Find relevant verses
        relevant_verses = self._find_verses_for_question(question)
        
        # Generate conversational response
        response = self._generate_conversational_response(question, relevant_verses)
        
        # Create discovery from this
        if relevant_verses:
            main_verse = relevant_verses[0]
            discovery = self._create_discovery(main_verse, f"Answer to: {question}")
            self.journey["discoveries"].append(discovery)
            self.journey["conversations"].append({
                "date": datetime.now().isoformat(),
                "question": question,
                "response": response,
                "verses": relevant_verses
            })
            self._save_journey()
        
        return {
            "question": question,
            "response": response,
            "verses": relevant_verses,
            "discovery": discovery if relevant_verses else None
        }
    
    def _find_verses_for_question(self, question: str, top_k: int = 3) -> List[Dict]:
        """Find verses that answer the question"""
        try:
            # Search all verses
            all_verses = []
            all_refs = []
            
            for version_dict in self.app.versions.values():
                for ref, text in version_dict.items():
                    all_verses.append(text)
                    all_refs.append(ref)
            
            if not all_verses:
                return []
            
            # Semantic search
            similar = self.app.kernel.find_similar(question, all_verses, top_k=top_k)
            
            results = []
            for verse_text, similarity in similar:
                try:
                    idx = all_verses.index(verse_text)
                    ref = all_refs[idx]
                    book, chapter, verse = self._parse_reference(ref)
                    
                    results.append({
                        "reference": ref,
                        "text": verse_text,
                        "relevance": float(similarity),
                        "book": book,
                        "chapter": chapter,
                        "verse": verse
                    })
                except:
                    continue
            
            return results
        except:
            return []
    
    def _generate_conversational_response(self, question: str, verses: List[Dict]) -> str:
        """Generate a warm, conversational response"""
        if not verses:
            return "Let me search the Scriptures for you. What specific area would you like to explore?"
        
        verse_texts = "\n".join([f"{v['reference']}: {v['text']}" for v in verses[:3]])
        
        prompt = f"""Someone asked: "{question}"

Here are relevant Bible verses:
{verse_texts}

Write a warm, conversational response that:
1. Acknowledges their question
2. Shares what the Bible says (using the verses)
3. Helps them see how this relates to relationship with God
4. Invites them to explore further
5. Feels like a friend helping, not a teacher lecturing

Keep it personal, warm, and focused on relationship. 3-4 sentences."""
        
        try:
            result = self.llm.generate_grounded(prompt, max_length=300, require_validation=True)
            return result.get('generated', self._default_response(verses))
        except:
            return self._default_response(verses)
    
    def _default_response(self, verses: List[Dict]) -> str:
        """Default response"""
        if verses:
            return f"The Bible speaks to your question in {verses[0]['reference']}. Let's explore what God says about this together."
        return "Let's explore what the Bible says about this together."
    
    def explore_connections(self, verse_ref: str) -> Dict:
        """
        Explore connections from a verse
        
        Like following threads in a conversation with God
        """
        book, chapter, verse = self._parse_reference(verse_ref)
        
        if not book:
            return {"error": "Invalid verse reference"}
        
        # Get cross-references
        cross_refs = self.app.discover_cross_references(book, chapter, verse, top_k=10)
        
        # Find themes
        themes = self._discover_themes(cross_refs)
        
        # Create exploration
        exploration = {
            "starting_verse": verse_ref,
            "connections": cross_refs.get("cross_references", []),
            "themes": themes,
            "explored_at": datetime.now().isoformat()
        }
        
        self.journey["discoveries"].append({
            "type": "exploration",
            "exploration": exploration,
            "discovered_at": datetime.now().isoformat()
        })
        self._save_journey()
        
        return exploration
    
    def _discover_themes(self, cross_refs: Dict) -> List[str]:
        """Discover themes from cross-references"""
        themes = set()
        for ref in cross_refs.get("cross_references", []):
            summary = ref.get("summary", "")
            if summary:
                themes.add(summary)
        return list(themes)[:5]
    
    def save_personal_verse(self, verse_ref: str, why_meaningful: str = None) -> Dict:
        """
        Save a verse that's meaningful to you
        
        Build your personal collection of verses that speak to you
        """
        book, chapter, verse = self._parse_reference(verse_ref)
        
        if not book:
            return {"error": "Invalid verse reference"}
        
        verse_text = self.app.get_verse_text(book, chapter, verse)
        
        personal_verse = {
            "reference": verse_ref,
            "text": verse_text,
            "why_meaningful": why_meaningful or "Speaks to my heart",
            "saved_at": datetime.now().isoformat()
        }
        
        self.journey["personal_verses"].append(personal_verse)
        self._save_journey()
        
        return {
            "message": "Verse saved to your personal collection",
            "verse": personal_verse,
            "total_saved": len(self.journey["personal_verses"])
        }
    
    def continue_journey(self) -> Dict:
        """
        Continue your journey - get next discovery
        
        Not a reading plan - a personalized next step
        """
        if not self.journey.get("discoveries"):
            return self.start_journey()
        
        # Find next discovery based on journey so far
        last_discovery = self.journey["discoveries"][-1]
        
        # Get a connected verse
        if last_discovery.get("cross_references"):
            next_ref = last_discovery["cross_references"][0]["reference"]
            book, chapter, verse = self._parse_reference(next_ref)
            verse_text = self.app.get_verse_text(book, chapter, verse)
            
            next_verse = {
                "reference": next_ref,
                "text": verse_text,
                "why": "Connected to what you just discovered"
            }
        else:
            # Find new theme
            next_verse = self._find_next_theme_verse()
        
        discovery = self._create_discovery(next_verse, "Your journey continues")
        self.journey["discoveries"].append(discovery)
        self._save_journey()
        
        return {
            "discovery": discovery,
            "journey_progress": len(self.journey["discoveries"]),
            "message": "Your journey continues..."
        }
    
    def _find_next_theme_verse(self) -> Dict:
        """Find next verse based on journey themes"""
        # Simple: return a foundational verse
        return {
            "reference": "Jeremiah 29:13",
            "text": self.app.get_verse_text("Jeremiah", 29, 13),
            "why": "A beautiful promise about seeking God"
        }
    
    def get_journey_summary(self) -> Dict:
        """Get your journey summary"""
        return {
            "started": self.journey.get("started"),
            "days_active": (datetime.now() - datetime.fromisoformat(self.journey["started"])).days if self.journey.get("started") else 0,
            "discoveries": len(self.journey.get("discoveries", [])),
            "conversations": len(self.journey.get("conversations", [])),
            "personal_verses": len(self.journey.get("personal_verses", [])),
            "current_theme": self.journey.get("current_theme"),
            "recent_discoveries": self.journey.get("discoveries", [])[-5:],
            "your_verses": self.journey.get("personal_verses", [])[-5:]
        }


def main():
    """Demo the relationship journey"""
    print("=" * 80)
    print("RELATIONSHIP BIBLE JOURNEY")
    print("=" * 80)
    print()
    print("This is not a reading plan.")
    print("This is a personalized journey to build relationship with God.")
    print()
    print("Features:")
    print("  - Ask questions, get answers from Scripture")
    print("  - Explore connections like following threads")
    print("  - Save verses that speak to you")
    print("  - Discover themes that matter to you")
    print("  - Build your personal collection")
    print("  - Continue your unique journey")
    print()
    
    journey = RelationshipBibleJourney()
    
    # Start journey
    result = journey.start_journey(
        current_life_situation="I want to know God better",
        what_youre_seeking="relationship with God"
    )
    
    print("\nStarting Verse:")
    print(f"  {result['starting_verse']['reference']}")
    print(f"  {result['starting_verse']['text']}")
    print(f"  Why: {result['starting_verse']['why']}")
    print()
    print("Discovery:")
    print(f"  Theme: {result['discovery']['theme']}")
    print(f"  Insight: {result['discovery']['insight']}")
    print()
    print("Your journey has begun!")
    print()
    print("Try:")
    print("  journey.ask_question('How can I trust God more?')")
    print("  journey.explore_connections('John 3:16')")
    print("  journey.save_personal_verse('John 3:16', 'This verse changed my life')")
    print("  journey.continue_journey()")


if __name__ == "__main__":
    main()