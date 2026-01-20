# How to Download American Standard Bible (ASV) - Free & Legal

## ✅ Good News: ASV is Public Domain!

The American Standard Version (ASV, 1901) is in the **public domain**, meaning it's completely free to download, use, and modify.

---

## 🚀 Quick Download (Automated)

I've created a download script for you:

```bash
python download_asv_bible.py
```

This will:
1. Download ASV from GitHub repositories
2. Parse it into (book, chapter, verse, text) format
3. Save to `asv_bible.json`
4. Ready to use in your hyperlinked Bible app!

---

## 📥 Manual Download Options

### Option 1: GitHub Repositories (Recommended for Developers)

**Open Bibles Repository:**
- URL: https://github.com/seven1m/open-bibles
- Contains: Multiple Bible versions including ASV
- Format: JSON, XML (OSIS, USFX)
- Best for: Building apps, structured data

**Open Bible Society Repository:**
- URL: https://github.com/openbiblesociety/bible-corpus
- Contains: ASV in multiple formats
- Format: JSON, XML, plain text
- Best for: Structured Bible data

**Download Link:**
```
https://raw.githubusercontent.com/openbiblesociety/bible-corpus/master/bibles/en-ASV.json
```

### Option 2: Bible Gateway (Online Reading)

- URL: https://www.biblegateway.com/passage/?search=John+3:16&version=ASV
- Format: Web-based (can scrape or use API)
- Note: ASV is public domain on Bible Gateway

### Option 3: Project Gutenberg Style

- Search for "American Standard Version" on Project Gutenberg
- Format: Plain text, EPUB
- Best for: Reading, simple parsing

### Option 4: iBibles.net

- URL: https://asv.ibibles.net/
- Format: Web-based, downloadable options
- Best for: Web viewing, some download formats

---

## 💻 Using Downloaded ASV in Your App

### Load from JSON File

```python
from hyperlinked_bible_app import HyperlinkedBibleApp
import json

# Create app
app = HyperlinkedBibleApp()

# Load ASV Bible
with open('asv_bible.json', 'r', encoding='utf-8') as f:
    bible_data = json.load(f)

# Add all verses
print(f"Loading {len(bible_data)} verses...")
for item in bible_data:
    app.add_verse(
        item['book'],
        item['chapter'],
        item['verse'],
        item['text']
    )

print(f"Loaded {len(app.verses)} verses!")

# Now use it!
result = app.get_verse_with_hyperlinks("John", 3, 16, top_k=10)
print(f"Found {len(result['hyperlinks'])} cross-references")
```

### Load from Different Formats

**If you have XML/OSIS format:**
```python
import xml.etree.ElementTree as ET

tree = ET.parse('asv_bible.xml')
root = tree.getroot()

# Parse XML structure (format depends on OSIS structure)
for verse in root.findall('.//verse'):
    book = verse.get('book')
    chapter = int(verse.get('chapter'))
    verse_num = int(verse.get('verse'))
    text = verse.text
    
    app.add_verse(book, chapter, verse_num, text)
```

**If you have plain text:**
```python
import re

with open('asv_bible.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Parse format like "Genesis 1:1 In the beginning..."
pattern = r'(\w+(?:\s+\w+)?)\s+(\d+):(\d+)\s+(.+?)(?=\n\w+\s+\d+:\d+|$)'

for match in re.finditer(pattern, content):
    book = match.group(1)
    chapter = int(match.group(2))
    verse = int(match.group(3))
    text = match.group(4).strip()
    
    app.add_verse(book, chapter, verse, text)
```

---

## 📊 Expected Data

The ASV Bible contains approximately:
- **66 books** (39 Old Testament, 27 New Testament)
- **31,173 verses** total
- **~780,000 words**

---

## 🔧 Troubleshooting

### Download Script Fails

1. **Check internet connection**
2. **Try manual download** from GitHub
3. **Use different URL** (the script tries multiple sources)

### Format Issues

1. **Check file format** (JSON, XML, plain text)
2. **Verify encoding** (should be UTF-8)
3. **Check structure** matches expected format

### Loading into App

1. **Verify JSON structure** matches:
   ```json
   [
     {
       "book": "Genesis",
       "chapter": 1,
       "verse": 1,
       "text": "In the beginning God created..."
     }
   ]
   ```

2. **Check book names** match your app's expected format
3. **Verify chapter/verse** are integers

---

## 📚 Additional Resources

### Bible Data Repositories

1. **Open Bibles** - https://github.com/seven1m/open-bibles
   - Multiple translations
   - Multiple formats
   - Well maintained

2. **Open Bible Society** - https://github.com/openbiblesociety/bible-corpus
   - Extensive corpus
   - Multiple languages
   - Structured data

3. **Unfolding Word** - https://github.com/unfoldingWord
   - Modern Bible data
   - Multiple formats

### License Information

- **ASV (1901)**: Public Domain ✅
- **No copyright restrictions**
- **Free to use, modify, distribute**

---

## ✅ Quick Start Checklist

- [ ] Run `python download_asv_bible.py`
- [ ] Verify `asv_bible.json` was created
- [ ] Load into hyperlinked Bible app
- [ ] Test with a few verses
- [ ] Enjoy your AI-powered hyperlinked Bible!

---

## 🎯 Next Steps

Once downloaded:

1. **Load into app**: Use the code above to load ASV
2. **Generate hyperlinks**: Run discovery for all verses
3. **Export format**: Format for web, mobile, or print
4. **Share**: Your hyperlinked ASV Bible is ready!

The ASV is perfect for your hyperlinked Bible app - it's accurate, readable, and completely free to use!
