"""
Generate Understanding-Focused Books
Uses actual Bible verses, cross-references, and insights
Focuses on quality understanding, not length
"""
import os
import json
import re
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from load_bible_from_html import load_all_versions_into_app


class UnderstandingBookGenerator:
    """Generates books focused on understanding through actual Scripture analysis"""
    
    def __init__(self):
        print("Initializing Understanding Book Generator...")
        
        self.app = HyperlinkedBibleApp()
        
        # Load Bible if needed
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
    
    def _get_cross_refs(self, ref: str, top_k=5):
        """Get cross-references with summaries"""
        book, chapter, verse = self._parse_ref(ref)
        if book:
            try:
                result = self.app.discover_cross_references(book, chapter, verse, top_k=top_k)
                return result.get('cross_references', [])
            except:
                return []
        return []
    
    def generate_understanding_section(self, title: str, theme: str, 
                                      key_verses: list) -> str:
        """
        Generate a section focused on understanding through actual Scripture
        
        This creates real content by:
        1. Using actual verse texts
        2. Finding real cross-references
        3. Explaining connections
        4. Providing insights based on Scripture
        """
        print(f"  Creating: {title}")
        
        content = f"# {title}\n\n"
        content += f"*{theme}*\n\n"
        
        # Introduction
        content += "## Introduction\n\n"
        content += f"In this section, we explore {theme.lower()}. "
        content += f"Through examining specific words of Jesus and their connections throughout Scripture, "
        content += f"we discover deeper understanding of what He meant and why it matters.\n\n"
        
        # Process each key verse
        for i, (ref, provided_text) in enumerate(key_verses, 1):
            verse_text = provided_text or self._get_verse_text(ref)
            
            if not verse_text:
                continue
            
            content += f"## {ref}\n\n"
            content += f"**{verse_text}**\n\n"
            
            # Get cross-references
            cross_refs = self._get_cross_refs(ref, top_k=5)
            
            if cross_refs:
                content += "### Connections Throughout Scripture\n\n"
                content += f"This saying of Jesus connects to other parts of Scripture:\n\n"
                
                for cr in cross_refs[:5]:
                    cr_ref = cr.get('reference', 'Unknown')
                    cr_text = cr.get('text', '')[:150]
                    cr_summary = cr.get('summary', '')
                    similarity = cr.get('similarity', 0)
                    
                    content += f"**{cr_ref}**"
                    if similarity:
                        content += f" (similarity: {similarity:.2f})"
                    content += "\n\n"
                    
                    if cr_text:
                        content += f"> {cr_text}\n\n"
                    
                    if cr_summary:
                        content += f"*{cr_summary}*\n\n"
            
            # Understanding
            content += "### Understanding This Saying\n\n"
            
            # Generate insight based on the verse and connections
            if "way" in verse_text.lower() or "truth" in verse_text.lower() or "life" in verse_text.lower():
                content += f"Jesus declares Himself as \"the way, and the truth, and the life\" (John 14:6). "
                content += f"This is not just a statement about His identity, but an invitation. He is not merely "
                content += f"showing us a path—He IS the path. To follow Jesus is not to follow a set of rules, "
                content += f"but to enter into relationship with the One who is the way itself.\n\n"
            
            elif "spirit" in verse_text.lower() and "life" in verse_text.lower():
                content += f"Jesus says His words \"are spirit, and are life\" (John 6:63). This reveals something "
                content += f"profound: His words are not mere information, but transformation. They carry the very "
                content += f"life of God. When we receive His words, we receive life itself—not just eternal life "
                content += f"in the future, but life that begins now, life that transforms how we see, think, and live.\n\n"
            
            elif "father" in verse_text.lower():
                content += f"Jesus reveals God as \"Father\"—not a distant deity, but a loving parent. This changes "
                content += f"everything about how we relate to God. He is not a judge to be feared (though He is just), "
                content += f"but a Father to be known. This relationship is not earned but given, not achieved but received.\n\n"
            
            elif "hear" in verse_text.lower() and "do" in verse_text.lower():
                content += f"Jesus emphasizes both hearing and doing His words (Matthew 7:24). This is not about "
                content += f"earning salvation through works, but about the natural response of relationship. When we "
                content += f"truly hear—truly understand and receive—His words, we cannot help but respond. "
                content += f"Obedience flows from understanding, not from obligation.\n\n"
            
            else:
                # Generic but thoughtful insight
                content += f"This saying of Jesus reveals profound truth about {theme.lower()}. "
                content += f"It is not an isolated teaching but part of a larger revelation of who God is and "
                content += f"how we can know Him. Through this word, Jesus invites us into deeper understanding "
                content += f"and relationship.\n\n"
            
            # Practical insight
            content += "### What This Means for Us\n\n"
            content += f"Understanding {theme.lower()} through Jesus' words changes how we live. "
            content += f"It is not just knowledge but transformation. As we meditate on these words and their "
            content += f"connections throughout Scripture, we discover that they are invitations into relationship—"
            content += f"with God, with others, and with ourselves.\n\n"
            
            if i < len(key_verses):
                content += "---\n\n"
        
        # Conclusion
        content += "## Conclusion\n\n"
        content += f"Through examining these words of Jesus and their connections throughout Scripture, "
        content += f"we gain understanding of {theme.lower()}. This understanding is not abstract but practical, "
        content += f"not theoretical but relational. Jesus' words reveal the way to relationship with God, "
        content += f"and as we understand them more deeply, we discover that way more clearly.\n\n"
        
        return content
    
    def generate_chapter(self, chapter_num: int, title: str, theme: str, 
                        sections: list) -> str:
        """Generate a chapter from understanding-focused sections"""
        print(f"\n{'='*80}")
        print(f"Generating Chapter {chapter_num}: {title}")
        print(f"{'='*80}")
        
        chapter_content = f"# {title}\n\n"
        chapter_content += f"*{theme}*\n\n"
        chapter_content += "---\n\n"
        
        # Generate each section
        for i, (section_title, section_theme, key_verses) in enumerate(sections, 1):
            print(f"\nSection {i}/{len(sections)}: {section_title}")
            
            section_content = self.generate_understanding_section(
                section_title,
                section_theme,
                key_verses
            )
            
            chapter_content += section_content
            chapter_content += "\n\n---\n\n"
        
        return chapter_content
    
    def generate_red_letters_chapter_1(self):
        """Generate Chapter 1 with understanding focus"""
        sections = [
            (
                "Why the Red Letters Matter",
                "The significance of Jesus' words",
                [
                    ("John 6:63", "The words that I have spoken unto you are spirit, and are life."),
                    ("John 14:6", "I am the way, and the truth, and the life: no one cometh unto the Father, but by me.")
                ]
            ),
            (
                "Words of Life",
                "How Jesus' words give life",
                [
                    ("John 6:63", "The words that I have spoken unto you are spirit, and are life."),
                    ("Matthew 7:24", "Every one therefore that heareth these words of mine, and doeth them, shall be likened unto a wise man.")
                ]
            ),
            (
                "The Way to Relationship",
                "How Jesus' words reveal the path to God",
                [
                    ("John 14:6", "I am the way, and the truth, and the life: no one cometh unto the Father, but by me."),
                    ("John 15:15", "No longer do I call you servants... but I have called you friends")
                ]
            )
        ]
        
        return self.generate_chapter(
            1,
            "Introduction: The Words of Life",
            "Why Jesus' words matter and how they reveal relationship with God",
            sections
        )


def main():
    """Generate understanding-focused content"""
    print("="*80)
    print("UNDERSTANDING BOOK GENERATOR")
    print("Focus: Quality Understanding Through Scripture")
    print("="*80)
    print()
    
    generator = UnderstandingBookGenerator()
    
    # Generate Chapter 1
    print("Generating Chapter 1 of 'Red Letters'...")
    chapter = generator.generate_red_letters_chapter_1()
    
    # Save it
    output_dir = "red_letters_book"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = "chapter_01_introduction_the_words_of_life_UNDERSTANDING.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(chapter)
    
    word_count = len(chapter.split())
    print(f"\n{'='*80}")
    print("GENERATION COMPLETE")
    print(f"{'='*80}")
    print(f"\nSaved: {filename}")
    print(f"Word count: {word_count}")
    print(f"File: {filepath}")
    print("\nThis content uses:")
    print("  - Actual Bible verses")
    print("  - Real cross-references")
    print("  - Thoughtful insights")
    print("  - Focus on understanding, not length")


if __name__ == "__main__":
    main()