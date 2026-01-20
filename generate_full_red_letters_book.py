"""
Generate FULL Red Letters Book - Actually Write the Content
This will generate actual chapter content, not just prompts
"""
import os
import json
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from quantum_llm_standalone import StandaloneQuantumLLM
from load_bible_from_html import load_bible_version


class FullRedLettersBookGenerator:
    """Generates actual full book content, not just prompts"""
    
    def __init__(self):
        print("Initializing Full Red Letters Book Generator...")
        
        # Initialize Bible app
        self.app = HyperlinkedBibleApp()
        
        # Load Bible versions if needed
        if not self.app.versions.get('asv'):
            print("Loading Bible versions...")
            bible_path = r"C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions"
            if os.path.exists(bible_path):
                for version in ['asv']:  # Just load ASV for now
                    verses = load_bible_version(bible_path, version, version)
                    if verses:
                        print(f"  Adding {len(verses)} verses to app...")
                        for book, chapter, verse_num, text in verses[:1000]:  # Limit for speed
                            self.app.add_verse(book, chapter, verse_num, text, version=version)
        
        # Initialize LLM
        verse_texts = []
        for version_data in self.app.versions.values():
            verse_texts.extend(list(version_data.values())[:200])
        
        self.llm = StandaloneQuantumLLM(
            kernel=self.app.kernel,
            source_texts=verse_texts[:200] if verse_texts else ["God is love", "Jesus said", "The Bible"]
        )
        
        self.output_dir = "red_letters_book"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _generate_full_chapter(self, chapter_num: int, title: str, theme: str, 
                               key_sayings: list, pages: int) -> str:
        """Generate actual full chapter content"""
        print(f"\n{'='*80}")
        print(f"Generating Chapter {chapter_num}: {title}")
        print(f"{'='*80}")
        
        # Build sayings context
        sayings_context = []
        for ref, text in key_sayings:
            sayings_context.append(f"{ref}: {text}")
        
        sayings_text = "\n\n".join(sayings_context)
        
        # Get cross-references for first saying
        cross_refs_text = ""
        if key_sayings:
            first_ref = key_sayings[0][0]
            try:
                book, chapter, verse = self._parse_ref(first_ref)
                if book:
                    result = self.app.discover_cross_references(book, chapter, verse, top_k=5)
                    cross_refs = result.get('cross_references', [])[:3]
                    if cross_refs:
                        cross_refs_text = "\n".join([
                            f"- {cr['reference']}: {cr.get('summary', cr.get('text', ''))[:100]}"
                            for cr in cross_refs
                        ])
            except:
                pass
        
        # Generate chapter
        word_count = pages * 500
        prompt = f"""Write a complete, full chapter for a book called "Red Letters: How Jesus' Words Reveal the Way to Relationship with God."

CHAPTER TITLE: {title}

THEME: {theme}

TARGET LENGTH: Approximately {word_count} words ({pages} pages)

JESUS' KEY SAYINGS (The Red Letters):
{sayings_text}

RELATED VERSES:
{cross_refs_text if cross_refs_text else "Explore connections throughout Scripture"}

INSTRUCTIONS:
Write a COMPLETE, FULL chapter (not an outline or summary). The chapter should:

1. Begin with an engaging introduction (2-3 paragraphs) that draws readers into the topic
2. Explain what Jesus said in these key sayings and what they mean (3-4 paragraphs)
3. Show how these sayings relate to the Old Testament - prophecies, themes, connections (2-3 paragraphs)
4. Show how they relate to the rest of the New Testament (2-3 paragraphs)
5. Explore the relationships revealed: with God, with others, with self (3-4 paragraphs)
6. Explain how these sayings show "the way" to relationship with God (2-3 paragraphs)
7. Include practical implications for living in relationship (2-3 paragraphs)
8. End with a thoughtful conclusion that ties back to the theme (1-2 paragraphs)

WRITING STYLE:
- Write in an accessible but thoughtful style
- Use clear, engaging prose
- Include specific examples and illustrations
- Make connections explicit
- Write as if you're explaining to someone who wants to understand deeply
- Be warm and inviting, not dry or academic
- Stay grounded in the actual words of Jesus provided

IMPORTANT: Write the ACTUAL CHAPTER CONTENT, not instructions or an outline. Write {word_count} words of actual prose that someone can read as a complete chapter."""
        
        print(f"  Generating {word_count} words of content...")
        
        try:
            result = self.llm.generate_grounded(
                prompt,
                max_length=word_count + 500,  # Allow some extra
                require_validation=True
            )
            
            content = result.get('generated', '')
            
            if not content or len(content) < 1000:
                print(f"  Warning: Generated content too short ({len(content)} chars), using fallback...")
                content = self._fallback_chapter(title, theme, sayings_text, word_count)
            
            # Ensure it starts with the title
            if not content.startswith('#'):
                content = f"# {title}\n\n{content}"
            
            print(f"  Generated {len(content)} characters ({len(content.split())} words)")
            return content
            
        except Exception as e:
            print(f"  Error: {e}")
            print(f"  Using fallback content...")
            return self._fallback_chapter(title, theme, sayings_text, word_count)
    
    def _fallback_chapter(self, title: str, theme: str, sayings: str, target_words: int) -> str:
        """Generate fallback chapter if AI fails"""
        content = f"# {title}\n\n"
        
        content += f"## Introduction\n\n"
        content += f"In the Gospels, Jesus' words are often printed in red - the 'red letters.' These words are not mere historical records or moral teachings. They are the very words of life, revealing the way to relationship with God. In this chapter, we explore how Jesus' words about {theme.lower()} show us the path to deeper relationship with God and with others.\n\n"
        
        content += f"## Jesus' Words: The Red Letters\n\n"
        for saying in sayings.split('\n\n')[:5]:
            content += f"{saying}\n\n"
        
        content += f"## What Jesus Meant\n\n"
        content += f"Jesus' words here reveal profound truth about {theme.lower()}. These sayings are not isolated teachings but part of a larger narrative that spans all of Scripture. They show us who God is, who we are, and how we can enter into relationship with the Creator.\n\n"
        
        content += f"## Connections to the Old Testament\n\n"
        content += f"These words of Jesus echo themes found throughout the Old Testament. They fulfill prophecies, reveal God's character, and show how God's plan has been unfolding since the beginning. The Old Testament points forward to Jesus, and Jesus' words point back to show how He fulfills all that was promised.\n\n"
        
        content += f"## Connections to the New Testament\n\n"
        content += f"Jesus' words here form the foundation for much of what follows in the New Testament. The apostles and early church built upon these teachings, showing how they apply to life, community, and mission. These red letters are not just for Jesus' immediate audience but for all who would follow Him.\n\n"
        
        content += f"## The Relationships Revealed\n\n"
        content += f"Through these words, Jesus reveals different dimensions of relationship: our relationship with God the Father, our relationship with Jesus the Son, our relationship with the Holy Spirit, and our relationships with one another. Each saying illuminates a different aspect of how we are called to live in relationship.\n\n"
        
        content += f"## The Way to Relationship\n\n"
        content += f"Jesus said, 'I am the way, and the truth, and the life: no one cometh unto the Father, but by me' (John 14:6). These words show us that relationship with God is not achieved through our own efforts but through Jesus. He is the way, and His words guide us along that path.\n\n"
        
        content += f"## Practical Implications\n\n"
        content += f"What does this mean for how we live? Jesus' words are not just theological concepts but practical guidance for daily life. They show us how to pray, how to love, how to serve, how to follow. As we apply these words, we discover what it means to live in relationship with God.\n\n"
        
        content += f"## Conclusion\n\n"
        content += f"Jesus' words in this chapter point us to a central truth: God desires relationship with us, and Jesus is the way to that relationship. These red letters are not just words on a page but invitations into life itself - life in relationship with the God who created us, loves us, and calls us to Himself.\n\n"
        
        return content
    
    def _parse_ref(self, ref: str):
        """Parse verse reference"""
        import re
        # Handle ranges
        if '-' in ref:
            ref = ref.split('-')[0]
        
        match = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
        if match:
            return match.group(1).strip(), int(match.group(2)), int(match.group(3))
        return None, 0, 0
    
    def generate_full_book(self):
        """Generate the complete book with actual content"""
        print("\n" + "="*80)
        print("GENERATING FULL 'RED LETTERS' BOOK")
        print("="*80)
        print("\nThis will generate ACTUAL chapter content, not just prompts.")
        print("This may take a while as each chapter is fully written...\n")
        
        chapters_data = [
            {
                "number": 1, "title": "Introduction: The Words of Life",
                "theme": "Why Jesus' words matter and how they reveal relationship with God",
                "key_sayings": [
                    ("John 6:63", "The words that I have spoken unto you are spirit, and are life."),
                    ("John 14:6", "I am the way, and the truth, and the life: no one cometh unto the Father, but by me."),
                    ("Matthew 7:24", "Every one therefore that heareth these words of mine, and doeth them, shall be likened unto a wise man.")
                ],
                "pages": 8
            },
            {
                "number": 2, "title": "The Relationship with the Father",
                "theme": "Jesus reveals how to know God as Father",
                "key_sayings": [
                    ("John 14:9", "He that hath seen me hath seen the Father"),
                    ("Matthew 6:9", "Our Father who art in heaven"),
                    ("John 17:3", "This is life eternal, that they should know thee the only true God"),
                    ("Matthew 11:27", "No one knoweth the Son, save the Father; neither doth any know the Father, save the Son")
                ],
                "pages": 12
            },
            # Add more chapters as needed - for now generating first 2 as proof of concept
        ]
        
        all_chapters = []
        
        for chapter_data in chapters_data:
            content = self._generate_full_chapter(
                chapter_data["number"],
                chapter_data["title"],
                chapter_data["theme"],
                chapter_data["key_sayings"],
                chapter_data["pages"]
            )
            
            # Save individual chapter
            safe_title = chapter_data['title'].lower().replace(' ', '_').replace(':', '').replace("'", "").replace(",", "")
            filename = f"chapter_{chapter_data['number']:02d}_{safe_title}.md"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  Saved: {filename}")
            
            all_chapters.append({
                "number": chapter_data["number"],
                "title": chapter_data["title"],
                "file": filename,
                "word_count": len(content.split())
            })
        
        print(f"\n{'='*80}")
        print("GENERATION COMPLETE!")
        print(f"{'='*80}")
        print(f"\nGenerated {len(all_chapters)} chapters")
        print(f"Check the files in: {self.output_dir}/")
        print("\nNote: This is a proof of concept. To generate all 20 chapters,")
        print("the script would need to be run for all chapters (takes time).")


if __name__ == "__main__":
    generator = FullRedLettersBookGenerator()
    generator.generate_full_book()