"""
Generate Passage Understanding
Step 4: Create understanding for entire chapters/passages
"""
import os
import re
from pathlib import Path
from typing import List, Tuple
from bible_understanding_library import UnderstandingGenerator, UnderstandingLibrary
from load_bible_from_html import load_all_versions_into_app
from hyperlinked_bible_app import HyperlinkedBibleApp


def parse_reference(ref: str):
    """Parse verse reference into book, chapter, verse"""
    # Handle ranges like "John 3:16-17"
    if '-' in ref:
        ref = ref.split('-')[0]
    
    match = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
    if match:
        return match.group(1).strip(), int(match.group(2)), int(match.group(3))
    return None, 0, 0


def get_verse_text(app: HyperlinkedBibleApp, book: str, chapter: int, verse: int, version: str = 'asv') -> str:
    """Get verse text from app"""
    try:
        return app.get_verse_text(book, chapter, verse, version=version)
    except:
        return None


def get_passage_verses(app: HyperlinkedBibleApp, book: str, chapter: int, 
                      start_verse: int, end_verse: int, version: str = 'asv') -> List[Tuple[str, str]]:
    """Get all verses in a passage"""
    verses = []
    for verse_num in range(start_verse, end_verse + 1):
        verse_text = get_verse_text(app, book, chapter, verse_num, version)
        if verse_text:
            verse_ref = f"{book} {chapter}:{verse_num}"
            verses.append((verse_ref, verse_text))
    return verses


def generate_chapter_understanding(app: HyperlinkedBibleApp, 
                                 book: str, chapter: int,
                                 library: UnderstandingLibrary,
                                 generator: UnderstandingGenerator,
                                 version: str = 'asv'):
    """Generate understanding for an entire chapter"""
    print(f"\nGenerating understanding for {book} {chapter}...")
    
    # Get all verses in chapter
    verses = []
    verse_num = 1
    
    while True:
        verse_text = get_verse_text(app, book, chapter, verse_num, version)
        if not verse_text:
            break
        verse_ref = f"{book} {chapter}:{verse_num}"
        verses.append((verse_ref, verse_text))
        verse_num += 1
        
        # Safety limit
        if verse_num > 200:
            break
    
    if not verses:
        print(f"  No verses found for {book} {chapter}")
        return None
    
    print(f"  Found {len(verses)} verses")
    
    # Generate passage understanding
    passage_ref = f"{book} {chapter}"
    understanding = generator.generate_passage_understanding(passage_ref, verses)
    
    # Add to library
    library.add_passage_understanding(understanding)
    
    print(f"  [OK] Added to library")
    
    return understanding


def generate_passage_understanding(app: HyperlinkedBibleApp,
                                   passage_ref: str,
                                   library: UnderstandingLibrary,
                                   generator: UnderstandingGenerator,
                                   version: str = 'asv'):
    """Generate understanding for a specific passage (e.g., "John 3:16-21")"""
    print(f"\nGenerating understanding for {passage_ref}...")
    
    # Parse passage reference
    # Format: "Book Chapter:StartVerse-EndVerse" or "Book Chapter:Verse"
    match = re.match(r"(.+?)\s+(\d+):(\d+)(?:-(\d+))?", passage_ref)
    if not match:
        print(f"  Invalid passage reference: {passage_ref}")
        return None
    
    book = match.group(1).strip()
    chapter = int(match.group(2))
    start_verse = int(match.group(3))
    end_verse = int(match.group(4)) if match.group(4) else start_verse
    
    # Get verses
    verses = get_passage_verses(app, book, chapter, start_verse, end_verse, version)
    
    if not verses:
        print(f"  No verses found for {passage_ref}")
        return None
    
    print(f"  Found {len(verses)} verses")
    
    # Generate understanding
    understanding = generator.generate_passage_understanding(passage_ref, verses)
    
    # Add to library
    library.add_passage_understanding(understanding)
    
    print(f"  [OK] Added to library")
    
    return understanding


def generate_popular_passages(bible_path: str = None):
    """Generate understanding for popular Bible passages"""
    print("=" * 80)
    print("GENERATING PASSAGE UNDERSTANDING")
    print("=" * 80)
    
    # Initialize
    app = HyperlinkedBibleApp()
    library = UnderstandingLibrary()
    generator = UnderstandingGenerator()
    
    # Load Bible
    if bible_path and os.path.exists(bible_path):
        print(f"\nLoading Bible from: {bible_path}")
        load_all_versions_into_app(app, bible_path)
    else:
        default_path = r"C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions"
        if os.path.exists(default_path):
            print(f"\nLoading Bible from default path")
            load_all_versions_into_app(app, default_path)
        else:
            print("No Bible path found. Cannot generate passage understanding.")
            return
    
    # Popular passages to generate
    popular_passages = [
        "John 3:16-21",      # The most famous passage
        "Psalm 23:1-6",      # The Lord is my shepherd
        "1 Corinthians 13:4-7",  # Love chapter
        "Romans 8:28-30",    # All things work together
        "Matthew 5:3-12",    # Beatitudes
        "Philippians 4:13",  # I can do all things
        "Isaiah 40:28-31",   # They that wait upon the Lord
        "Jeremiah 29:11-13", # Plans to prosper you
    ]
    
    print(f"\nGenerating understanding for {len(popular_passages)} popular passages...")
    
    generated = 0
    skipped = 0
    
    for passage_ref in popular_passages:
        try:
            result = generate_passage_understanding(
                app, passage_ref, library, generator
            )
            if result:
                generated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            skipped += 1
    
    # Show results
    stats = library.get_stats()
    print()
    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print(f"Generated: {generated} passages")
    print(f"Skipped: {skipped} passages")
    print(f"Total passages in library: {stats['total_passages']}")
    print(f"Total entries: {stats['total_entries']}")
    print()
    print(f"Library location: {library.library_path}")
    print("=" * 80)
    
    return {
        "generated": generated,
        "skipped": skipped,
        "total_passages": stats['total_passages']
    }


if __name__ == "__main__":
    result = generate_popular_passages()
    print(f"\nResult: {result}")