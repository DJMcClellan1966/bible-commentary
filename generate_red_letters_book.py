"""
Generate "Red Letters" Book
A comprehensive exploration of Jesus' words from the Gospels
and how they relate to the whole Bible and reveal the way to relationship with God
"""
import os
import json
import re
from typing import List, Dict, Tuple
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from quantum_llm_standalone import StandaloneQuantumLLM
from load_bible_from_html import load_bible_version


class RedLettersBookGenerator:
    """
    Generates a book exploring Jesus' words (the "red letters")
    and their relationship to the whole Bible
    """
    
    def __init__(self):
        """Initialize the book generator"""
        print("Initializing Red Letters Book Generator...")
        
        # Initialize Bible app
        self.app = HyperlinkedBibleApp()
        
        # Initialize LLM for content generation
        self.llm = StandaloneQuantumLLM(
            kernel=self.app.kernel,
            source_texts=list(self.app.versions.get('asv', {}).values())[:100] if self.app.versions else ["God is love"]
        )
        
        # Jesus' key sayings organized by theme
        self.chapters = self._define_chapter_structure()
        
        # Output directory
        self.output_dir = "red_letters_book"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _define_chapter_structure(self) -> List[Dict]:
        """Define the book's chapter structure based on Jesus' key sayings"""
        return [
            {
                "number": 1,
                "title": "Introduction: The Words of Life",
                "theme": "Why Jesus' words matter and how they reveal relationship with God",
                "key_sayings": [
                    ("John 6:63", "The words that I have spoken unto you are spirit, and are life."),
                    ("John 14:6", "I am the way, and the truth, and the life: no one cometh unto the Father, but by me."),
                    ("Matthew 7:24", "Every one therefore that heareth these words of mine, and doeth them, shall be likened unto a wise man.")
                ],
                "pages": 8
            },
            {
                "number": 2,
                "title": "The Relationship with the Father",
                "theme": "Jesus reveals how to know God as Father",
                "key_sayings": [
                    ("John 14:9", "He that hath seen me hath seen the Father"),
                    ("Matthew 6:9", "Our Father who art in heaven"),
                    ("John 17:3", "This is life eternal, that they should know thee the only true God"),
                    ("Matthew 11:27", "No one knoweth the Son, save the Father; neither doth any know the Father, save the Son")
                ],
                "pages": 12
            },
            {
                "number": 3,
                "title": "The Relationship with the Son",
                "theme": "Who Jesus is and what it means to follow Him",
                "key_sayings": [
                    ("John 8:12", "I am the light of the world"),
                    ("John 10:11", "I am the good shepherd"),
                    ("John 11:25", "I am the resurrection, and the life"),
                    ("Matthew 16:24", "If any man would come after me, let him deny himself, and take up his cross, and follow me")
                ],
                "pages": 12
            },
            {
                "number": 4,
                "title": "The Relationship with the Holy Spirit",
                "theme": "Jesus' teaching about the Helper and Comforter",
                "key_sayings": [
                    ("John 14:16", "I will pray the Father, and he shall give you another Comforter"),
                    ("John 14:26", "The Comforter, even the Holy Spirit, whom the Father will send in my name"),
                    ("John 16:13", "When he, the Spirit of truth, is come, he shall guide you into all the truth"),
                    ("John 3:5", "Except one be born of water and the Spirit, he cannot enter into the kingdom of God")
                ],
                "pages": 10
            },
            {
                "number": 5,
                "title": "The Relationship with Others: Love Your Neighbor",
                "theme": "Jesus' command to love others",
                "key_sayings": [
                    ("John 13:34", "A new commandment I give unto you, that ye love one another"),
                    ("Matthew 22:39", "Thou shalt love thy neighbor as thyself"),
                    ("Matthew 5:44", "Love your enemies, and pray for them that persecute you"),
                    ("John 15:13", "Greater love hath no man than this, that a man lay down his life for his friends")
                ],
                "pages": 12
            },
            {
                "number": 6,
                "title": "The Relationship with Self: Identity in Christ",
                "theme": "Who we are in relationship with Jesus",
                "key_sayings": [
                    ("John 15:5", "I am the vine, ye are the branches"),
                    ("Matthew 5:14", "Ye are the light of the world"),
                    ("John 1:12", "As many as received him, to them gave he the right to become children of God"),
                    ("Matthew 5:48", "Ye therefore shall be perfect, as your heavenly Father is perfect")
                ],
                "pages": 10
            },
            {
                "number": 7,
                "title": "The Way: Following Jesus",
                "theme": "What it means to follow Jesus",
                "key_sayings": [
                    ("John 14:6", "I am the way, and the truth, and the life"),
                    ("Matthew 7:13", "Enter ye in by the narrow gate"),
                    ("John 10:9", "I am the door: by me if any man enter in, he shall be saved"),
                    ("Matthew 4:19", "Follow me, and I will make you fishers of men")
                ],
                "pages": 12
            },
            {
                "number": 8,
                "title": "The Truth: Jesus' Teaching",
                "theme": "Jesus as the source of truth",
                "key_sayings": [
                    ("John 8:32", "Ye shall know the truth, and the truth shall make you free"),
                    ("John 18:37", "To this end have I been born, and to this end am I come into the world, that I should bear witness unto the truth"),
                    ("Matthew 5:17", "Think not that I came to destroy the law or the prophets"),
                    ("John 5:39", "Ye search the scriptures, because ye think that in them ye have eternal life")
                ],
                "pages": 12
            },
            {
                "number": 9,
                "title": "The Life: Abundant Life in Christ",
                "theme": "Jesus' promise of abundant life",
                "key_sayings": [
                    ("John 10:10", "I came that they may have life, and may have it abundantly"),
                    ("John 6:35", "I am the bread of life"),
                    ("John 4:14", "Whosoever drinketh of the water that I shall give him shall never thirst"),
                    ("John 11:25", "I am the resurrection, and the life")
                ],
                "pages": 10
            },
            {
                "number": 10,
                "title": "The Kingdom: Living in God's Kingdom",
                "theme": "Jesus' teaching about the kingdom of God",
                "key_sayings": [
                    ("Matthew 6:33", "Seek ye first his kingdom, and his righteousness"),
                    ("Luke 17:21", "The kingdom of God is within you"),
                    ("Matthew 5:3", "Blessed are the poor in spirit: for theirs is the kingdom of heaven"),
                    ("Mark 1:15", "The time is fulfilled, and the kingdom of God is at hand")
                ],
                "pages": 12
            },
            {
                "number": 11,
                "title": "The Prayer: Relationship Through Prayer",
                "theme": "Jesus' teaching on prayer",
                "key_sayings": [
                    ("Matthew 6:9", "After this manner therefore pray ye: Our Father"),
                    ("John 14:13", "Whatsoever ye shall ask in my name, that will I do"),
                    ("Matthew 7:7", "Ask, and it shall be given you; seek, and ye shall find"),
                    ("Luke 18:1", "Men ought always to pray, and not to faint")
                ],
                "pages": 10
            },
            {
                "number": 12,
                "title": "The Faith: Trusting in Jesus",
                "theme": "What Jesus says about faith",
                "key_sayings": [
                    ("Mark 11:22", "Have faith in God"),
                    ("Matthew 17:20", "If ye have faith as a grain of mustard seed"),
                    ("John 20:29", "Blessed are they that have not seen, and yet have believed"),
                    ("Matthew 9:22", "Thy faith hath made thee whole")
                ],
                "pages": 10
            },
            {
                "number": 13,
                "title": "The Forgiveness: Receiving and Giving Forgiveness",
                "theme": "Jesus' teaching on forgiveness",
                "key_sayings": [
                    ("Matthew 6:14", "If ye forgive men their trespasses, your heavenly Father will also forgive you"),
                    ("Luke 23:34", "Father, forgive them; for they know not what they do"),
                    ("Matthew 18:22", "I say not unto thee, Until seven times; but, Until seventy times seven"),
                    ("Mark 11:25", "Whensoever ye stand praying, forgive, if ye have aught against any one")
                ],
                "pages": 10
            },
            {
                "number": 14,
                "title": "The Service: Serving Others as Jesus Served",
                "theme": "Jesus' example and teaching on service",
                "key_sayings": [
                    ("Matthew 20:28", "The Son of man came not to be ministered unto, but to minister"),
                    ("John 13:14", "If I then, the Lord and the Teacher, have washed your feet, ye also ought to wash one another's feet"),
                    ("Matthew 25:40", "Inasmuch as ye did it unto one of these my brethren, even these least, ye did it unto me"),
                    ("Mark 10:45", "For the Son of man also came not to be ministered unto, but to minister")
                ],
                "pages": 10
            },
            {
                "number": 15,
                "title": "The Cross: The Cost of Relationship",
                "theme": "Jesus' teaching about taking up the cross",
                "key_sayings": [
                    ("Matthew 16:24", "If any man would come after me, let him deny himself, and take up his cross"),
                    ("John 12:24", "Except a grain of wheat fall into the earth and die, it abideth by itself alone"),
                    ("Matthew 10:38", "He that doth not take his cross and follow after me, is not worthy of me"),
                    ("Luke 9:23", "If any man would come after me, let him deny himself, and take up his cross daily")
                ],
                "pages": 12
            },
            {
                "number": 16,
                "title": "The Resurrection: New Life in Relationship",
                "theme": "Jesus' promise of resurrection and new life",
                "key_sayings": [
                    ("John 11:25", "I am the resurrection, and the life: he that believeth on me, though he die, yet shall he live"),
                    ("John 14:19", "Because I live, ye shall live also"),
                    ("Matthew 28:20", "Lo, I am with you always, even unto the end of the world"),
                    ("John 6:40", "This is the will of my Father, that every one that beholdeth the Son, and believeth on him, should have eternal life")
                ],
                "pages": 10
            },
            {
                "number": 17,
                "title": "The Parables: Stories of Relationship",
                "theme": "How Jesus' parables reveal relationships",
                "key_sayings": [
                    ("Matthew 13:11", "Unto you it is given to know the mysteries of the kingdom of heaven"),
                    ("Luke 15:11-32", "The Parable of the Prodigal Son"),
                    ("Matthew 13:3", "Behold, the sower went forth to sow"),
                    ("Luke 10:30", "A certain man went down from Jerusalem to Jericho")
                ],
                "pages": 14
            },
            {
                "number": 18,
                "title": "The Beatitudes: The Character of Relationship",
                "theme": "The Beatitudes as a path to relationship with God",
                "key_sayings": [
                    ("Matthew 5:3-12", "Blessed are the poor in spirit..."),
                    ("Luke 6:20-23", "Blessed are ye poor..."),
                    ("Matthew 5:8", "Blessed are the pure in heart: for they shall see God"),
                    ("Matthew 5:6", "Blessed are they that hunger and thirst after righteousness")
                ],
                "pages": 12
            },
            {
                "number": 19,
                "title": "The Great Commission: Relationship Multiplied",
                "theme": "Jesus' command to make disciples",
                "key_sayings": [
                    ("Matthew 28:19", "Go ye therefore, and make disciples of all the nations"),
                    ("Mark 16:15", "Go ye into all the world, and preach the gospel to the whole creation"),
                    ("John 20:21", "As the Father hath sent me, even so send I you"),
                    ("Acts 1:8", "Ye shall be my witnesses")
                ],
                "pages": 10
            },
            {
                "number": 20,
                "title": "Conclusion: The Red Letters and the Whole Story",
                "theme": "How Jesus' words connect to all of Scripture and reveal the way to God",
                "key_sayings": [
                    ("John 5:39", "Ye search the scriptures, because ye think that in them ye have eternal life; and these are they which bear witness of me"),
                    ("Luke 24:27", "Beginning from Moses and from all the prophets, he interpreted to them in all the scriptures the things concerning himself"),
                    ("John 14:6", "I am the way, and the truth, and the life: no one cometh unto the Father, but by me"),
                    ("John 15:15", "No longer do I call you servants... but I have called you friends")
                ],
                "pages": 10
            }
        ]
    
    def _parse_reference(self, ref: str) -> Tuple[str, int, int]:
        """Parse a verse reference"""
        # Handle ranges like "Matthew 5:3-12"
        if '-' in ref:
            ref = ref.split('-')[0]
        
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
            text = self.app.get_verse_text(book, chapter, verse, version)
            if not text:
                # Try to get from the saying tuple if provided
                return ""
            return text
        return ""
    
    def _get_cross_references(self, ref: str, top_k: int = 5) -> List[Dict]:
        """Get cross-references for a verse"""
        book, chapter, verse = self._parse_reference(ref)
        if book:
            try:
                result = self.app.discover_cross_references(book, chapter, verse, top_k=top_k)
                return result.get('cross_references', [])
            except:
                return []
        return []
    
    def _generate_chapter_content(self, chapter: Dict) -> str:
        """Generate content for a single chapter"""
        print(f"\nGenerating Chapter {chapter['number']}: {chapter['title']}...")
        
        # Collect Jesus' sayings
        sayings_text = []
        for ref, saying_text in chapter['key_sayings']:
            # Use provided text or try to get from Bible
            if saying_text:
                sayings_text.append(f"{ref}: {saying_text}")
            else:
                text = self._get_verse_text(ref)
                if text:
                    sayings_text.append(f"{ref}: {text}")
        
        # Collect cross-references
        all_cross_refs = []
        for ref, _ in chapter['key_sayings'][:3]:
            cross_refs = self._get_cross_references(ref, top_k=3)
            all_cross_refs.extend(cross_refs)
        
        # Build context
        context = "\n\n".join(sayings_text)
        
        # Generate chapter content
        prompt = f"""Write a comprehensive chapter for a book called "Red Letters" about Jesus' words from the Gospels.

Chapter Title: {chapter['title']}
Theme: {chapter['theme']}
Target Length: Approximately {chapter['pages']} pages (about {chapter['pages'] * 500} words)

Jesus' Key Sayings (Red Letters):
{context}

Cross-References Found Throughout Scripture:
{chr(10).join([f"- {cr['reference']}: {cr['summary']}" for cr in all_cross_refs[:5]])}

Instructions:
1. Begin with an engaging introduction that draws readers into Jesus' words
2. Explain what Jesus said and what it means
3. Show how this saying relates to the Old Testament (prophecies, themes, connections)
4. Show how it relates to the rest of the New Testament
5. Explore the relationship(s) revealed: with God, with others, with self, etc.
6. Explain how this saying shows "the way" to relationship with God
7. Include practical implications for living in relationship
8. Use the cross-references to show connections throughout Scripture
9. Write in an accessible but thoughtful style
10. Stay grounded in the actual words of Jesus provided

The chapter should be approximately {chapter['pages'] * 500} words, well-structured with clear sections.
Focus on how Jesus' words reveal relationships and the way to God."""
        
        try:
            result = self.llm.generate_grounded(
                prompt,
                max_length=chapter['pages'] * 600,
                require_validation=True
            )
            
            content = result.get('generated', '')
            if not content or len(content) < 500:
                content = self._generate_fallback_chapter(chapter, sayings_text)
            
            return content
        except Exception as e:
            print(f"Error generating chapter {chapter['number']}: {e}")
            return self._generate_fallback_chapter(chapter, sayings_text)
    
    def _generate_fallback_chapter(self, chapter: Dict, sayings: List[str]) -> str:
        """Generate a simpler chapter if AI generation fails"""
        content = f"# {chapter['title']}\n\n"
        content += f"## Introduction\n\n"
        content += f"Jesus' words in this chapter reveal {chapter['theme'].lower()}. "
        content += f"These 'red letters' - the recorded sayings of Jesus - show us the way to relationship with God "
        content += f"and with others. Let us explore what Jesus said and how it connects to the whole of Scripture.\n\n"
        
        content += f"## Jesus' Words (Red Letters)\n\n"
        for saying in sayings[:5]:
            content += f"{saying}\n\n"
        
        content += f"## The Relationship Revealed\n\n"
        content += f"Jesus' words here reveal {chapter['theme'].lower()}. "
        content += f"These sayings show us how to relate to God, to others, and to ourselves. "
        content += f"They are not isolated teachings but connect to the entire biblical narrative.\n\n"
        
        content += f"## Connections Throughout Scripture\n\n"
        content += f"These words of Jesus echo themes found throughout the Old Testament and are "
        content += f"expanded upon in the New Testament. They reveal God's heart and His plan for "
        content += f"relationship with humanity.\n\n"
        
        content += f"## The Way to Relationship\n\n"
        content += f"Through these words, Jesus shows us the way to relationship with God. "
        content += f"They are not just teachings but invitations into relationship - with the Father, "
        content += f"through the Son, by the Spirit, and with one another.\n\n"
        
        content += f"## Conclusion\n\n"
        content += f"Jesus' words in this chapter point us to the central truth: God desires relationship "
        content += f"with us, and Jesus is the way to that relationship. As we explore these red letters, "
        content += f"we discover not just information, but the path to life itself.\n\n"
        
        return content
    
    def generate_book(self):
        """Generate the complete book"""
        print("=" * 80)
        print("GENERATING 'RED LETTERS' BOOK")
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
        print(f"- Full book: red_letters_book.md")
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
        prompt = """Write an engaging introduction for a book titled "Red Letters: How Jesus' Words Reveal the Way to Relationship with God."

The introduction should:
1. Explain what "red letters" means (Jesus' words in the Gospels)
2. Explain why Jesus' words matter
3. Show how Jesus' words relate to the whole Bible
4. Explain the focus on relationships (with God, others, self)
5. Invite readers into discovery
6. Be approximately 4-5 pages (2000-2500 words)

Write in a style that is both scholarly and accessible, suitable for both new and experienced Bible readers."""
        
        try:
            result = self.llm.generate_grounded(prompt, max_length=2500, require_validation=True)
            return result.get('generated', self._default_introduction())
        except:
            return self._default_introduction()
    
    def _default_introduction(self) -> str:
        """Default introduction"""
        return """# Introduction: The Red Letters

In many Bibles, the words of Jesus are printed in red - the "red letters." These are the recorded sayings of Jesus Christ from the four Gospels: Matthew, Mark, Luke, and John. But these red letters are far more than historical records or moral teachings. They are the very words of life, revealing the way to relationship with God.

Jesus Himself said, "The words that I have spoken unto you are spirit, and are life" (John 6:63). His words are not mere information, but transformation. They reveal who God is, who we are, and how we can enter into relationship with the Creator of the universe.

This book explores Jesus' key sayings and shows how they:
- Connect to the entire Old Testament, fulfilling prophecies and revealing God's plan
- Relate to the rest of the New Testament, showing the foundation of Christian faith
- Reveal relationships: with God the Father, with Jesus the Son, with the Holy Spirit, and with others
- Show the way to relationship with God

As we journey through these red letters together, we will discover that Jesus' words are not isolated teachings but threads that weave together the entire biblical narrative, revealing God's heart and His desire for relationship with us."""
    
    def _generate_conclusion(self) -> str:
        """Generate book conclusion"""
        prompt = """Write a thoughtful conclusion for "Red Letters" that:
1. Summarizes how Jesus' words connect to the whole Bible
2. Shows how they reveal the way to relationship with God
3. Explores the relationships revealed (with God, others, self)
4. Invites readers into continued exploration
5. Is approximately 3-4 pages (1500-2000 words)

Write in a style that is inspiring and reflective."""
        
        try:
            result = self.llm.generate_grounded(prompt, max_length=2000, require_validation=True)
            return result.get('generated', self._default_conclusion())
        except:
            return self._default_conclusion()
    
    def _default_conclusion(self) -> str:
        """Default conclusion"""
        return """# Conclusion: The Red Letters and the Whole Story

As we have journeyed through the red letters - the recorded words of Jesus - we have discovered that these are not isolated teachings but threads that connect throughout all of Scripture. From Genesis to Revelation, Jesus' words echo, fulfill, and illuminate the entire biblical narrative.

We have seen how Jesus' words reveal:
- **Relationship with the Father**: How to know God as our loving Father
- **Relationship with the Son**: Who Jesus is and what it means to follow Him
- **Relationship with the Spirit**: How the Holy Spirit guides and empowers us
- **Relationship with Others**: How to love and serve one another
- **Relationship with Self**: Who we are in Christ

These relationships are not separate but interconnected, forming a beautiful tapestry of life in relationship with God. Jesus said, "I am the way, and the truth, and the life: no one cometh unto the Father, but by me" (John 14:6). The red letters show us this way.

As we continue to explore Jesus' words, may we discover not just information, but transformation. May we enter into the relationships He reveals - with the Father, through the Son, by the Spirit, and with one another. For in these relationships, we find life itself."""
    
    def _compile_book(self, toc: str, introduction: str, chapters: List[Dict], conclusion: str) -> str:
        """Compile the complete book"""
        book = f"""# Red Letters: How Jesus' Words Reveal the Way to Relationship with God

*Exploring the sayings of Jesus from the Gospels and their relationship to the whole Bible*

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
        book += "This book explores the 'red letters' - the recorded words of Jesus from the Gospels. "
        book += "All content is grounded in actual Scripture, showing how Jesus' words relate to the "
        book += "entire Bible and reveal the way to relationship with God.\n\n"
        
        return book
    
    def _save_book(self, full_book: str, chapters: List[Dict]):
        """Save the book to files"""
        # Save full book
        with open(os.path.join(self.output_dir, "red_letters_book.md"), 'w', encoding='utf-8') as f:
            f.write(full_book)
        
        # Save individual chapters
        for chapter in chapters:
            safe_title = chapter['title'].lower().replace(' ', '_').replace(':', '').replace("'", '').replace(',', '')[:50]
            filename = f"chapter_{chapter['number']:02d}_{safe_title}.md"
            with open(os.path.join(self.output_dir, filename), 'w', encoding='utf-8') as f:
                f.write(f"# {chapter['title']}\n\n{chapter['content']}")
        
        # Save metadata
        metadata = {
            "title": "Red Letters: How Jesus' Words Reveal the Way to Relationship with God",
            "generated_date": datetime.now().isoformat(),
            "total_chapters": len(self.chapters),
            "estimated_pages": sum(c['pages'] for c in self.chapters),
            "chapters": [
                {
                    "number": c['number'],
                    "title": c['title'],
                    "theme": c['theme'],
                    "pages": c['pages'],
                    "key_sayings": [ref for ref, _ in c['key_sayings']]
                }
                for c in self.chapters
            ]
        }
        
        with open(os.path.join(self.output_dir, "book_metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)


def main():
    """Main function"""
    print("=" * 80)
    print("RED LETTERS BOOK GENERATOR")
    print("=" * 80)
    print("\nThis will generate a book exploring Jesus' words from the Gospels")
    print("and how they relate to the whole Bible and reveal relationships.")
    print("\nStarting generation...\n")
    
    try:
        generator = RedLettersBookGenerator()
        generator.generate_book()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()