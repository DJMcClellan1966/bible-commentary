"""
Load Bible Versions from HTML Files
Simple, robust parser for HTML Bible files
Supports: ASV, Darby (engDBY), Young's Literal (englyt)
"""
import os
import re
from typing import List, Tuple, Dict, Optional
from hyperlinked_bible_app import HyperlinkedBibleApp


# Book name mappings
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


class BibleHTMLParser:
    """Parse Bible verses from HTML files"""
    
    @staticmethod
    def parse_file(file_path: str) -> List[Tuple[str, int, int, str]]:
        """
        Parse HTML file and extract verses
        
        Returns:
            List of (book, chapter, verse, text) tuples
        """
        verses = []
        
        try:
            # Read file with multiple encoding attempts
            content = None
            for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']:
                try:
                    with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                        content = f.read()
                    break
                except Exception:
                    continue
            
            if not content:
                return verses
            
            # Get book and chapter from filename
            filename = os.path.basename(file_path)
            book_match = re.match(r'([A-Z1-3]+)(\d+)\.htm', filename, re.I)
            if not book_match:
                return verses
            
            book_abbr = book_match.group(1).upper()
            chapter = int(book_match.group(2))
            book = BOOK_MAPPINGS.get(book_abbr, book_abbr)
            
            # Extract verses - this format uses <span class="verse" id="V1">1 </span>text
            # Pattern: <span class="verse" id="V{number}">{number}&#160;</span>text until next span or </div>
            
            # Pattern 1: <span class="verse" id="V1">1&#160;</span>verse text
            verse_pattern = r'<span\s+class=["\']verse["\']\s+id=["\']V(\d+)["\'][^>]*>[\d&#160;]+\s*</span>\s*([^<]+?)(?=<span\s+class=["\']verse|<div|</div>|$)'
            matches = re.finditer(verse_pattern, content, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                verse_num = int(match.group(1))
                verse_text = match.group(2).strip()
                
                # Clean HTML entities and tags
                verse_text = verse_text.replace('&#160;', ' ').replace('&nbsp;', ' ')
                verse_text = re.sub(r'<[^>]+>', '', verse_text)  # Remove HTML tags
                verse_text = re.sub(r'&[a-z]+;', '', verse_text)  # Remove HTML entities
                verse_text = re.sub(r'\s+', ' ', verse_text).strip()
                
                if verse_text and len(verse_text) > 3 and verse_num <= 200:
                    verses.append((book, chapter, verse_num, verse_text))
            
            # Pattern 2: Alternative format - verse numbers in spans followed by text
            if not verses:
                alt_pattern = r'<span[^>]*class=["\']verse["\'][^>]*id=["\']V(\d+)["\'][^>]*>[\d\s&#160;]*</span>\s*([^<]+)'
                matches = re.finditer(alt_pattern, content, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    verse_num = int(match.group(1))
                    verse_text = match.group(2).strip()
                    
                    # Clean
                    verse_text = verse_text.replace('&#160;', ' ').replace('&nbsp;', ' ')
                    verse_text = re.sub(r'<[^>]+>', '', verse_text)
                    verse_text = re.sub(r'&[a-z]+;', '', verse_text)
                    verse_text = re.sub(r'\s+', ' ', verse_text).strip()
                    
                    if verse_text and len(verse_text) > 3 and verse_num <= 200:
                        verses.append((book, chapter, verse_num, verse_text))
            
            # Pattern 3: Fallback - numbers followed by capitalized text
            if not verses:
                fallback_pattern = r'(?:<[^>]*>|^|\s)(\d+)\s+([A-Z][^<\n]{10,})'
                matches = re.finditer(fallback_pattern, content, re.IGNORECASE | re.MULTILINE)
                
                for match in matches:
                    verse_num = int(match.group(1))
                    verse_text = match.group(2).strip()
                    verse_text = re.sub(r'<[^>]+>', '', verse_text)
                    verse_text = re.sub(r'\s+', ' ', verse_text).strip()
                    
                    if verse_text and len(verse_text) > 5 and verse_num <= 200:
                        verses.append((book, chapter, verse_num, verse_text))
            
            # Remove duplicates (keep first occurrence)
            seen = set()
            unique_verses = []
            for verse in verses:
                key = (verse[0], verse[1], verse[2])
                if key not in seen:
                    seen.add(key)
                    unique_verses.append(verse)
            
            return unique_verses
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return []


def load_bible_version(base_path: str, version_folder: str, version_name: str = "") -> List[Tuple[str, int, int, str]]:
    """
    Load all verses from a version folder
    
    Args:
        base_path: Path to bible-versions folder
        version_folder: Folder name ('asv', 'engDBY', 'englyt')
        version_name: Display name for version
    
    Returns:
        List of (book, chapter, verse, text) tuples
    """
    version_path = os.path.join(base_path, version_folder)
    
    if not os.path.exists(version_path):
        print(f"❌ Version folder not found: {version_path}")
        return []
    
    parser = BibleHTMLParser()
    all_verses = []
    
    # Get all chapter HTML files (pattern: BOOK##.htm)
    html_files = [f for f in os.listdir(version_path) 
                 if f.endswith('.htm') and re.match(r'[A-Z1-3]+\d+\.htm$', f, re.I)]
    
    html_files.sort()  # Process in order
    
    print(f"\n{'='*60}")
    print(f"Loading {version_name or version_folder}")
    print(f"{'='*60}")
    print(f"Found {len(html_files)} HTML files")
    
    for i, html_file in enumerate(html_files):
        if (i + 1) % 50 == 0:
            print(f"  Processing {i + 1}/{len(html_files)} files... (loaded {len(all_verses)} verses)")
        
        file_path = os.path.join(version_path, html_file)
        verses = parser.parse_file(file_path)
        all_verses.extend(verses)
    
    print(f"[OK] Loaded {len(all_verses)} verses from {version_name or version_folder}")
    return all_verses


def load_all_versions_into_app(app: HyperlinkedBibleApp, base_path: str):
    """
    Load all three Bible versions into the app
    
    Args:
        app: HyperlinkedBibleApp instance
        base_path: Path to bible-versions folder
    """
    versions = {
        'asv': 'American Standard Version',
        'engDBY': 'Darby Bible',
        'englyt': "Young's Literal Translation"
    }
    
    total_verses = 0
    
    for version_folder, version_name in versions.items():
        print(f"\n{'='*80}")
        print(f"LOADING {version_name.upper()}")
        print(f"{'='*80}")
        
        verses = load_bible_version(base_path, version_folder, version_name)
        
        if verses:
            print(f"\nAdding {len(verses)} verses to app...")
            
            # Add to app with version identifier
            for book, chapter, verse, text in verses:
                app.add_verse(book, chapter, verse, text, version=version_folder)
            
            total_verses += len(verses)
            print(f"[OK] Added {len(verses)} verses")
        else:
            print(f"⚠ No verses found for {version_name}")
    
    return total_verses


def main():
    """Main loading function"""
    # Update this path to match your folder location
    base_path = r'C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions'
    
    print("=" * 80)
    print("BIBLE VERSION LOADER")
    print("=" * 80)
    print(f"\nLoading from: {base_path}")
    
    # Check if path exists
    if not os.path.exists(base_path):
        print(f"\n❌ Path not found: {base_path}")
        print("\nPlease update the base_path in the script.")
        return
    
    # Create app
    print("\nInitializing Hyperlinked Bible App...")
    app = HyperlinkedBibleApp()
    
    # Load all versions
    total = load_all_versions_into_app(app, base_path)
    
    # Statistics
    print("\n" + "=" * 80)
    print("LOADING COMPLETE")
    print("=" * 80)
    
    stats = app.get_stats()
    print(f"\n[OK] Total verses loaded: {total}")
    print(f"[OK] Verses in app: {stats['total_verses']}")
    print(f"[OK] Kernel cache: {stats['kernel_stats']['cache_size']} items")
    print(f"[OK] Embeddings computed: {stats['kernel_stats']['embeddings_computed']}")
    
    # Test
    print("\n" + "=" * 80)
    print("TESTING HYPERLINKS")
    print("=" * 80)
    
    try:
        test_result = app.get_verse_with_hyperlinks("John", 3, 16, top_k=5)
        print(f"\nVerse: {test_result['verse']}")
        print(f"Text: {test_result['verse_text'][:100]}...")
        print(f"\nFound {len(test_result['hyperlinks'])} cross-references:")
        for i, link in enumerate(test_result['hyperlinks'][:5], 1):
            print(f"{i}. {link['reference']}: {link['summary']} (similarity: {link['similarity']:.3f})")
    except Exception as e:
        print(f"Test error: {e}")
    
    print("\n" + "=" * 80)
    print("[OK] ALL DONE! Your Bible app is ready with all 3 versions!")
    print("=" * 80)
    
    return app


if __name__ == "__main__":
    main()
