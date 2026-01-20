# Free ASV Bible Download Sources

## ✅ American Standard Version (ASV) - Public Domain - Free to Download!

The ASV (1901) is in the public domain, meaning you can download, use, and modify it freely.

---

## 🎯 Best Download Options

### Option 1: GitHub - Open Bible Society (Recommended)

**Repository**: https://github.com/openbiblesociety/bible-corpus

**Direct Download Links** (try these):
- **JSON Format**: 
  - https://github.com/openbiblesociety/bible-corpus/raw/master/bibles/en-ASV.json
  - Or clone the repo: `git clone https://github.com/openbiblesociety/bible-corpus.git`
  
- **How to download**:
  1. Go to https://github.com/openbiblesociety/bible-corpus
  2. Click "Code" → "Download ZIP"
  3. Extract and find `bibles/en-ASV.json` (or other formats)

**Formats available**:
- JSON (best for apps)
- XML/OSIS
- Plain text

---

### Option 2: GitHub - Open Bibles Project

**Repository**: https://github.com/seven1m/open-bibles

**How to download**:
1. Go to https://github.com/seven1m/open-bibles
2. Click "Code" → "Download ZIP"
3. Extract and find ASV in the `bibles/` folder

**Formats**: JSON, XML (OSIS, USFX)

---

### Option 3: Bible Gateway (Web-based)

**URL**: https://www.biblegateway.com/passage/?search=John+3:16&version=ASV

**Note**: ASV is public domain on Bible Gateway. You can:
- Use their API (with limitations)
- Scrape individual verses (check their terms)
- Read online and copy

**API**: https://www.biblegateway.com/passage/ (check their API documentation)

---

### Option 4: iBibles.net

**URL**: https://asv.ibibles.net/

**Format**: Web-based, downloadable options
**Usage**: Can be scraped or used for reference

---

### Option 5: Project Gutenberg

**Search**: "American Standard Version" on https://www.gutenberg.org/

**Format**: Plain text, EPUB
**Best for**: Reading, simple parsing

---

### Option 6: Sword of the Spirit

**URL**: https://sword-of-the-spirit.org/

**Format**: Multiple formats available
**Note**: Check their download options

---

## 💻 Quick Download Methods

### Method 1: Clone GitHub Repository

```bash
# Clone Open Bible Society repository
git clone https://github.com/openbiblesociety/bible-corpus.git
cd bible-corpus/bibles
# Find en-ASV.json or other ASV files
```

### Method 2: Download ZIP from GitHub

1. Go to https://github.com/openbiblesociety/bible-corpus
2. Click "Code" → "Download ZIP"
3. Extract ZIP file
4. Navigate to `bibles/` folder
5. Find `en-ASV.json` or other ASV formats

### Method 3: Use wget/curl (Linux/Mac)

```bash
# Try direct download
wget https://github.com/openbiblesociety/bible-corpus/raw/master/bibles/en-ASV.json

# Or
curl -O https://github.com/openbiblesociety/bible-corpus/raw/master/bibles/en-ASV.json
```

### Method 4: Manual Download from GitHub Web Interface

1. Go to https://github.com/openbiblesociety/bible-corpus/tree/master/bibles
2. Find `en-ASV.json` (or other ASV file)
3. Click on the file
4. Click "Raw" button (top right)
5. Save page as `asv_bible.json`

---

## 📝 Expected File Format

Once downloaded, the JSON format should look like:

```json
[
  {
    "book": "Genesis",
    "chapter": 1,
    "verse": 1,
    "text": "In the beginning God created the heaven and the earth."
  },
  {
    "book": "Genesis",
    "chapter": 1,
    "verse": 2,
    "text": "And the earth was waste and void..."
  }
]
```

Or as nested structure:

```json
{
  "Genesis": {
    "1": {
      "1": "In the beginning God created...",
      "2": "And the earth was waste..."
    }
  }
}
```

---

## 🔧 Loading into Your Hyperlinked Bible App

Once you have the file:

```python
from hyperlinked_bible_app import HyperlinkedBibleApp
import json

# Create app
app = HyperlinkedBibleApp()

# Load ASV Bible (adjust filename/path as needed)
with open('en-ASV.json', 'r', encoding='utf-8') as f:
    bible_data = json.load(f)

# Handle different JSON formats
if isinstance(bible_data, list):
    # Format: [{"book": "...", "chapter": 1, "verse": 1, "text": "..."}]
    for item in bible_data:
        app.add_verse(
            item['book'],
            item['chapter'],
            item['verse'],
            item['text']
        )
elif isinstance(bible_data, dict):
    # Format: {"Genesis": {"1": {"1": "text"}}}
    for book_name, chapters in bible_data.items():
        for chapter_num, verses_dict in chapters.items():
            chapter = int(chapter_num)
            if isinstance(verses_dict, dict):
                for verse_num, text in verses_dict.items():
                    verse = int(verse_num)
                    app.add_verse(book_name, chapter, verse, str(text))

print(f"Loaded {len(app.verses)} verses!")

# Now use your hyperlinked Bible!
result = app.get_verse_with_hyperlinks("John", 3, 16, top_k=10)
print(f"Found {len(result['hyperlinks'])} cross-references")
```

---

## ✅ Recommended Approach

**Best for your app**: 
1. **Download from Open Bible Society GitHub** (most reliable, well-maintained)
2. **Use JSON format** (easiest to parse)
3. **Save as `asv_bible.json`** in your project folder
4. **Load using the code above**

---

## 📊 File Size Expectations

- **Full ASV Bible**: ~2-5 MB (JSON format)
- **Number of verses**: ~31,173 verses
- **Number of words**: ~780,000 words

---

## 🎯 Quick Start Checklist

- [ ] Visit https://github.com/openbiblesociety/bible-corpus
- [ ] Download ZIP or clone repository
- [ ] Find `en-ASV.json` in `bibles/` folder
- [ ] Copy to your project folder
- [ ] Load into hyperlinked Bible app using code above
- [ ] Enjoy your AI-powered hyperlinked ASV Bible!

---

The ASV is perfect for your app - it's accurate, readable, and completely free to use!
