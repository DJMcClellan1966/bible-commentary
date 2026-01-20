"""
Load Bible Versions from HTML Files
Parses HTML files from asv, engDBY, and englyt folders
and loads them into the hyperlinked Bible app
"""
import os
import re
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict, Optional
from hyperlinked_bible_app import HyperlinkedBibleApp


# Book name mappings (HTML abbreviations to full names)
BOOK_MAPPINGS = {
    'GEN': 'Genesis', 'EXO': 'Exodus', 'LEV': 'Leviticus', 'NUM': 'Numbers', 'DEU': 'Deuteronomy',
    'JOS': 'Joshua', 'JDG': 'Judges', 'RUT': 'Ruth', '1SA': '1 Samuel', '2SA': '2 Samuel',
    '1KI': '1 Kings', '2KI': '2 Kings', '1CH': '1 Chronicles', '2CH': '2 Chronicles',
    'EZR': 'Ezra', 'NEH': 'Nehemiah', 'EST': 'Esther', 'JOB': 'Job', 'PSA': 'Psalms',
    'PRO': 'Proverbs', 'ECC': 'Ecclesiastes', 'SNG': 'Song of Songs', 'ISA': 'Isaiah',
    'JER': 'Jeremiah', 'LAM': 'Lamentations', 'EZK': 'Ezekiel', 'DAN': 'Daniel',
    'HOS': 'Hosea', 'JOL': 'Joel', 'AMO': 'Amos', 'OBA': 'Obadiah', 'JON': 'Jonah',
    'MIC': 'Micah', 'NAM': 'Nahum', 'HAB': 'Habakkuk', 'ZEP': 'Zephaniah', 'HAG': 'Haggai',
    'ZEC': 'Zechariah', 'MAL': 'Malachi',
    'MAT': 'Matthew', 'MRK': 'Mark', 'LUK': 'Luke', 'JOH': 'John', 'ACT': 'Acts',
    'ROM': 'Romans', '1CO': '1 Corinthians', '2CO': '2 Corinthians', 'GAL': 'Galatians',
    'EPH': 'Ephesians', 'PHP': 'Philippians', 'COL': 'Colossians', '1TH': '1 Thessalonians',
    '2TH': '2 Thessalonians', '1TI': '1 Timothy', '2TI': '2 Timothy', 'TIT': 'Titus',
    'PHM': 'Philemon', 'HEB': 'Hebrews', 'JAS': 'James', '1PE': '1 Peter', '2PE': '2 Peter',
    '1JN': '1 John', '2JN': '2 John', '3JN': '3 John', 'JUD': 'Jude', 'REV': 'Revelation',
}


class BibleVersionLoader:
    """Load Bible versions from HTML files"""
    
    def __init__(self, base_path: str):
        """
        Initialize loader
        
        Args:
            base_path: Path to bible-versions folder
                      e.g., r'C:\Users\...\bible-commentary\data\bible-versions'
        """
        self.base_path = base_path
        self.versions = {
            'asv': 'American Standard Version',
            'engDBY': 'Darby Bible',
            'englyt': "Young's Literal Translation"
        }
    
    def parse_html_file(self, file_path: str) -> List[Tuple[str, int, int, str]]:
        """
        Parse HTML file and extract verses
        
        Returns:
            List of (book, chapter, verse, text) tuples
        """
        verses = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Try BeautifulSoup first (more reliable)
            try:
                soup = BeautifulSoup(content, 'html.parser')
                # Find all verse elements (common patterns)
                verse_elements = soup.find_all(['p', 'div', 'span'], class_=re.compile(r'verse|v\d+', re.I))
                verse_elements = verse_elements or soup.find_all(id=re.compile(r'v\d+|verse', re.I))
                
                if verse_elements:
                    for elem in verse_elements:
                        verse_text = self._extract_verse_text(elem)
                        ref = self._extract_reference(elem, file_path)
                        if ref and verse_text:
                            book, chapter, verse = ref
                            verses.append((book, chapter, verse, verse_text))
            except Exception:
                pass
            
            # Fallback: Regex parsing
            if not verses:
                verses = self._regex_parse(content, file_path)
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return verses
    
    def _extract_verse_text(self, element) -> str:
        """Extract verse text from HTML element"""
        # Get text, removing verse numbers
        text = element.get_text()
        # Remove verse numbers like "16 " or "[16]"
        text = re.sub(r'^\[\d+\]\s*|\d+\s+', '', text.strip())
        return text.strip()
    
    def _extract_reference(self, element, file_path: str) -> Optional[Tuple[str, int, int]]:
        """Extract book, chapter, verse from element or filename"""
        # Try to get from element ID or class
        elem_id = element.get('id', '')
        elem_class = ' '.join(element.get('class', []))
        
        # Pattern: v16, verse16, etc.
        verse_match = re.search(r'v(\d+)', elem_id + elem_class, re.I)
        verse = int(verse_match.group(1)) if verse_match else None
        
        # Get book and chapter from filename
        filename = os.path.basename(file_path)
        # Pattern: JOH03.htm or JOH3.htm
        book_match = re.match(r'([A-Z1-3]+)(\d+)\.htm', filename, re.I)
        if book_match:
            book_abbr = book_match.group(1).upper()
            chapter = int(book_match.group(2))
            book = BOOK_MAPPINGS.get(book_abbr, book_abbr)
            if verse:
                return (book, chapter, verse)
        
        return None
    
    def _regex_parse(self, content: str, file_path: str) -> List[Tuple[str, int, int, str]]:
        """Fallback regex parsing"""
        verses = []
        
        # Get book and chapter from filename
        filename = os.path.basename(file_path)
        book_match = re.match(r'([A-Z1-3]+)(\d+)\.htm', filename, re.I)
        if not book_match:
            return verses
        
        book_abbr = book_match.group(1).upper()
        chapter = int(book_match.group(2))
        book = BOOK_MAPPINGS.get(book_abbr, book_abbr)
        
        # Common patterns for verses in HTML
        patterns = [
            r'<p[^>]*>.*?(\d+)\s+([^<]+)</p>',  # <p>16 verse text</p>
            r'\[(\d+)\]\s*([^<\n]+)',  # [16] verse text
            r'<span[^>]*>(\d+)\s+([^<]+)</span>',  # <span>16 verse text</span>
            r'(\d+)\s+([A-Z][^<\n]{10,})',  # 16 Verse text (standalone)
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                verse_num = int(match.group(1))
                verse_text = match.group(2).strip()
                # Clean HTML tags
                verse_text = re.sub(r'<[^>]+>', '', verse_text)
                verse_text = verse_text.strip()
                
                if verse_text and len(verse_text) > 5:  # Minimum length
                    verses.append((book, chapter, verse_num, verse_text))
        
        return verses
    
    def load_version(self, version_folder: str) -> List[Tuple[str, int, int, str]]:
        """
        Load all verses from a version folder
        
        Args:
            version_folder: Folder name (e.g., 'asv', 'engDBY', 'englyt')
        
        Returns:
            List of (book, chapter, verse, text) tuples
        """
        version_path = os.path.join(self.base_path, version_folder)
        
        if not os.path.exists(version_path):
            print(f"Version folder not found: {version_path}")
            return []
        
        all_verses = []
        html_files = [f for f in os.listdir(version_path) 
                     if f.endswith('.htm') and re.match(r'[A-Z1-3]+\d+\.htm', f, re.I)]
        
        print(f"Loading {version_folder}...")
        print(f"Found {len(html_files)} HTML files")
        
        for i, html_file in enumerate(html_files):
            if i % 100 == 0:
                print(f"  Processing {i}/{len(html_files)}...")
            
            file_path = os.path.join(version_path, html_file)
            verses = self.parse_html_file(file_path)
            all_verses.extend(verses)
        
        print(f"Loaded {len(all_verses)} verses from {version_folder}")
        return all_verses
    
    def load_all_versions(self) -> Dict[str, List[Tuple[str, int, int, str]]]:
        """Load all three Bible versions"""
        all_data = {}
        
        for version_folder, version_name in self.versions.items():
            print(f"\n{'='*60}")
            print(f"Loading {version_name} ({version_folder})")
            print(f"{'='*60}")
            verses = self.load_version(version_folder)
            all_data[version_folder] = verses
        
        return all_data


def load_into_app(app: HyperlinkedBibleApp, verses: List[Tuple[str, int, int, str]], 
                  version_name: str = ""):
    """
    Load verses into hyperlinked Bible app
    
    Args:
        app: HyperlinkedBibleApp instance
        verses: List of (book, chapter, verse, text) tuples
        version_name: Optional version identifier
    """
    print(f"\nLoading {len(verses)} verses into app...")
    
    for i, (book, chapter, verse, text) in enumerate(verses):
        if i % 1000 == 0:
            print(f"  Loaded {i}/{len(verses)} verses...")
        
        # Store with version identifier if provided
        if version_name:
            reference = f"{book} {chapter}:{verse} ({version_name})"
        else:
            reference = f"{book} {chapter}:{verse}"
        
        app.add_verse(book, chapter, verse, text)
    
    print(f"✓ Loaded {len(verses)} verses")


def main():
    """Main loading function"""
    # Path to bible-versions folder
    base_path = r'C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions'
    
    print("=" * 80)
    print("BIBLE VERSION LOADER")
    print("=" * 80)
    print(f"\nBase path: {base_path}")
    
    # Check if path exists
    if not os.path.exists(base_path):
        print(f"\n❌ Path not found: {base_path}")
        print("\nPlease update the base_path in the script to match your folder location.")
        return
    
    # Create loader
    loader = BibleVersionLoader(base_path)
    
    # Load all versions
    all_versions = loader.load_all_versions()
    
    # Create app and load verses
    print("\n" + "=" * 80)
    print("LOADING INTO HYPERLINKED BIBLE APP")
    print("=" * 80)
    
    app = HyperlinkedBibleApp()
    
    # Load each version
    for version_folder, verses in all_versions.items():
        version_name = loader.versions.get(version_folder, version_folder)
        print(f"\nLoading {version_name}...")
        load_into_app(app, verses, version_name)
    
    # Statistics
    print("\n" + "=" * 80)
    print("LOADING COMPLETE")
    print("=" * 80)
    
    stats = app.get_stats()
    print(f"\nTotal verses loaded: {stats['total_verses']}")
    print(f"Kernel cache size: {stats['kernel_stats']['cache_size']}")
    print(f"Embeddings computed: {stats['kernel_stats']['embeddings_computed']}")
    
    # Test with a verse
    print("\n" + "=" * 80)
    print("TESTING")
    print("=" * 80)
    
    test_result = app.get_verse_with_hyperlinks("John", 3, 16, top_k=5)
    print(f"\nVerse: {test_result['verse']}")
    print(f"Text: {test_result['verse_text'][:100]}...")
    print(f"\nFound {len(test_result['hyperlinks'])} cross-references:")
    for link in test_result['hyperlinks'][:3]:
        print(f"  - {link['reference']}: {link['summary']} (similarity: {link['similarity']:.3f})")
    
    print("\n" + "=" * 80)
    print("✓ ALL VERSIONS LOADED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()
