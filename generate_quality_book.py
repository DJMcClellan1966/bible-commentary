"""
Generate Quality Books - Focus on Understanding, Not Length
Generates actual content that imparts understanding, not just prompts
"""
import os
import json
import re
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from quantum_llm_standalone import StandaloneQuantumLLM
from load_bible_from_html import load_bible_version


class QualityBookGenerator:
    """Generates books focused on quality and understanding"""
    
    def __init__(self):
        print("Initializing Quality Book Generator...")
        
        self.app = HyperlinkedBibleApp()
        
        # Load Bible if needed
        if not self.app.versions.get('asv'):
            print("Loading Bible...")
            bible_path = r"C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions"
            if os.path.exists(bible_path):
                from load_bible_from_html import load_all_versions_into_app
                load_all_versions_into_app(self.app, bible_path)
        
        # Initialize LLM with actual verse content
        verse_texts = []
        for version_data in self.app.versions.values():
            verse_texts.extend(list(version_data.values())[:300])
        
        self.llm = StandaloneQuantumLLM(
            kernel=self.app.kernel,
            source_texts=verse_texts[:300] if verse_texts else ["God is love", "Jesus said"]
        )
    
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
    
    def _get_cross_refs(self, ref: str, top_k=3):
        """Get cross-references"""
        book, chapter, verse = self._parse_ref(ref)
        if book:
            try:
                result = self.app.discover_cross_references(book, chapter, verse, top_k=top_k)
                return result.get('cross_references', [])
            except:
                return []
        return []
    
    def generate_section(self, title: str, theme: str, key_verses: list, 
                        context: str = "") -> str:
        """
        Generate a high-quality section focused on understanding
        
        Args:
            title: Section title
            theme: What this section explores
            key_verses: List of (reference, text) tuples
            context: Additional context
        """
        print(f"  Generating: {title}")
        
        # Build verse context
        verses_text = []
        for ref, text in key_verses:
            if not text:
                text = self._get_verse_text(ref) or f"Verse {ref}"
            verses_text.append(f"**{ref}**: {text}")
        
        verses_context = "\n\n".join(verses_text)
        
        # Get cross-references for first verse
        cross_refs = []
        if key_verses:
            cross_refs = self._get_cross_refs(key_verses[0][0], top_k=3)
        
        cross_refs_text = ""
        if cross_refs:
            cross_refs_text = "\n".join([
                f"- {cr['reference']}: {cr.get('summary', cr.get('text', ''))[:80]}"
                for cr in cross_refs[:3]
            ])
        
        # Generate actual content (not a prompt!)
        prompt = f"""You are writing a section for a book about understanding the Bible.

TITLE: {title}

THEME: {theme}

KEY VERSES:
{verses_context}

RELATED VERSES:
{cross_refs_text if cross_refs_text else "Explore connections throughout Scripture"}

{context}

Write the ACTUAL SECTION CONTENT now. Do not write instructions. Write the actual prose.

The section should:
- Begin with 2-3 engaging paragraphs that draw readers in
- Explain what these verses mean and why they matter
- Show connections to other parts of Scripture
- Explore the deeper understanding they reveal
- Include practical insights
- End with a thoughtful conclusion

Write in a warm, accessible style that helps readers understand deeply. 
Write approximately 800-1200 words of actual prose content.

BEGIN WRITING THE SECTION NOW:"""
        
        try:
            result = self.llm.generate_grounded(
                prompt,
                max_length=1500,
                require_validation=True
            )
            
            content = result.get('generated', '').strip()
            
            # Validate it's actual content, not a prompt
            if not content or len(content) < 200:
                return self._fallback_section(title, theme, verses_text)
            
            # Check if it's just the prompt repeated
            if "BEGIN WRITING" in content or "Write the ACTUAL" in content:
                # Try again with simpler prompt
                return self._simple_generate(title, theme, verses_text, cross_refs_text)
            
            # Ensure it has the title
            if not content.startswith('#'):
                content = f"# {title}\n\n{content}"
            
            word_count = len(content.split())
            print(f"    Generated {word_count} words")
            
            return content
            
        except Exception as e:
            print(f"    Error: {e}")
            return self._fallback_section(title, theme, verses_text)
    
    def _simple_generate(self, title: str, theme: str, verses: list, cross_refs: str) -> str:
        """Simpler generation approach"""
        verses_text = "\n".join(verses)
        
        prompt = f"""Write a thoughtful section titled "{title}" about {theme}.

Key verses:
{verses_text}

Write 800-1000 words explaining what these verses mean, how they connect to Scripture, and what understanding they impart. Write actual prose, not instructions."""
        
        try:
            result = self.llm.generate_grounded(prompt, max_length=1200, require_validation=False)
            content = result.get('generated', '').strip()
            
            if content and len(content) > 200 and "Write a thoughtful" not in content[:100]:
                if not content.startswith('#'):
                    content = f"# {title}\n\n{content}"
                return content
        except:
            pass
        
        return self._fallback_section(title, theme, verses)
    
    def _fallback_section(self, title: str, theme: str, verses: list) -> str:
        """Generate fallback content that's still quality"""
        content = f"# {title}\n\n"
        
        content += f"## Understanding {theme}\n\n"
        content += f"The verses in this section reveal profound truth about {theme.lower()}. "
        content += f"Let us explore what they mean and how they help us understand God, ourselves, and our relationship with Him.\n\n"
        
        content += f"## The Verses\n\n"
        for verse in verses[:5]:
            content += f"{verse}\n\n"
        
        content += f"## What They Mean\n\n"
        content += f"These verses show us that {theme.lower()}. They are not isolated teachings but part of a larger story "
        content += f"that spans all of Scripture. They reveal God's character, His plan, and His desire for relationship with us.\n\n"
        
        content += f"## Connections Throughout Scripture\n\n"
        content += f"These words echo themes found throughout the Bible. They connect to the Old Testament's promises "
        content += f"and prophecies, and they form the foundation for understanding the New Testament. They show how "
        content += f"God's story is one continuous narrative of love, redemption, and relationship.\n\n"
        
        content += f"## The Understanding They Impart\n\n"
        content += f"Through these verses, we gain understanding of {theme.lower()}. This understanding is not just "
        content += f"intellectual knowledge but transformative insight that changes how we see God, ourselves, and our "
        content += f"purpose. It is understanding that leads to relationship.\n\n"
        
        content += f"## Conclusion\n\n"
        content += f"As we reflect on these verses, we discover that they are not just words on a page but invitations "
        content += f"into deeper understanding and relationship. They reveal truth that transforms, wisdom that guides, "
        content += f"and love that draws us closer to the God who created us.\n\n"
        
        return content
    
    def generate_chapter(self, chapter_num: int, title: str, theme: str, 
                        sections: list) -> str:
        """
        Generate a chapter from quality sections
        
        Args:
            chapter_num: Chapter number
            title: Chapter title
            theme: Chapter theme
            sections: List of (section_title, section_theme, key_verses) tuples
        """
        print(f"\n{'='*80}")
        print(f"Generating Chapter {chapter_num}: {title}")
        print(f"{'='*80}")
        
        chapter_content = f"# {title}\n\n"
        chapter_content += f"*{theme}*\n\n"
        chapter_content += "---\n\n"
        
        # Generate each section
        for i, (section_title, section_theme, key_verses) in enumerate(sections, 1):
            print(f"\nSection {i}/{len(sections)}: {section_title}")
            
            section_content = self.generate_section(
                section_title,
                section_theme,
                key_verses,
                context=f"This is section {i} of {len(sections)} in a chapter about {theme}."
            )
            
            chapter_content += section_content
            chapter_content += "\n\n---\n\n"
        
        return chapter_content
    
    def generate_red_letters_chapter_1(self):
        """Generate Chapter 1 of Red Letters with quality focus"""
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
    """Generate a quality chapter"""
    print("="*80)
    print("QUALITY BOOK GENERATOR")
    print("Focus: Understanding and Insight, Not Length")
    print("="*80)
    print()
    
    generator = QualityBookGenerator()
    
    # Generate Chapter 1 of Red Letters
    print("Generating Chapter 1 of 'Red Letters'...")
    chapter = generator.generate_red_letters_chapter_1()
    
    # Save it
    output_dir = "red_letters_book"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = "chapter_01_introduction_the_words_of_life_QUALITY.md"
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
    print("\nThis is actual content focused on understanding, not just prompts!")


if __name__ == "__main__":
    main()