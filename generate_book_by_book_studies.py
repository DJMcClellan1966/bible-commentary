"""
Generate Book-by-Book Bible Studies
Creates comprehensive studies for all 66 books of the Bible
"""
import os
import json
import re
from typing import List, Dict, Tuple
from datetime import datetime
from hyperlinked_bible_app import HyperlinkedBibleApp
from quantum_llm_standalone import StandaloneQuantumLLM


# All 66 books of the Bible with themes and key verses
BIBLE_BOOKS = [
    # Old Testament (39 books)
    {"name": "Genesis", "testament": "Old", "theme": "The Beginning - Creation, Fall, and God's Covenant", "key_verses": ["Genesis 1:1", "Genesis 3:15", "Genesis 12:1-3", "Genesis 50:20"]},
    {"name": "Exodus", "testament": "Old", "theme": "Deliverance from Egypt and the Law", "key_verses": ["Exodus 3:14", "Exodus 12:13", "Exodus 20:1-17", "Exodus 34:6-7"]},
    {"name": "Leviticus", "testament": "Old", "theme": "Holiness and Worship", "key_verses": ["Leviticus 11:45", "Leviticus 19:2", "Leviticus 17:11"]},
    {"name": "Numbers", "testament": "Old", "theme": "Journey and Testing in the Wilderness", "key_verses": ["Numbers 6:24-26", "Numbers 14:18", "Numbers 23:19"]},
    {"name": "Deuteronomy", "testament": "Old", "theme": "The Second Law - Reminder and Renewal", "key_verses": ["Deuteronomy 6:4-5", "Deuteronomy 30:19-20", "Deuteronomy 31:6"]},
    {"name": "Joshua", "testament": "Old", "theme": "Conquest and Inheritance of the Promised Land", "key_verses": ["Joshua 1:8-9", "Joshua 24:15"]},
    {"name": "Judges", "testament": "Old", "theme": "Cycles of Sin, Oppression, and Deliverance", "key_verses": ["Judges 2:16", "Judges 21:25"]},
    {"name": "Ruth", "testament": "Old", "theme": "Redemption and Loyalty", "key_verses": ["Ruth 1:16", "Ruth 4:14"]},
    {"name": "1 Samuel", "testament": "Old", "theme": "The Kingdom Established - Saul and David", "key_verses": ["1 Samuel 13:14", "1 Samuel 16:7"]},
    {"name": "2 Samuel", "testament": "Old", "theme": "David's Reign and God's Covenant", "key_verses": ["2 Samuel 7:12-16", "2 Samuel 22:2"]},
    {"name": "1 Kings", "testament": "Old", "theme": "The Divided Kingdom", "key_verses": ["1 Kings 3:9", "1 Kings 8:27"]},
    {"name": "2 Kings", "testament": "Old", "theme": "The Fall of Israel and Judah", "key_verses": ["2 Kings 17:13", "2 Kings 23:25"]},
    {"name": "1 Chronicles", "testament": "Old", "theme": "The History Retold - Genealogy and David", "key_verses": ["1 Chronicles 16:8-36", "1 Chronicles 29:11"]},
    {"name": "2 Chronicles", "testament": "Old", "theme": "The History Retold - The Kingdom", "key_verses": ["2 Chronicles 7:14", "2 Chronicles 16:9"]},
    {"name": "Ezra", "testament": "Old", "theme": "The Return from Exile and Rebuilding", "key_verses": ["Ezra 1:1", "Ezra 7:10"]},
    {"name": "Nehemiah", "testament": "Old", "theme": "Rebuilding the Walls of Jerusalem", "key_verses": ["Nehemiah 2:20", "Nehemiah 8:10"]},
    {"name": "Esther", "testament": "Old", "theme": "God's Hidden Hand in Deliverance", "key_verses": ["Esther 4:14", "Esther 8:16"]},
    {"name": "Job", "testament": "Old", "theme": "Suffering, Faith, and God's Sovereignty", "key_verses": ["Job 1:21", "Job 42:2", "Job 19:25"]},
    {"name": "Psalms", "testament": "Old", "theme": "Songs of the Heart - Worship, Prayer, and Praise", "key_verses": ["Psalm 1:1-2", "Psalm 23:1", "Psalm 46:1", "Psalm 119:105"]},
    {"name": "Proverbs", "testament": "Old", "theme": "Wisdom for Daily Living", "key_verses": ["Proverbs 1:7", "Proverbs 3:5-6", "Proverbs 9:10"]},
    {"name": "Ecclesiastes", "testament": "Old", "theme": "The Meaning of Life Under the Sun", "key_verses": ["Ecclesiastes 1:2", "Ecclesiastes 12:13"]},
    {"name": "Song of Songs", "testament": "Old", "theme": "Love and Intimacy", "key_verses": ["Song of Songs 2:16", "Song of Songs 8:6-7"]},
    {"name": "Isaiah", "testament": "Old", "theme": "The Prophet of Hope and the Messiah", "key_verses": ["Isaiah 6:8", "Isaiah 9:6", "Isaiah 53:5", "Isaiah 55:8-9"]},
    {"name": "Jeremiah", "testament": "Old", "theme": "Judgment and Restoration", "key_verses": ["Jeremiah 1:5", "Jeremiah 29:11", "Jeremiah 31:33"]},
    {"name": "Lamentations", "testament": "Old", "theme": "Grief and Hope in Destruction", "key_verses": ["Lamentations 3:22-23", "Lamentations 5:21"]},
    {"name": "Ezekiel", "testament": "Old", "theme": "Visions of Judgment and Restoration", "key_verses": ["Ezekiel 36:26", "Ezekiel 37:1-14"]},
    {"name": "Daniel", "testament": "Old", "theme": "Faith in Exile and Prophecy", "key_verses": ["Daniel 2:20-21", "Daniel 3:17-18", "Daniel 6:23"]},
    {"name": "Hosea", "testament": "Old", "theme": "God's Unfaithful People and Unfailing Love", "key_verses": ["Hosea 6:6", "Hosea 11:1"]},
    {"name": "Joel", "testament": "Old", "theme": "The Day of the Lord", "key_verses": ["Joel 2:12-13", "Joel 2:28"]},
    {"name": "Amos", "testament": "Old", "theme": "Justice and Righteousness", "key_verses": ["Amos 5:24", "Amos 9:11"]},
    {"name": "Obadiah", "testament": "Old", "theme": "Judgment on Edom", "key_verses": ["Obadiah 1:15", "Obadiah 1:21"]},
    {"name": "Jonah", "testament": "Old", "theme": "God's Mercy to All Nations", "key_verses": ["Jonah 2:9", "Jonah 4:2"]},
    {"name": "Micah", "testament": "Old", "theme": "Justice, Mercy, and the Coming Messiah", "key_verses": ["Micah 5:2", "Micah 6:8"]},
    {"name": "Nahum", "testament": "Old", "theme": "Judgment on Nineveh", "key_verses": ["Nahum 1:7", "Nahum 1:15"]},
    {"name": "Habakkuk", "testament": "Old", "theme": "Faith in Times of Trouble", "key_verses": ["Habakkuk 2:4", "Habakkuk 3:17-19"]},
    {"name": "Zephaniah", "testament": "Old", "theme": "The Day of the Lord's Wrath", "key_verses": ["Zephaniah 3:17", "Zephaniah 3:20"]},
    {"name": "Haggai", "testament": "Old", "theme": "Rebuilding the Temple", "key_verses": ["Haggai 1:8", "Haggai 2:9"]},
    {"name": "Zechariah", "testament": "Old", "theme": "Visions of Restoration and the Coming King", "key_verses": ["Zechariah 9:9", "Zechariah 14:9"]},
    {"name": "Malachi", "testament": "Old", "theme": "The Last Prophet - Preparing for the Messiah", "key_verses": ["Malachi 3:1", "Malachi 4:2"]},
    
    # New Testament (27 books)
    {"name": "Matthew", "testament": "New", "theme": "The Kingdom Gospel - Jesus as King", "key_verses": ["Matthew 1:23", "Matthew 5:17", "Matthew 16:16", "Matthew 28:19-20"]},
    {"name": "Mark", "testament": "New", "theme": "The Action Gospel - Jesus as Servant", "key_verses": ["Mark 1:1", "Mark 10:45", "Mark 16:15"]},
    {"name": "Luke", "testament": "New", "theme": "The Universal Gospel - Jesus as Savior of All", "key_verses": ["Luke 2:10-11", "Luke 19:10", "Luke 24:46-47"]},
    {"name": "John", "testament": "New", "theme": "The Gospel of Life - Jesus as God", "key_verses": ["John 1:1", "John 3:16", "John 14:6", "John 20:31"]},
    {"name": "Acts", "testament": "New", "theme": "The Early Church and the Spread of the Gospel", "key_verses": ["Acts 1:8", "Acts 2:42", "Acts 4:12"]},
    {"name": "Romans", "testament": "New", "theme": "The Gospel Explained - Righteousness by Faith", "key_verses": ["Romans 1:16", "Romans 3:23", "Romans 5:8", "Romans 8:28"]},
    {"name": "1 Corinthians", "testament": "New", "theme": "Church Life and Unity", "key_verses": ["1 Corinthians 1:18", "1 Corinthians 13:4-7", "1 Corinthians 15:3-4"]},
    {"name": "2 Corinthians", "testament": "New", "theme": "Ministry, Suffering, and Grace", "key_verses": ["2 Corinthians 3:18", "2 Corinthians 5:17", "2 Corinthians 12:9"]},
    {"name": "Galatians", "testament": "New", "theme": "Freedom in Christ - Justification by Faith", "key_verses": ["Galatians 2:20", "Galatians 3:28", "Galatians 5:1"]},
    {"name": "Ephesians", "testament": "New", "theme": "The Church's Identity and Unity in Christ", "key_verses": ["Ephesians 1:3", "Ephesians 2:8-9", "Ephesians 4:1"]},
    {"name": "Philippians", "testament": "New", "theme": "Joy in Christ Despite Circumstances", "key_verses": ["Philippians 1:21", "Philippians 2:5-11", "Philippians 4:13"]},
    {"name": "Colossians", "testament": "New", "theme": "The Supremacy of Christ", "key_verses": ["Colossians 1:15-20", "Colossians 2:9-10", "Colossians 3:2"]},
    {"name": "1 Thessalonians", "testament": "New", "theme": "The Second Coming and Holy Living", "key_verses": ["1 Thessalonians 4:16-17", "1 Thessalonians 5:16-18"]},
    {"name": "2 Thessalonians", "testament": "New", "theme": "The Day of the Lord and Perseverance", "key_verses": ["2 Thessalonians 2:1-2", "2 Thessalonians 3:10"]},
    {"name": "1 Timothy", "testament": "New", "theme": "Pastoral Leadership and Sound Doctrine", "key_verses": ["1 Timothy 3:16", "1 Timothy 4:12", "1 Timothy 6:12"]},
    {"name": "2 Timothy", "testament": "New", "theme": "Endurance and Faithfulness in Ministry", "key_verses": ["2 Timothy 1:7", "2 Timothy 3:16-17", "2 Timothy 4:7"]},
    {"name": "Titus", "testament": "New", "theme": "Sound Doctrine and Good Works", "key_verses": ["Titus 2:11-14", "Titus 3:5"]},
    {"name": "Philemon", "testament": "New", "theme": "Forgiveness and Reconciliation", "key_verses": ["Philemon 1:15-16", "Philemon 1:17"]},
    {"name": "Hebrews", "testament": "New", "theme": "The Superiority of Christ and the New Covenant", "key_verses": ["Hebrews 1:3", "Hebrews 4:12", "Hebrews 11:1", "Hebrews 12:2"]},
    {"name": "James", "testament": "New", "theme": "Faith in Action - Practical Christianity", "key_verses": ["James 1:2-3", "James 2:17", "James 4:7"]},
    {"name": "1 Peter", "testament": "New", "theme": "Living as Exiles - Hope in Suffering", "key_verses": ["1 Peter 1:3", "1 Peter 2:9", "1 Peter 5:7"]},
    {"name": "2 Peter", "testament": "New", "theme": "False Teachers and the Day of the Lord", "key_verses": ["2 Peter 1:20-21", "2 Peter 3:9"]},
    {"name": "1 John", "testament": "New", "theme": "Love, Truth, and Assurance", "key_verses": ["1 John 1:9", "1 John 4:8", "1 John 5:13"]},
    {"name": "2 John", "testament": "New", "theme": "Walking in Truth and Love", "key_verses": ["2 John 1:6", "2 John 1:9"]},
    {"name": "3 John", "testament": "New", "theme": "Hospitality and Support for Ministry", "key_verses": ["3 John 1:2", "3 John 1:11"]},
    {"name": "Jude", "testament": "New", "theme": "Contending for the Faith", "key_verses": ["Jude 1:3", "Jude 1:24-25"]},
    {"name": "Revelation", "testament": "New", "theme": "The End and the Beginning - Victory in Christ", "key_verses": ["Revelation 1:8", "Revelation 21:1-4", "Revelation 22:20"]},
]


class BookByBookStudyGenerator:
    """Generate comprehensive studies for each book of the Bible"""
    
    def __init__(self):
        """Initialize the generator"""
        print("Initializing Book-by-Book Study Generator...")
        
        self.app = HyperlinkedBibleApp()
        self.llm = StandaloneQuantumLLM(
            kernel=self.app.kernel,
            source_texts=list(self.app.versions.get('asv', {}).values())[:100] if self.app.versions else ["God is love"]
        )
        
        self.output_dir = "book_by_book_studies"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.library = None
        try:
            from book_library import BookLibrary, initialize_library_with_existing_books
            self.library = initialize_library_with_existing_books()
        except ImportError:
            print("Warning: Book library not available")
    
    def _parse_reference(self, ref: str) -> Tuple[str, int, int]:
        """Parse a verse reference"""
        match = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
        if match:
            book = match.group(1).strip()
            chapter = int(match.group(2))
            verse = int(match.group(3))
            return book, chapter, verse
        return None, 0, 0
    
    def _get_verse_text(self, ref: str, version: str = "asv") -> str:
        """Get verse text"""
        book, chapter, verse = self._parse_reference(ref)
        if book:
            return self.app.get_verse_text(book, chapter, verse, version)
        return ""
    
    def _generate_book_study(self, book_info: Dict) -> str:
        """Generate a study for a single book"""
        book_name = book_info["name"]
        theme = book_info["theme"]
        key_verses = book_info["key_verses"]
        testament = book_info["testament"]
        
        print(f"\nGenerating study for {book_name}...")
        
        # Collect verse texts
        verses_text = []
        for ref in key_verses:
            text = self._get_verse_text(ref)
            if text:
                verses_text.append(f"{ref}: {text}")
        
        # Build context
        context = "\n\n".join(verses_text) if verses_text else ""
        
        # Determine pages based on book length (shorter books get fewer pages)
        if book_name in ["Obadiah", "Philemon", "2 John", "3 John", "Jude"]:
            pages = 4
        elif book_name in ["Ruth", "Joel", "Nahum", "Haggai", "Malachi"]:
            pages = 6
        elif book_name in ["Esther", "Ecclesiastes", "Song of Songs", "Lamentations"]:
            pages = 8
        else:
            pages = 10
        
        # Generate study
        prompt = f"""Write a comprehensive Bible study for the book of {book_name}.

Book: {book_name}
Testament: {testament}
Theme: {theme}
Target Length: Approximately {pages} pages (about {pages * 500} words)

Key Verses:
{context}

Instructions:
1. Provide an overview of the book (author, date, historical context)
2. Explain the main theme and purpose
3. Outline the book's structure and key sections
4. Explore the key verses and their significance
5. Show how this book relates to the rest of the Bible
6. Highlight key theological concepts
7. Provide practical applications for today
8. Include study questions for reflection
9. Write in an accessible but thoughtful style
10. Stay grounded in the actual Bible text

The study should be approximately {pages * 500} words, well-structured with clear sections."""
        
        try:
            result = self.llm.generate_grounded(
                prompt,
                max_length=pages * 600,
                require_validation=True
            )
            
            content = result.get('generated', '')
            if not content or len(content) < 300:
                content = self._generate_fallback_study(book_info, verses_text, pages)
            
            return content
        except Exception as e:
            print(f"Error generating {book_name}: {e}")
            return self._generate_fallback_study(book_info, verses_text, pages)
    
    def _generate_fallback_study(self, book_info: Dict, verses: List[str], pages: int) -> str:
        """Generate a simpler study if AI generation fails"""
        book_name = book_info["name"]
        theme = book_info["theme"]
        testament = book_info["testament"]
        
        content = f"# {book_name}: A Bible Study\n\n"
        content += f"## Overview\n\n"
        content += f"The book of {book_name} is part of the {testament} Testament. "
        content += f"Its main theme is: {theme.lower()}.\n\n"
        
        content += f"## Key Verses\n\n"
        for verse in verses[:5]:
            content += f"{verse}\n\n"
        
        content += f"## Main Theme\n\n"
        content += f"{theme}. This book reveals important truths about God, "
        content += f"humanity, and the relationship between them.\n\n"
        
        content += f"## Structure\n\n"
        content += f"The book of {book_name} can be divided into key sections "
        content += f"that develop the main theme. Each section contributes to "
        content += f"the overall message of the book.\n\n"
        
        content += f"## Key Concepts\n\n"
        content += f"This book explores important biblical concepts that relate "
        content += f"to the whole of Scripture. Understanding {book_name} helps "
        content += f"us understand God's plan and purposes.\n\n"
        
        content += f"## Practical Application\n\n"
        content += f"The teachings and principles in {book_name} have practical "
        content += f"implications for our lives today. We can apply these truths "
        content += f"to our relationship with God and with others.\n\n"
        
        content += f"## Study Questions\n\n"
        content += f"1. What is the main theme of {book_name}?\n"
        content += f"2. How does this book relate to the rest of the Bible?\n"
        content += f"3. What are the key verses and why are they important?\n"
        content += f"4. How can we apply the teachings of {book_name} today?\n\n"
        
        return content
    
    def generate_all_studies(self, add_to_library: bool = True):
        """Generate studies for all 66 books"""
        print("=" * 80)
        print("GENERATING BOOK-BY-BOOK BIBLE STUDIES")
        print("=" * 80)
        print(f"\nTotal Books: {len(BIBLE_BOOKS)}")
        print(f"Old Testament: {sum(1 for b in BIBLE_BOOKS if b['testament'] == 'Old')}")
        print(f"New Testament: {sum(1 for b in BIBLE_BOOKS if b['testament'] == 'New')}")
        print(f"Output Directory: {self.output_dir}\n")
        
        generated_studies = []
        
        for i, book_info in enumerate(BIBLE_BOOKS, 1):
            book_name = book_info["name"]
            print(f"[{i}/{len(BIBLE_BOOKS)}] {book_name}...")
            
            # Generate study
            study_content = self._generate_book_study(book_info)
            
            # Save study
            safe_name = book_name.replace(" ", "_").replace("'", "")
            filename = f"{safe_name}_study.md"
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(study_content)
            
            # Add to library if available
            if add_to_library and self.library:
                try:
                    self.library.add_book(
                        filepath,
                        f"{book_name}: A Bible Study",
                        f"Comprehensive study of the book of {book_name}. {book_info['theme']}",
                        category=f"{book_info['testament']} Testament Studies",
                        tags=[book_name.lower(), book_info['testament'].lower(), "book study", "bible study"]
                    )
                    print(f"  Added to library")
                except Exception as e:
                    print(f"  Warning: Could not add to library: {e}")
            
            generated_studies.append({
                "book": book_name,
                "file": filename,
                "path": filepath
            })
        
        # Save metadata
        metadata = {
            "generated_date": datetime.now().isoformat(),
            "total_books": len(BIBLE_BOOKS),
            "studies": [
                {
                    "book": s["book"],
                    "file": s["file"]
                }
                for s in generated_studies
            ]
        }
        
        with open(os.path.join(self.output_dir, "studies_metadata.json"), 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print("\n" + "=" * 80)
        print("GENERATION COMPLETE!")
        print("=" * 80)
        print(f"\nGenerated {len(generated_studies)} book studies")
        print(f"Saved to: {self.output_dir}/")
        if add_to_library and self.library:
            print(f"Added to library: {len(generated_studies)} books")
            stats = self.library.get_statistics()
            print(f"Total books in library: {stats['total_books']}")
        
        return generated_studies


def main():
    """Main function"""
    print("=" * 80)
    print("BOOK-BY-BOOK BIBLE STUDY GENERATOR")
    print("=" * 80)
    print("\nThis will generate comprehensive studies for all 66 books of the Bible.")
    print("This may take some time. Each study will be added to the library.")
    print("\nStarting generation...\n")
    
    try:
        generator = BookByBookStudyGenerator()
        generator.generate_all_studies(add_to_library=True)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()