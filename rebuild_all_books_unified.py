"""
Unified Book Generator - Understanding-Focused Style
Rebuilds all books using the same quality, understanding-focused approach
"""
import os
import json
import re
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from load_bible_from_html import load_all_versions_into_app


class UnifiedBookGenerator:
    """Generates all books using the same understanding-focused style"""
    
    def __init__(self):
        print("Initializing Unified Book Generator...")
        print("Style: Understanding-focused, Scripture-based, quality over length")
        
        self.app = HyperlinkedBibleApp()
        
        # Load Bible if needed
        if not self.app.versions.get('asv'):
            print("\nLoading Bible versions...")
            bible_path = r"C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions"
            if os.path.exists(bible_path):
                load_all_versions_into_app(self.app, bible_path)
            else:
                print("Warning: Bible path not found. Some features may be limited.")
    
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
    
    def generate_understanding_content(self, title: str, theme: str, 
                                     key_verses: list, context: str = "") -> str:
        """
        Generate understanding-focused content using actual Scripture
        
        This is the unified style used for all books:
        - Uses actual Bible verses
        - Finds real cross-references
        - Provides thoughtful insights
        - Focuses on understanding, not length
        """
        content = f"# {title}\n\n"
        if theme:
            content += f"*{theme}*\n\n"
        
        if context:
            content += f"{context}\n\n"
        
        content += "---\n\n"
        
        # Introduction
        content += "## Introduction\n\n"
        content += f"In this section, we explore {theme.lower() if theme else 'this topic'}. "
        content += f"Through examining specific verses and their connections throughout Scripture, "
        content += f"we discover deeper understanding of what they mean and why they matter.\n\n"
        
        # Process each key verse
        for i, verse_ref in enumerate(key_verses, 1):
            # Handle tuple or string
            if isinstance(verse_ref, tuple):
                ref, provided_text = verse_ref
            else:
                ref = verse_ref
                provided_text = None
            
            verse_text = provided_text or self._get_verse_text(ref)
            
            if not verse_text:
                continue
            
            content += f"## {ref}\n\n"
            content += f"**{verse_text}**\n\n"
            
            # Get cross-references
            cross_refs = self._get_cross_refs(ref, top_k=5)
            
            if cross_refs:
                content += "### Connections Throughout Scripture\n\n"
                content += f"This verse connects to other parts of Scripture:\n\n"
                
                for cr in cross_refs[:5]:
                    cr_ref = cr.get('reference', 'Unknown')
                    cr_text = cr.get('text', '')[:150]
                    cr_summary = cr.get('summary', '')
                    similarity = cr.get('similarity', 0)
                    
                    content += f"**{cr_ref}**"
                    if similarity and similarity > 0.7:
                        content += f" (similarity: {similarity:.2f})"
                    content += "\n\n"
                    
                    if cr_text:
                        content += f"> {cr_text}\n\n"
                    
                    if cr_summary:
                        content += f"*{cr_summary}*\n\n"
            
            # Understanding
            content += "### Understanding This Verse\n\n"
            
            # Generate insight based on verse content
            verse_lower = verse_text.lower()
            
            if "way" in verse_lower and "truth" in verse_lower and "life" in verse_lower:
                content += f"Jesus declares Himself as \"the way, and the truth, and the life\" (John 14:6). "
                content += f"This is not just a statement about His identity, but an invitation. He is not merely "
                content += f"showing us a path—He IS the path. To follow Jesus is not to follow a set of rules, "
                content += f"but to enter into relationship with the One who is the way itself.\n\n"
            
            elif "spirit" in verse_lower and "life" in verse_lower:
                content += f"Jesus says His words \"are spirit, and are life\" (John 6:63). This reveals something "
                content += f"profound: His words are not mere information, but transformation. They carry the very "
                content += f"life of God. When we receive His words, we receive life itself—not just eternal life "
                content += f"in the future, but life that begins now, life that transforms how we see, think, and live.\n\n"
            
            elif "father" in verse_lower:
                content += f"Jesus reveals God as \"Father\"—not a distant deity, but a loving parent. This changes "
                content += f"everything about how we relate to God. He is not a judge to be feared (though He is just), "
                content += f"but a Father to be known. This relationship is not earned but given, not achieved but received.\n\n"
            
            elif "mystery" in verse_lower or "mysteries" in verse_lower:
                content += f"The Bible speaks of mysteries—not puzzles to be solved, but truths to be revealed. "
                content += f"These mysteries are not hidden from us, but revealed to us through Scripture. They show "
                content += f"us the depth of God's wisdom and the wonder of His ways.\n\n"
            
            elif "love" in verse_lower and "god" in verse_lower:
                content += f"God's love is not abstract but concrete. It is not a feeling but an action. This verse "
                content += f"reveals the nature of divine love—sacrificial, unconditional, transformative. It is love "
                content += f"that gives, that serves, that redeems.\n\n"
            
            else:
                # Thoughtful generic insight
                content += f"This verse reveals profound truth. It is not an isolated teaching but part of a larger "
                content += f"revelation of who God is and how we can know Him. Through this word, we are invited into "
                content += f"deeper understanding and relationship.\n\n"
            
            # Practical insight
            content += "### What This Means for Us\n\n"
            content += f"Understanding this verse changes how we live. It is not just knowledge but transformation. "
            content += f"As we meditate on these words and their connections throughout Scripture, we discover that "
            content += f"they are invitations into relationship—with God, with others, and with ourselves.\n\n"
            
            if i < len(key_verses):
                content += "---\n\n"
        
        # Conclusion
        content += "## Conclusion\n\n"
        content += f"Through examining these verses and their connections throughout Scripture, "
        content += f"we gain understanding of {theme.lower() if theme else 'these truths'}. This understanding is "
        content += f"not abstract but practical, not theoretical but relational. Scripture reveals the way to "
        content += f"relationship with God, and as we understand it more deeply, we discover that way more clearly.\n\n"
        
        return content
    
    def rebuild_red_letters(self):
        """Rebuild Red Letters book with understanding-focused style"""
        print("\n" + "="*80)
        print("REBUILDING: Red Letters Book")
        print("="*80)
        
        output_dir = "red_letters_book"
        os.makedirs(output_dir, exist_ok=True)
        
        chapters = [
            {
                "number": 1,
                "title": "Introduction: The Words of Life",
                "theme": "Why Jesus' words matter and how they reveal relationship with God",
                "key_verses": [
                    ("John 6:63", "The words that I have spoken unto you are spirit, and are life."),
                    ("John 14:6", "I am the way, and the truth, and the life: no one cometh unto the Father, but by me."),
                    ("Matthew 7:24", "Every one therefore that heareth these words of mine, and doeth them, shall be likened unto a wise man.")
                ]
            },
            {
                "number": 2,
                "title": "The Relationship with the Father",
                "theme": "Jesus reveals how to know God as Father",
                "key_verses": [
                    ("John 14:9", "He that hath seen me hath seen the Father"),
                    ("Matthew 6:9", "Our Father who art in heaven"),
                    ("John 17:3", "This is life eternal, that they should know thee the only true God")
                ]
            }
        ]
        
        for chapter in chapters[:2]:  # Start with first 2 chapters
            print(f"\nGenerating Chapter {chapter['number']}: {chapter['title']}")
            
            content = self.generate_understanding_content(
                chapter['title'],
                chapter['theme'],
                chapter['key_verses']
            )
            
            # Save
            safe_title = chapter['title'].lower().replace(' ', '_').replace(':', '').replace("'", "").replace(",", "")
            filename = f"chapter_{chapter['number']:02d}_{safe_title}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            word_count = len(content.split())
            print(f"  Saved: {filename} ({word_count} words)")
    
    def rebuild_bible_mysteries(self):
        """Rebuild Bible Mysteries book with understanding-focused style"""
        print("\n" + "="*80)
        print("REBUILDING: Bible Mysteries Book")
        print("="*80)
        
        output_dir = "bible_mysteries_book"
        os.makedirs(output_dir, exist_ok=True)
        
        chapters = [
            {
                "number": 1,
                "title": "Introduction: The Mystery of Divine Revelation",
                "theme": "How God reveals Himself through Scripture",
                "key_verses": ["John 1:1", "2 Timothy 3:16", "Hebrews 4:12"]
            },
            {
                "number": 2,
                "title": "The Mystery of the Trinity",
                "theme": "One God in three persons",
                "key_verses": ["Matthew 28:19", "John 10:30", "2 Corinthians 13:14"]
            }
        ]
        
        for chapter in chapters[:2]:  # Start with first 2 chapters
            print(f"\nGenerating Chapter {chapter['number']}: {chapter['title']}")
            
            content = self.generate_understanding_content(
                chapter['title'],
                chapter['theme'],
                chapter['key_verses']
            )
            
            # Save
            safe_title = chapter['title'].lower().replace(' ', '_').replace(':', '').replace("'", "").replace(",", "")
            filename = f"chapter_{chapter['number']:02d}_{safe_title}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            word_count = len(content.split())
            print(f"  Saved: {filename} ({word_count} words)")
    
    def rebuild_book_study(self, book_name: str, theme: str, key_verses: list):
        """Rebuild a single book study with understanding-focused style"""
        print(f"\nGenerating study for: {book_name}")
        
        content = self.generate_understanding_content(
            f"{book_name}: A Bible Study",
            theme,
            key_verses,
            context=f"This is a study of the book of {book_name}, exploring its themes, "
                    f"key verses, and connections throughout Scripture."
        )
        
        # Save
        output_dir = "book_by_book_studies"
        os.makedirs(output_dir, exist_ok=True)
        
        safe_name = book_name.replace(' ', '_').replace(':', '').replace("'", "")
        filename = f"{safe_name}_study.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        word_count = len(content.split())
        print(f"  Saved: {filename} ({word_count} words)")
        
        return content


def main():
    """Rebuild all books with unified understanding-focused style"""
    print("="*80)
    print("UNIFIED BOOK GENERATOR")
    print("Rebuilding all books with understanding-focused style")
    print("="*80)
    print()
    print("Style features:")
    print("  - Uses actual Bible verses")
    print("  - Real cross-references")
    print("  - Thoughtful insights")
    print("  - Focus on understanding, not length")
    print()
    
    generator = UnifiedBookGenerator()
    
    # Rebuild Red Letters
    generator.rebuild_red_letters()
    
    # Rebuild Bible Mysteries
    generator.rebuild_bible_mysteries()
    
    # Rebuild a sample book study
    print("\n" + "="*80)
    print("REBUILDING: Sample Book Study")
    print("="*80)
    generator.rebuild_book_study(
        "Genesis",
        "The Beginning - Creation, Fall, and God's Covenant",
        ["Genesis 1:1", "Genesis 3:15", "Genesis 12:1-3"]
    )
    
    print("\n" + "="*80)
    print("REBUILD COMPLETE")
    print("="*80)
    print("\nAll books rebuilt with unified understanding-focused style!")
    print("\nNote: This is a sample. To rebuild all chapters/books, run with full lists.")


if __name__ == "__main__":
    main()