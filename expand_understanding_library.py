"""
Expand Understanding Library
Step 1: Automatically add more verses to the library
"""
import os
from pathlib import Path
from bible_understanding_library import UnderstandingGenerator, UnderstandingLibrary
from load_bible_from_html import load_all_versions_into_app
from hyperlinked_bible_app import HyperlinkedBibleApp


def expand_library_with_bible_verses(bible_path: str = None, max_verses: int = 100):
    """
    Expand the understanding library by loading verses from the Bible
    and generating understanding for them
    
    Args:
        bible_path: Path to Bible versions folder
        max_verses: Maximum number of verses to process
    """
    print("=" * 80)
    print("EXPANDING UNDERSTANDING LIBRARY")
    print("=" * 80)
    print()
    
    # Initialize
    generator = UnderstandingGenerator()
    library = UnderstandingLibrary()
    
    # Load Bible if path provided
    app = HyperlinkedBibleApp()
    
    if bible_path and os.path.exists(bible_path):
        print(f"Loading Bible from: {bible_path}")
        load_all_versions_into_app(app, bible_path)
        print(f"Loaded {len(app.versions)} Bible versions")
    else:
        # Use default path
        default_path = r"C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions"
        if os.path.exists(default_path):
            print(f"Loading Bible from default path: {default_path}")
            load_all_versions_into_app(app, default_path)
            print(f"Loaded {len(app.versions)} Bible versions")
        else:
            print("No Bible path found. Using sample verses only.")
            return expand_with_sample_verses(library, generator, max_verses)
    
    # Get verses from ASV version
    asv_verses = app.versions.get('asv', {})
    if not asv_verses:
        print("ASV version not found. Using sample verses.")
        return expand_with_sample_verses(library, generator, max_verses)
    
    # Collect verses with references
    verses_to_process = []
    count = 0
    
    print(f"\nCollecting verses from ASV...")
    
    # Try different structures
    if isinstance(asv_verses, dict):
        for book_name, book_data in asv_verses.items():
            if isinstance(book_data, dict):
                for chapter_num, chapter_data in book_data.items():
                    if isinstance(chapter_data, dict):
                        for verse_num, verse_text in chapter_data.items():
                            if verse_text and isinstance(verse_text, str) and len(verse_text.strip()) > 10:
                                verse_ref = f"{book_name} {chapter_num}:{verse_num}"
                                verses_to_process.append((verse_ref, verse_text))
                                count += 1
                                
                                if count >= max_verses:
                                    break
                    if count >= max_verses:
                        break
            if count >= max_verses:
                break
    
    # If still no verses, try accessing through app methods
    if not verses_to_process:
        print("Trying alternative method to access verses...")
        # Sample some popular verses directly
        sample_refs = [
            ("John 3:16", "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life."),
            ("John 1:1", "In the beginning was the Word, and the Word was with God, and the Word was God."),
            ("John 14:6", "Jesus saith unto him, I am the way, and the truth, and the life: no one cometh unto the Father, but by me."),
            ("Romans 3:23", "For all have sinned, and fall short of the glory of God;"),
            ("Ephesians 2:8", "For by grace have ye been saved through faith; and that not of yourselves, it is the gift of God;"),
        ]
        
        # Try to get actual verse text from app
        for ref, default_text in sample_refs:
            try:
                # Parse reference
                import re
                match = re.match(r"(.+?)\s+(\d+):(\d+)", ref)
                if match:
                    book = match.group(1).strip()
                    chapter = int(match.group(2))
                    verse = int(match.group(3))
                    
                    # Try to get from app
                    verse_text = app.get_verse_text(book, chapter, verse, version='asv')
                    if verse_text:
                        verses_to_process.append((ref, verse_text))
                        count += 1
                    else:
                        verses_to_process.append((ref, default_text))
                        count += 1
                    
                    if count >= max_verses:
                        break
            except:
                verses_to_process.append((ref, default_text))
                count += 1
                if count >= max_verses:
                    break
    
    print(f"Found {len(verses_to_process)} verses to process")
    
    # Check what's already in library
    existing_verses = set(library.list_all_verses())
    new_verses = [(ref, text) for ref, text in verses_to_process if ref not in existing_verses]
    
    print(f"Already in library: {len(existing_verses)}")
    print(f"New verses to add: {len(new_verses)}")
    print()
    
    # Generate understanding for new verses
    added = 0
    skipped = 0
    
    for i, (verse_ref, verse_text) in enumerate(new_verses, 1):
        print(f"[{i}/{len(new_verses)}] Processing {verse_ref}...", end=" ")
        
        try:
            understanding = generator.generate_verse_understanding(verse_ref, verse_text)
            library.add_verse_understanding(understanding)
            added += 1
            print("OK")
        except Exception as e:
            print(f"ERROR: {e}")
            skipped += 1
    
    # Show results
    stats = library.get_stats()
    print()
    print("=" * 80)
    print("EXPANSION COMPLETE")
    print("=" * 80)
    print(f"Added: {added} new verses")
    print(f"Skipped: {skipped} verses")
    print(f"Total in library: {stats['total_verses']}")
    print(f"Last updated: {stats['last_updated']}")
    print()
    print(f"Library location: {library.library_path}")
    print("=" * 80)
    
    return {
        "added": added,
        "skipped": skipped,
        "total": stats['total_verses']
    }


def expand_with_sample_verses(library: UnderstandingLibrary, 
                              generator: UnderstandingGenerator,
                              max_verses: int = 50):
    """Expand with additional sample verses"""
    print("Expanding with sample verses...")
    
    sample_verses = [
        ("1 Corinthians 13:4-7", "Love is patient, love is kind. It does not envy, it does not boast, it is not proud. It does not dishonor others, it is not self-seeking, it is not easily angered, it keeps no record of wrongs. Love does not delight in evil but rejoices with the truth. It always protects, always trusts, always hopes, always perseveres."),
        ("Galatians 5:22-23", "But the fruit of the Spirit is love, joy, peace, forbearance, kindness, goodness, faithfulness, gentleness and self-control. Against such things there is no law."),
        ("Ephesians 2:8-9", "For by grace you have been saved through faith. And this is not your own doing; it is the gift of God, not a result of works, so that no one may boast."),
        ("Isaiah 40:31", "But they that wait for the Lord shall renew their strength; they shall mount up with wings as eagles; they shall run, and not be weary; and they shall walk, and not faint."),
        ("Joshua 1:9", "Have not I commanded thee? Be strong and of a good courage; be not afraid, neither be thou dismayed: for the Lord thy God is with thee whithersoever thou goest."),
        ("Psalm 119:105", "Thy word is a lamp unto my feet, and a light unto my path."),
        ("Isaiah 55:8-9", "For my thoughts are not your thoughts, neither are your ways my ways, saith the Lord. For as the heavens are higher than the earth, so are my ways higher than your ways, and my thoughts than your thoughts."),
        ("Hebrews 11:1", "Now faith is the substance of things hoped for, the evidence of things not seen."),
        ("James 1:2-3", "My brethren, count it all joy when ye fall into divers temptations; Knowing this, that the trying of your faith worketh patience."),
        ("1 John 4:8", "He that loveth not knoweth not God; for God is love."),
        ("Micah 6:8", "He hath shewed thee, O man, what is good; and what doth the Lord require of thee, but to do justly, and to love mercy, and to walk humbly with thy God?"),
        ("Matthew 5:3-4", "Blessed are the poor in spirit: for theirs is the kingdom of heaven. Blessed are they that mourn: for they shall be comforted."),
        ("John 15:13", "Greater love hath no man than this, that a man lay down his life for his friends."),
        ("Romans 12:2", "And be not conformed to this world: but be ye transformed by the renewing of your mind, that ye may prove what is that good, and acceptable, and perfect, will of God."),
        ("2 Corinthians 5:17", "Therefore if any man be in Christ, he is a new creature: old things are passed away; behold, all things are become new."),
    ]
    
    existing = set(library.list_all_verses())
    new_verses = [(ref, text) for ref, text in sample_verses if ref not in existing]
    
    added = 0
    for verse_ref, verse_text in new_verses[:max_verses]:
        print(f"  Adding {verse_ref}...", end=" ")
        try:
            understanding = generator.generate_verse_understanding(verse_ref, verse_text)
            library.add_verse_understanding(understanding)
            added += 1
            print("OK")
        except Exception as e:
            print(f"ERROR: {e}")
    
    print(f"\nAdded {added} sample verses")
    return {"added": added, "total": library.get_stats()['total_verses']}


if __name__ == "__main__":
    # Expand library
    result = expand_library_with_bible_verses(max_verses=100)
    print(f"\nResult: {result}")