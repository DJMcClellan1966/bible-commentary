"""Quick script to inspect HTML structure"""
import os
import re

path = r'C:\Users\DJMcC\OneDrive\Desktop\bible-commentary\bible-commentary\data\bible-versions\asv\GEN01.htm'

try:
    # Try different encodings
    for encoding in ['utf-8-sig', 'utf-8', 'latin-1']:
        try:
            with open(path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()
            
            # Write to file for inspection
            with open('html_sample.txt', 'w', encoding='utf-8') as out:
                out.write(content[:3000])
            
            print(f"Successfully read with {encoding}")
            print(f"Length: {len(content)}")
            print(f"\nFirst 500 chars:")
            print(content[:500])
            
            # Check for verse patterns
            print("\n\nLooking for verse patterns...")
            
            # Check for numbers followed by text
            verse_patterns = [
                r'<p[^>]*>.*?(\d+)\s+([A-Z][^<]{20,})',
                r'(\d+)\s+([A-Z][^<\n]{20,})',
                r'\[(\d+)\]\s*([^<\n]{20,})',
            ]
            
            for pattern in verse_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    print(f"\nPattern {pattern} found {len(matches)} matches")
                    print("Sample:", matches[:3])
            
            break
        except Exception as e:
            continue
except Exception as e:
    print(f"Error: {e}")
