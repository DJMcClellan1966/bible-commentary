"""
Load All 3 Bible Versions into Hyperlinked Bible App
Simple wrapper script
"""
from load_bible_from_html import main

if __name__ == "__main__":
    print("Starting to load all Bible versions...")
    print("This may take several minutes for all 3 versions...\n")
    
    app = main()
    
    if app:
        print("\n" + "="*80)
        print("SUCCESS! All Bible versions loaded!")
        print("="*80)
        print("\nYou can now use:")
        print("  app.get_verse_with_hyperlinks('John', 3, 16)")
        print("  app.discover_cross_references('John', 3, 16)")
        print("  app.discover_themes()")
