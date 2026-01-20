"""
Blow Your Mind - Reveal the Infinite Depth of Scripture
Shows how one verse connects to the ENTIRE biblical narrative
"""
import os
import json
import re
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from load_bible_from_html import load_all_versions_into_app


class BlowYourMind:
    """
    Reveals how one verse connects to:
    - The entire Old Testament
    - The entire New Testament  
    - The grand narrative
    - Multiple themes simultaneously
    - The mind of God
    """
    
    def __init__(self):
        print("Initializing Mind-Blowing Revelation System...")
        
        self.app = HyperlinkedBibleApp()
        
        # Load Bible
        if not self.app.versions.get('asv'):
            print("Loading Bible...")
            bible_path = r"C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions"
            if os.path.exists(bible_path):
                load_all_versions_into_app(self.app, bible_path)
    
    def _parse_ref(self, ref: str):
        """Parse verse reference"""
        if '-' in ref:
            ref = ref.split('-')[0]
        match = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
        if match:
            return match.group(1).strip(), int(match.group(2)), int(match.group(3))
        return None, 0, 0
    
    def _get_verse_text(self, ref: str):
        """Get verse text"""
        book, chapter, verse = self._parse_ref(ref)
        if book:
            return self.app.get_verse_text(book, chapter, verse, version='asv')
        return None
    
    def _get_all_connections(self, ref: str, max_connections=50):
        """Get ALL connections to a verse"""
        book, chapter, verse = self._parse_ref(ref)
        if not book:
            return []
        
        try:
            result = self.app.discover_cross_references(book, chapter, verse, top_k=max_connections)
            return result.get('cross_references', [])
        except:
            return []
    
    def _map_to_biblical_narrative(self, verse_ref: str, verse_text: str):
        """Map how this verse connects to the entire biblical narrative"""
        
        narrative = {
            "creation": [],
            "fall": [],
            "covenant": [],
            "exodus": [],
            "law": [],
            "kings": [],
            "prophets": [],
            "exile": [],
            "return": [],
            "gospels": [],
            "church": [],
            "revelation": []
        }
        
        # Get connections
        connections = self._get_all_connections(verse_ref, max_connections=100)
        
        # Map to narrative periods
        for conn in connections:
            ref = conn.get('reference', '')
            book = ref.split()[0] if ref else ''
            
            # Old Testament periods
            if book in ['Genesis']:
                if '1' in ref or '2' in ref:
                    narrative['creation'].append(conn)
                elif '3' in ref or '4' in ref:
                    narrative['fall'].append(conn)
                elif '12' in ref or '15' in ref or '17' in ref:
                    narrative['covenant'].append(conn)
            
            elif book in ['Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']:
                narrative['exodus'].append(conn)
                narrative['law'].append(conn)
            
            elif book in ['Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', 
                          '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles']:
                narrative['kings'].append(conn)
            
            elif book in ['Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel',
                          'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah',
                          'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']:
                narrative['prophets'].append(conn)
            
            elif book in ['Ezra', 'Nehemiah', 'Esther']:
                narrative['return'].append(conn)
            
            # New Testament periods
            elif book in ['Matthew', 'Mark', 'Luke', 'John']:
                narrative['gospels'].append(conn)
            
            elif book in ['Acts', 'Romans', '1 Corinthians', '2 Corinthians',
                          'Galatians', 'Ephesians', 'Philippians', 'Colossians',
                          '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy',
                          'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter',
                          '1 John', '2 John', '3 John', 'Jude']:
                narrative['church'].append(conn)
            
            elif book == 'Revelation':
                narrative['revelation'].append(conn)
        
        return narrative
    
    def blow_your_mind(self, book: str, chapter: int, verse: int):
        """
        Generate a mind-blowing revelation about a verse
        """
        verse_ref = f"{book} {chapter}:{verse}"
        verse_text = self._get_verse_text(verse_ref)
        
        if not verse_text:
            return {"error": f"Verse {verse_ref} not found"}
        
        print(f"\n{'='*80}")
        print(f"BLOWING YOUR MIND WITH: {verse_ref}")
        print(f"{'='*80}\n")
        
        # Get all connections
        print("Discovering connections throughout ALL of Scripture...")
        all_connections = self._get_all_connections(verse_ref, max_connections=100)
        
        # Map to biblical narrative
        print("Mapping to the entire biblical narrative...")
        narrative_map = self._map_to_biblical_narrative(verse_ref, verse_text)
        
        # Create the mind-blowing revelation
        revelation = self._create_revelation(verse_ref, verse_text, all_connections, narrative_map)
        
        return {
            "verse": verse_ref,
            "verse_text": verse_text,
            "total_connections": len(all_connections),
            "narrative_map": narrative_map,
            "revelation": revelation,
            "generated_at": datetime.now().isoformat()
        }
    
    def _create_revelation(self, verse_ref: str, verse_text: str,
                          connections: list, narrative_map: dict) -> str:
        """Create the mind-blowing revelation"""
        
        content = f"# MIND-BLOWN: {verse_ref}\n\n"
        content += f"**{verse_text}**\n\n"
        content += "---\n\n"
        
        content += "## Why This Will Blow Your Mind\n\n"
        content += f"This single verse—{verse_ref}—is not just a verse. It's a **window into the entire biblical narrative**.\n\n"
        
        # The connections
        content += f"## The Connections\n\n"
        content += f"This verse connects to **{len(connections)} other verses** throughout Scripture. "
        content += f"That's not a coincidence—it's because this verse is woven into the very fabric of God's story.\n\n"
        
        # Narrative mapping
        content += "## How It Connects to the ENTIRE Story\n\n"
        content += "This verse echoes through every period of biblical history:\n\n"
        
        periods = {
            "creation": "The Beginning",
            "fall": "The Fall",
            "covenant": "God's Covenant",
            "exodus": "The Exodus",
            "law": "The Law",
            "kings": "The Kingdom",
            "prophets": "The Prophets",
            "exile": "The Exile",
            "return": "The Return",
            "gospels": "The Gospels",
            "church": "The Church",
            "revelation": "The Revelation"
        }
        
        for period, count in [(p, len(narrative_map[p])) for p in periods.keys()]:
            if count > 0:
                content += f"- **{periods[period]}**: {count} connections\n"
        
        content += "\n"
        
        # Show examples from each period
        content += "### Examples of Connections\n\n"
        shown_periods = 0
        for period, period_name in periods.items():
            if len(narrative_map[period]) > 0 and shown_periods < 5:
                content += f"**{period_name}:**\n"
                for conn in narrative_map[period][:3]:
                    ref = conn.get('reference', 'Unknown')
                    summary = conn.get('summary', conn.get('text', ''))[:100]
                    content += f"- {ref}: {summary}...\n"
                content += "\n"
                shown_periods += 1
        
        # The revelation
        content += "## The Revelation\n\n"
        content += f"Here's what makes {verse_ref} mind-blowing:\n\n"
        content += f"1. **It's Not Isolated**: This verse connects to {len(connections)} other verses\n"
        content += f"2. **It Spans History**: It echoes through every period of biblical history\n"
        content += f"3. **It's Part of a Story**: It's not just a verse—it's part of God's grand narrative\n"
        content += f"4. **It's Infinite**: The more you explore, the more connections you find\n"
        content += f"5. **It's Alive**: This verse is living truth that speaks across time\n\n"
        
        content += "## The Mind-Blowing Truth\n\n"
        content += f"**This single verse contains more depth than we could explore in a lifetime.**\n\n"
        content += f"That's the nature of Scripture—every word is a window into infinite truth. "
        content += f"Every verse is connected to the entire story. Every phrase reveals something about "
        content += f"God's character, His plan, and His love.\n\n"
        
        content += f"When you read {verse_ref}, you're not just reading a verse. You're reading "
        content += f"a thread that runs through all of Scripture, connecting creation to revelation, "
        content += f"promise to fulfillment, law to grace, and humanity to divinity.\n\n"
        
        content += "**That's why it blows your mind.**\n\n"
        
        return content
    
    def save_revelation(self, insight: dict, filename: str = None):
        """Save the revelation"""
        if filename is None:
            verse_ref = insight['verse'].replace(' ', '_').replace(':', '_')
            filename = f"mind_blown_{verse_ref}.md"
        
        output_dir = "mind_blowing_insights"
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(insight.get('revelation', ''))
        
        print(f"\n[SAVED] {filepath}")
        return filepath


def main():
    """Blow your mind"""
    print("="*80)
    print("BLOW YOUR MIND - REVEALING THE INFINITE DEPTH OF SCRIPTURE")
    print("="*80)
    print()
    print("This will show you how ONE verse connects to:")
    print("  - The ENTIRE Old Testament")
    print("  - The ENTIRE New Testament")
    print("  - Every period of biblical history")
    print("  - The grand narrative of God's story")
    print()
    
    generator = BlowYourMind()
    
    # Try a few verses
    test_verses = [
        ("John", 3, 16),
        ("Genesis", 1, 1),
        ("John", 14, 6),
        ("Romans", 8, 28)
    ]
    
    for book, chapter, verse in test_verses[:1]:  # Start with one
        print(f"\n{'='*80}")
        print(f"Analyzing: {book} {chapter}:{verse}")
        print(f"{'='*80}")
        
        insight = generator.blow_your_mind(book, chapter, verse)
        
        if "error" not in insight:
            filepath = generator.save_revelation(insight)
            
            print(f"\n[OK] MIND BLOWN!")
            print(f"   Verse: {insight['verse']}")
            print(f"   Total connections: {insight['total_connections']}")
            print(f"   File: {filepath}")
            print(f"\n   Open the file to see how this ONE verse connects to ALL of Scripture!")
        else:
            print(f"   {insight['error']}")


if __name__ == "__main__":
    main()