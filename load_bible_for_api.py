"""
Pre-load Bible data for the API
Run this once to load all Bible data before starting the server
This makes the API start faster
"""
import os
import sys
import pickle

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from hyperlinked_bible_app import HyperlinkedBibleApp
from load_bible_from_html import load_all_versions_into_app

def main():
    print("="*80)
    print("PRE-LOADING BIBLE DATA FOR API")
    print("="*80)
    print()
    
    base_path = r'C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions'
    
    if not os.path.exists(base_path):
        print(f"ERROR: Bible data path not found: {base_path}")
        print("\nPlease update the path in this script.")
        return
    
    print(f"Loading from: {base_path}")
    print("\nThis will load all 3 Bible versions (may take a few minutes)...")
    print()
    
    # Create app
    app = HyperlinkedBibleApp()
    
    # Load all versions
    total = load_all_versions_into_app(app, base_path)
    
    # Save to cache file
    cache_file = "bible_app_cache.pkl"
    print(f"\nSaving to cache: {cache_file}...")
    try:
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'versions': app.versions,
                'total_verses': total
            }, f)
        print(f"[OK] Saved cache to {cache_file}")
    except Exception as e:
        print(f"Warning: Could not save cache: {e}")
    
    # Statistics
    stats = app.get_stats()
    print("\n" + "="*80)
    print("LOADING COMPLETE")
    print("="*80)
    print(f"\nTotal verses loaded: {total}")
    print(f"Verses in app: {stats['total_verses']}")
    print(f"Versions: {list(app.versions.keys())}")
    print("\n[OK] Bible data is ready!")
    print("\nNow you can start the API server:")
    print("  python start_bible_app.py")


if __name__ == "__main__":
    main()