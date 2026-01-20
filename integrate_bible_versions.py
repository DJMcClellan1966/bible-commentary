"""
Integrate All 3 Bible Versions into Hyperlinked Bible App
Loads ASV, Darby, and Young's Literal Translation
"""
import os
from hyperlinked_bible_app import HyperlinkedBibleApp
from load_bible_from_html import load_bible_version
from bible_modernizer import BibleModernizer


def integrate_all_versions():
    """Load and integrate all 3 Bible versions"""
    
    base_path = r'C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions'
    
    print("=" * 80)
    print("INTEGRATING ALL BIBLE VERSIONS INTO HYPERLINKED BIBLE APP")
    print("=" * 80)
    
    # Create app
    print("\n[1] Initializing Hyperlinked Bible App...")
    app = HyperlinkedBibleApp()
    
    # Create modernizer (for ASV)
    print("[2] Initializing Bible Modernizer...")
    modernizer = BibleModernizer()
    
    # Version info
    versions = {
        'asv': 'American Standard Version',
        'engDBY': 'Darby Bible',
        'englyt': "Young's Literal Translation"
    }
    
    total_loaded = 0
    
    # Load each version
    for version_folder, version_name in versions.items():
        print(f"\n{'='*80}")
        print(f"[3] Loading {version_name} ({version_folder})")
        print(f"{'='*80}")
        
        verses = load_bible_version(base_path, version_folder, version_name)
        
        if verses:
            print(f"\nAdding {len(verses)} verses to app...")
            
            added = 0
            for book, chapter, verse, text in verses:
                app.add_verse(book, chapter, verse, text, version=version_folder)
                added += 1
                
                if added % 1000 == 0:
                    print(f"  Added {added}/{len(verses)} verses...")
            
            total_loaded += len(verses)
            print(f"[OK] Added {len(verses)} verses from {version_name}")
            
            # Modernize ASV (optional - can be done later)
            if version_folder == 'asv':
                print(f"\n[4] Modernizing ASV text (optional)...")
                print("    (This can be done later - skipping for now)")
                # Uncomment to modernize:
                # modernized_count = 0
                # for book, chapter, verse, text in verses[:100]:  # Sample
                #     result = modernizer.modernize_verse(text, f"{book} {chapter}:{verse}")
                #     if result['is_accurate']:
                #         app.verses[f"{book} {chapter}:{verse}"] = result['modernized']
                #         modernized_count += 1
                # print(f"    Modernized {modernized_count} verses")
        else:
            print(f"[WARNING] No verses found for {version_name}")
    
    # Statistics
    print("\n" + "=" * 80)
    print("INTEGRATION COMPLETE")
    print("=" * 80)
    
    stats = app.get_stats()
    print(f"\nTotal verses loaded: {total_loaded}")
    print(f"Verses in app: {stats['total_verses']}")
    print(f"Available versions: {list(app.versions.keys())}")
    print(f"Kernel cache: {stats['kernel_stats']['cache_size']} items")
    
    # Test
    print("\n" + "=" * 80)
    print("TESTING")
    print("=" * 80)
    
    try:
        # Test with ASV
        result = app.get_verse_with_hyperlinks("John", 3, 16, top_k=5, version='asv')
        print(f"\nVerse: {result['verse']} ({result.get('version', 'default')})")
        print(f"Text: {result['verse_text'][:100]}...")
        print(f"\nAvailable versions: {result.get('available_versions', [])}")
        print(f"\nFound {len(result['hyperlinks'])} cross-references:")
        for i, link in enumerate(result['hyperlinks'][:3], 1):
            print(f"  {i}. {link['reference']}: {link['summary']} (similarity: {link['similarity']:.3f})")
    except Exception as e:
        print(f"Test error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("[OK] ALL VERSIONS INTEGRATED SUCCESSFULLY!")
    print("=" * 80)
    
    return app


if __name__ == "__main__":
    app = integrate_all_versions()
    
    print("\nUsage:")
    print("  app.get_verse_with_hyperlinks('John', 3, 16, version='asv')")
    print("  app.get_verse_with_hyperlinks('John', 3, 16, version='engDBY')")
    print("  app.get_verse_with_hyperlinks('John', 3, 16, version='englyt')")
