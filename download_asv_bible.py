"""
Download American Standard Bible (ASV) - Public Domain
Helps download and parse ASV Bible text for the hyperlinked Bible app
"""
import urllib.request
import json
import re
from typing import List, Tuple


def download_asv_from_github():
    """
    Download ASV Bible from open-bibles repository
    Returns list of (book, chapter, verse, text) tuples
    """
    # Open Bibles repository on GitHub
    # Format: JSON with books/chapters/verses
    asv_urls = [
        "https://raw.githubusercontent.com/seven1m/open-bibles/main/bibles/ASV.json",
        "https://raw.githubusercontent.com/openbiblesociety/bible-corpus/master/bibles/en-ASV.json",
    ]
    
    print("Downloading ASV Bible...")
    
    for url in asv_urls:
        try:
            print(f"Trying: {url}")
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                verses = parse_bible_json(data)
                if verses:
                    print(f"Successfully downloaded {len(verses)} verses!")
                    return verses
        except Exception as e:
            print(f"Failed: {e}")
            continue
    
    return None


def parse_bible_json(data: dict) -> List[Tuple[str, int, int, str]]:
    """Parse Bible JSON into (book, chapter, verse, text) tuples"""
    verses = []
    
    # Common JSON formats
    if isinstance(data, list):
        # Format: [{"book": "Genesis", "chapter": 1, "verse": 1, "text": "..."}, ...]
        for item in data:
            if isinstance(item, dict):
                book = item.get('book', '')
                chapter = item.get('chapter', 0)
                verse = item.get('verse', 0)
                text = item.get('text', '')
                if book and chapter and verse and text:
                    verses.append((book, chapter, verse, text))
    
    elif isinstance(data, dict):
        # Format: {"Genesis": {"1": {"1": "text", "2": "text"}, "2": {...}}, ...}
        for book_name, chapters in data.items():
            if isinstance(chapters, dict):
                for chapter_num, verses_dict in chapters.items():
                    try:
                        chapter = int(chapter_num)
                        if isinstance(verses_dict, dict):
                            for verse_num, text in verses_dict.items():
                                try:
                                    verse = int(verse_num)
                                    if text:
                                        verses.append((book_name, chapter, verse, str(text)))
                                except ValueError:
                                    pass
                    except ValueError:
                        pass
    
    return verses


def download_asv_plain_text():
    """
    Alternative: Download ASV as plain text and parse
    """
    urls = [
        "https://raw.githubusercontent.com/openbiblesociety/bible-corpus/master/bibles/en-ASV.txt",
    ]
    
    for url in urls:
        try:
            print(f"Trying plain text: {url}")
            with urllib.request.urlopen(url, timeout=10) as response:
                text = response.read().decode('utf-8')
                verses = parse_plain_text(text)
                if verses:
                    print(f"Successfully downloaded {len(verses)} verses!")
                    return verses
        except Exception as e:
            print(f"Failed: {e}")
            continue
    
    return None


def parse_plain_text(text: str) -> List[Tuple[str, int, int, str]]:
    """Parse plain text Bible format"""
    verses = []
    
    # Common format: Book Chapter:Verse Text
    pattern = r'(\w+(?:\s+\w+)?)\s+(\d+):(\d+)\s+(.+?)(?=\n\w+\s+\d+:\d+|$)'
    
    matches = re.finditer(pattern, text, re.MULTILINE | re.DOTALL)
    
    for match in matches:
        book = match.group(1).strip()
        chapter = int(match.group(2))
        verse = int(match.group(3))
        text_verse = match.group(4).strip()
        
        if book and chapter and verse and text_verse:
            verses.append((book, chapter, verse, text_verse))
    
    return verses


def save_to_file(verses: List[Tuple[str, int, int, str]], filename: str = "asv_bible.json"):
    """Save verses to JSON file"""
    data = []
    for book, chapter, verse, text in verses:
        data.append({
            "book": book,
            "chapter": chapter,
            "verse": verse,
            "text": text
        })
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(verses)} verses to {filename}")


def load_from_file(filename: str = "asv_bible.json") -> List[Tuple[str, int, int, str]]:
    """Load verses from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        verses = []
        for item in data:
            verses.append((
                item['book'],
                item['chapter'],
                item['verse'],
                item['text']
            ))
        
        return verses
    except FileNotFoundError:
        return None


def main():
    """Main download function"""
    print("=" * 80)
    print("AMERICAN STANDARD BIBLE (ASV) DOWNLOADER")
    print("=" * 80)
    print("\nThe ASV is in the public domain - free to download and use!")
    print()
    
    # Try to download
    verses = download_asv_from_github()
    
    if not verses:
        print("\nTrying alternative source (plain text)...")
        verses = download_asv_plain_text()
    
    if verses:
        print(f"\nSuccess! Downloaded {len(verses)} verses")
        
        # Show sample
        print("\nSample verses:")
        for i, (book, chapter, verse, text) in enumerate(verses[:5], 1):
            print(f"{i}. {book} {chapter}:{verse} - {text[:60]}...")
        
        # Save to file
        save_to_file(verses, "asv_bible.json")
        
        print("\n" + "=" * 80)
        print("DOWNLOAD COMPLETE!")
        print("=" * 80)
        print("\nTo use in your hyperlinked Bible app:")
        print("""
from hyperlinked_bible_app import HyperlinkedBibleApp
import json

# Load Bible
app = HyperlinkedBibleApp()

with open('asv_bible.json', 'r', encoding='utf-8') as f:
    bible_data = json.load(f)

# Add all verses
for item in bible_data:
    app.add_verse(
        item['book'],
        item['chapter'],
        item['verse'],
        item['text']
    )

# Now use the app!
result = app.get_verse_with_hyperlinks("John", 3, 16)
        """)
        
        return verses
    else:
        print("\n" + "=" * 80)
        print("DOWNLOAD FAILED")
        print("=" * 80)
        print("\nAlternative options:")
        print("1. Download manually from:")
        print("   - https://github.com/seven1m/open-bibles")
        print("   - https://github.com/openbiblesociety/bible-corpus")
        print("   - https://asv.ibibles.net/")
        print("\n2. Use the format from the repository")
        print("3. Check internet connection and try again")
        
        return None


if __name__ == "__main__":
    main()
