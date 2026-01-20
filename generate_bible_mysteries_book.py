"""
Generate "The Mysteries of the Bible" Book
A comprehensive 150-200 page exploration of biblical mysteries
Uses AI-powered analysis with grounded generation
"""
import os
import json
from typing import List, Dict, Tuple
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from quantum_llm_standalone import StandaloneQuantumLLM
from load_bible_from_html import load_bible_version


class BibleMysteriesBookGenerator:
    """
    Generates a comprehensive book about biblical mysteries
    Uses AI to explore mysteries while staying grounded in Scripture
    """
    
    def __init__(self):
        """Initialize the book generator"""
        print("Initializing Bible Mysteries Book Generator...")
        
        # Initialize Bible app
        self.app = HyperlinkedBibleApp()
        
        # Initialize LLM for content generation
        self.llm = StandaloneQuantumLLM(
            kernel=self.app.kernel,
            source_texts=list(self.app.versions.get('asv', {}).values())[:100] if self.app.versions else ["God is love"]
        )
        
        # Book structure
        self.chapters = self._define_chapter_structure()
        
        # Output directory
        self.output_dir = "bible_mysteries_book"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _define_chapter_structure(self) -> List[Dict]:
        """Define the book's chapter structure"""
        return [
            {
                "number": 1,
                "title": "Introduction: The Mystery of Divine Revelation",
                "theme": "How God reveals Himself through Scripture",
                "key_verses": ["John 1:1", "2 Timothy 3:16", "Hebrews 4:12"],
                "pages": 8
            },
            {
                "number": 2,
                "title": "The Mystery of the Trinity",
                "theme": "One God in three persons",
                "key_verses": ["Matthew 28:19", "John 14:26", "2 Corinthians 13:14", "Genesis 1:26"],
                "pages": 12
            },
            {
                "number": 3,
                "title": "The Mystery of Creation",
                "theme": "How God created the universe and humanity",
                "key_verses": ["Genesis 1:1", "John 1:3", "Colossians 1:16", "Hebrews 11:3"],
                "pages": 10
            },
            {
                "number": 4,
                "title": "The Mystery of the Fall",
                "theme": "Original sin and its consequences",
                "key_verses": ["Genesis 3:1-24", "Romans 5:12", "1 Corinthians 15:22"],
                "pages": 10
            },
            {
                "number": 5,
                "title": "The Mystery of the Incarnation",
                "theme": "God becoming man in Jesus Christ",
                "key_verses": ["John 1:14", "Philippians 2:5-11", "1 Timothy 3:16", "Colossians 2:9"],
                "pages": 12
            },
            {
                "number": 6,
                "title": "The Mystery of the Atonement",
                "theme": "How Christ's death saves humanity",
                "key_verses": ["Romans 3:23-26", "2 Corinthians 5:21", "1 Peter 2:24", "Hebrews 9:22"],
                "pages": 12
            },
            {
                "number": 7,
                "title": "The Mystery of the Resurrection",
                "theme": "Christ's victory over death",
                "key_verses": ["1 Corinthians 15:3-8", "Romans 6:4", "1 Peter 1:3", "John 11:25"],
                "pages": 10
            },
            {
                "number": 8,
                "title": "The Mystery of the Holy Spirit",
                "theme": "The third person of the Trinity",
                "key_verses": ["John 14:16-17", "Acts 2:1-4", "Romans 8:26", "1 Corinthians 12:4-11"],
                "pages": 12
            },
            {
                "number": 9,
                "title": "The Mystery of Predestination and Free Will",
                "theme": "God's sovereignty and human responsibility",
                "key_verses": ["Ephesians 1:4-5", "Romans 8:29-30", "John 6:44", "2 Peter 3:9"],
                "pages": 14
            },
            {
                "number": 10,
                "title": "The Mystery of Suffering",
                "theme": "Why God allows pain and evil",
                "key_verses": ["Job 1:1-22", "Romans 8:18", "2 Corinthians 12:7-10", "James 1:2-4"],
                "pages": 12
            },
            {
                "number": 11,
                "title": "The Mystery of Prayer",
                "theme": "How prayer works and why it matters",
                "key_verses": ["Matthew 6:9-13", "James 5:16", "Philippians 4:6-7", "1 John 5:14-15"],
                "pages": 10
            },
            {
                "number": 12,
                "title": "The Mystery of Faith",
                "theme": "What faith is and how it transforms",
                "key_verses": ["Hebrews 11:1", "Ephesians 2:8-9", "James 2:14-26", "Romans 10:17"],
                "pages": 10
            },
            {
                "number": 13,
                "title": "The Mystery of Grace",
                "theme": "God's unmerited favor",
                "key_verses": ["Ephesians 2:8", "Romans 3:24", "Titus 2:11", "2 Corinthians 12:9"],
                "pages": 10
            },
            {
                "number": 14,
                "title": "The Mystery of the Church",
                "theme": "The body of Christ on earth",
                "key_verses": ["Ephesians 1:22-23", "1 Corinthians 12:12-27", "Matthew 16:18", "Acts 2:42-47"],
                "pages": 10
            },
            {
                "number": 15,
                "title": "The Mystery of the End Times",
                "theme": "Eschatology and God's ultimate plan",
                "key_verses": ["1 Thessalonians 4:16-17", "Revelation 21:1-4", "Matthew 24:36", "2 Peter 3:10"],
                "pages": 14
            },
            {
                "number": 16,
                "title": "The Mystery of Prophecy",
                "theme": "How God speaks through prophets",
                "key_verses": ["2 Peter 1:20-21", "Isaiah 53", "Micah 5:2", "Jeremiah 1:4-10"],
                "pages": 10
            },
            {
                "number": 17,
                "title": "The Mystery of Miracles",
                "theme": "Divine intervention in the natural world",
                "key_verses": ["John 2:1-11", "Mark 4:35-41", "Acts 3:1-10", "1 Corinthians 12:10"],
                "pages": 10
            },
            {
                "number": 18,
                "title": "The Mystery of Divine Providence",
                "theme": "How God works all things for good",
                "key_verses": ["Romans 8:28", "Genesis 50:20", "Proverbs 16:9", "Ephesians 1:11"],
                "pages": 10
            },
            {
                "number": 19,
                "title": "The Mystery of the Kingdom of God",
                "theme": "God's reign in heaven and on earth",
                "key_verses": ["Matthew 6:10", "Luke 17:20-21", "Revelation 11:15", "Colossians 1:13"],
                "pages": 10
            },
            {
                "number": 20,
                "title": "Conclusion: The Mystery of God's Love",
                "theme": "How all mysteries point to God's love",
                "key_verses": ["John 3:16", "Romans 8:38-39", "1 John 4:8", "Ephesians 3:18-19"],
                "pages": 8
            }
        ]
    
    def _parse_reference(self, ref: str) -> Tuple[str, int, int]:
        """Parse a verse reference like 'John 3:16'"""
        import re
        match = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
        if match:
            book = match.group(1).strip()
            chapter = int(match.group(2))
            verse = int(match.group(3))
            return book, chapter, verse
        return None, 0, 0
    
    def _get_verse_text(self, ref: str, version: str = "asv") -> str:
        """Get verse text from reference"""
        book, chapter, verse = self._parse_reference(ref)
        if book:
            return self.app.get_verse_text(book, chapter, verse, version)
        return ""
    
    def _get_cross_references(self, ref: str, top_k: int = 5) -> List[Dict]:
        """Get cross-references for a verse"""
        book, chapter, verse = self._parse_reference(ref)
        if book:
            result = self.app.discover_cross_references(book, chapter, verse, top_k=top_k)
            return result.get('cross_references', [])
        return []
    
    def _generate_chapter_content(self, chapter: Dict) -> str:
        """Generate content for a single chapter"""
        print(f"\nGenerating Chapter {chapter['number']}: {chapter['title']}...")
        
        # Collect verse texts
        verse_texts = []
        for ref in chapter['key_verses']:
            text = self._get_verse_text(ref)
            if text:
                verse_texts.append(f"{ref}: {text}")
        
        # Collect cross-references
        all_cross_refs = []
        for ref in chapter['key_verses'][:3]:  # Use first 3 for cross-refs
            cross_refs = self._get_cross_references(ref, top_k=3)
            all_cross_refs.extend(cross_refs)
        
        # Build context
        context = "\n\n".join(verse_texts)
        
        # Generate chapter content
        prompt = f"""Write a comprehensive chapter for a book about biblical mysteries.

Chapter Title: {chapter['title']}
Theme: {chapter['theme']}
Target Length: Approximately {chapter['pages']} pages (about {chapter['pages'] * 500} words)

Key Bible Verses:
{context}

Cross-References Found:
{chr(10).join([f"- {cr['reference']}: {cr['summary']}" for cr in all_cross_refs[:5]])}

Instructions:
1. Begin with an engaging introduction that draws readers into the mystery
2. Explain the mystery clearly, using the key verses provided
3. Explore how this mystery relates to the overall biblical narrative
4. Discuss different perspectives and interpretations (when appropriate)
5. Show how this mystery connects to other biblical mysteries
6. Include practical implications for faith and life
7. End with a thoughtful conclusion that ties back to the theme
8. Use the cross-references to show connections throughout Scripture
9. Write in an accessible but thoughtful style
10. Stay grounded in the actual Bible text provided

The chapter should be approximately {chapter['pages'] * 500} words, well-structured with clear sections."""
        
        try:
            result = self.llm.generate_grounded(
                prompt,
                max_length=chapter['pages'] * 600,  # Allow more words
                require_validation=True
            )
            
            content = result.get('generated', '')
            if not content or len(content) < 500:
                # Fallback to simpler generation
                content = self._generate_fallback_chapter(chapter, verse_texts)
            
            return content
        except Exception as e:
            print(f"Error generating chapter {chapter['number']}: {e}")
            return self._generate_fallback_chapter(chapter, verse_texts)
    
    def _generate_fallback_chapter(self, chapter: Dict, verse_texts: List[str]) -> str:
        """Generate a simpler chapter if AI generation fails"""
        content = f"# {chapter['title']}\n\n"
        content += f"## Introduction\n\n"
        content += f"The mystery of {chapter['theme'].lower()} is one of the most profound aspects of biblical revelation. "
        content += f"This chapter explores how this mystery unfolds throughout Scripture and its significance for our understanding of God and faith.\n\n"
        
        content += f"## Key Biblical Passages\n\n"
        for verse_text in verse_texts[:5]:
            content += f"{verse_text}\n\n"
        
        content += f"## Exploring the Mystery\n\n"
        content += f"The biblical text reveals {chapter['theme'].lower()} as a central theme that connects "
        content += f"throughout the Old and New Testaments. As we examine the passages above, we see how "
        content += f"this mystery relates to God's overall plan for humanity and creation.\n\n"
        
        content += f"## Connections to the Whole\n\n"
        content += f"This mystery is not isolated but connects to other biblical mysteries. "
        content += f"It reveals God's character, His purposes, and His relationship with humanity. "
        content += f"Understanding this mystery helps us see the coherence and beauty of God's revelation.\n\n"
        
        content += f"## Conclusion\n\n"
        content += f"The mystery of {chapter['theme'].lower()} invites us into deeper relationship with God. "
        content += f"As we explore this mystery, we find that it points to the ultimate mystery: "
        content += f"God's infinite love for His creation.\n\n"
        
        return content
    
    def generate_book(self):
        """Generate the complete book"""
        print("=" * 80)
        print("GENERATING 'THE MYSTERIES OF THE BIBLE' BOOK")
        print("=" * 80)
        print(f"\nTotal Chapters: {len(self.chapters)}")
        print(f"Estimated Pages: {sum(c['pages'] for c in self.chapters)}")
        print(f"Output Directory: {self.output_dir}\n")
        
        # Generate table of contents
        toc = self._generate_table_of_contents()
        
        # Generate introduction
        introduction = self._generate_introduction()
        
        # Generate each chapter
        chapters_content = []
        for chapter in self.chapters:
            chapter_content = self._generate_chapter_content(chapter)
            chapters_content.append({
                "number": chapter['number'],
                "title": chapter['title'],
                "content": chapter_content
            })
        
        # Generate conclusion
        conclusion = self._generate_conclusion()
        
        # Compile book
        book_content = self._compile_book(toc, introduction, chapters_content, conclusion)
        
        # Save book
        self._save_book(book_content, chapters_content)
        
        print("\n" + "=" * 80)
        print("BOOK GENERATION COMPLETE!")
        print("=" * 80)
        print(f"\nBook saved to: {self.output_dir}/")
        print(f"- Full book: bible_mysteries_book.md")
        print(f"- Individual chapters: chapter_*.md")
        print(f"- Metadata: book_metadata.json")
    
    def _generate_table_of_contents(self) -> str:
        """Generate table of contents"""
        toc = "# Table of Contents\n\n"
        for chapter in self.chapters:
            toc += f"{chapter['number']}. {chapter['title']} ({chapter['pages']} pages)\n"
        return toc
    
    def _generate_introduction(self) -> str:
        """Generate book introduction"""
        prompt = """Write an engaging introduction for a book titled "The Mysteries of the Bible: How Divine Mysteries Reveal God's Grand Design."

The introduction should:
1. Explain why biblical mysteries matter
2. Set the tone for the book (thoughtful, accessible, reverent)
3. Explain the approach (exploring mysteries through Scripture itself)
4. Invite readers into a journey of discovery
5. Be approximately 3-4 pages (1500-2000 words)

Write in a style that is both scholarly and accessible, suitable for both new and experienced Bible readers."""
        
        try:
            result = self.llm.generate_grounded(prompt, max_length=2000, require_validation=True)
            return result.get('generated', self._default_introduction())
        except:
            return self._default_introduction()
    
    def _default_introduction(self) -> str:
        """Default introduction if generation fails"""
        return """# Introduction: The Mystery of Divine Revelation

The Bible is a book of mysteries. Not mysteries in the sense of puzzles to be solved, but mysteries in the sense of profound truths that transcend human understanding yet invite us into deeper relationship with God.

Throughout Scripture, we encounter mysteries that reveal God's character, His purposes, and His love for humanity. These mysteries are not meant to confuse us, but to draw us closer to the infinite God who has chosen to reveal Himself to finite creatures.

This book explores twenty key mysteries of the Bible, showing how each one connects to the whole of Scripture and points to God's grand design. We will see how these mysteries are not isolated concepts but interconnected threads in the tapestry of divine revelation.

As we journey through these mysteries together, may we be drawn into deeper wonder, worship, and relationship with the God who has revealed Himself through His Word."""
    
    def _generate_conclusion(self) -> str:
        """Generate book conclusion"""
        prompt = """Write a thoughtful conclusion for "The Mysteries of the Bible" that:
1. Summarizes how all the mysteries connect
2. Shows how they point to God's love
3. Invites readers into continued exploration
4. Is approximately 2-3 pages (1000-1500 words)

Write in a style that is inspiring and reflective."""
        
        try:
            result = self.llm.generate_grounded(prompt, max_length=1500, require_validation=True)
            return result.get('generated', self._default_conclusion())
        except:
            return self._default_conclusion()
    
    def _default_conclusion(self) -> str:
        """Default conclusion if generation fails"""
        return """# Conclusion: The Mystery of God's Love

As we have journeyed through the mysteries of the Bible, we have seen how each mystery, while profound in itself, connects to the greater story of God's love for His creation.

From the mystery of the Trinity to the mystery of the end times, from the mystery of grace to the mystery of suffering, all these mysteries ultimately point to one central truth: God is love, and He has revealed Himself to us through His Word.

These mysteries are not meant to be fully comprehended, but to be embraced. They invite us into a relationship with the infinite God who has chosen to make Himself known to us. As we continue to explore these mysteries, may we be drawn ever deeper into wonder, worship, and love for the God who has revealed Himself through Scripture.

The journey through biblical mysteries is not one that ends with the last page of this book, but one that continues throughout our lives as we grow in relationship with God and understanding of His Word."""
    
    def _compile_book(self, toc: str, introduction: str, chapters: List[Dict], conclusion: str) -> str:
        """Compile the complete book"""
        book = f"""# The Mysteries of the Bible: How Divine Mysteries Reveal God's Grand Design

*Generated using AI-powered biblical analysis*
*Date: {datetime.now().strftime('%B %d, %Y')}*

---

{toc}

---

{introduction}

---

"""
        
        for chapter in chapters:
            book += f"\n\n# Chapter {chapter['number']}: {chapter['title']}\n\n"
            book += chapter['content']
            book += "\n\n---\n\n"
        
        book += f"\n\n{conclusion}\n\n"
        
        book += f"\n\n---\n\n## About This Book\n\n"
        book += "This book was generated using AI-powered analysis of the Bible, "
        book += "ensuring all content is grounded in actual Scripture. "
        book += "The mysteries explored are based on key biblical passages and their "
        book += "connections throughout the entire Bible.\n\n"
        
        return book
    
    def _save_book(self, full_book: str, chapters: List[Dict]):
        """Save the book to files"""
        # Save full book
        with open(os.path.join(self.output_dir, "bible_mysteries_book.md"), 'w', encoding='utf-8') as f:
            f.write(full_book)
        
        # Save individual chapters
        for chapter in chapters:
            filename = f"chapter_{chapter['number']:02d}_{chapter['title'].lower().replace(' ', '_').replace(':', '')[:50]}.md"
            with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(f"# {chapter['title']}\n\n{chapter['content']}")
        
        # Save metadata
        metadata = {
            "title": "The Mysteries of the Bible: How Divine Mysteries Reveal God's Grand Design",
            "generated_date": datetime.now().isoformat(),
            "total_chapters": len(self.chapters),
            "estimated_pages": sum(c['pages'] for c in self.chapters),
            "chapters": [
                {
                    "number": c['number'],
                    "title": c['title'],
                    "theme": c['theme'],
                    "pages": c['pages']
                }
                for c in self.chapters
            ]
        }
        
        with open(os.path.join(self.output_dir, "book_metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)


def main():
    """Main function"""
    print("=" * 80)
    print("BIBLE MYSTERIES BOOK GENERATOR")
    print("=" * 80)
    print("\nThis will generate a 150-200 page book exploring biblical mysteries.")
    print("The process may take some time as it generates each chapter.")
    print("\nStarting generation...\n")
    
    try:
        generator = BibleMysteriesBookGenerator()
        generator.generate_book()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()