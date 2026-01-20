# Unified Bible Commentary Agent API - Complete Guide

## What This Is

A **unified API** that combines:
- ✅ Understanding Library
- ✅ Commentary API
- ✅ Bible Study Tools
- ✅ All endpoints in one place

---

## Quick Start

### Start the Server

**Easiest way:**
```bash
start_unified_api.bat
```

**Or manually:**
```bash
python unified_bible_api.py
```

### Access the API

Once started, you'll see:
```
Starting server on port 8000...
Access on your computer:
  http://localhost:8000
```

**Open:** `http://localhost:8000`

---

## All Available Endpoints

### Web Interfaces

- **`GET /`** - Root (serves improved interface if available, otherwise web interface)
- **`GET /web`** - Web interface (Understanding Library)
- **`GET /bible-study`** - Bible study interface
- **`GET /bible-ai`** - Bible AI interface
- **`GET /bible-llm`** - Bible LLM interface

### Commentary API

- **`POST /api/commentary`** - Build commentary for a verse
  ```json
  {
    "book": "John",
    "chapter": 3,
    "verse": 16,
    "text": "For God so loved the world...",
    "category": "theological"
  }
  ```

- **`GET /api/commentary/{book}/{chapter}/{verse}/{category}`** - Get commentary by category
  Example: `/api/commentary/John/3/16/theological`

- **`GET /api/search?query=love&category=theological&limit=10`** - Search commentary
  - `query`: Search term
  - `category`: Optional filter
  - `limit`: Max results (default: 10)

- **`GET /api/suggestions/{book}/{chapter}/{verse}`** - Get suggestions
  Example: `/api/suggestions/John/3/16`
  Returns: Related verses, themes, study paths

### Understanding Library API

- **`GET /api/understanding/verse/{verse_ref}`** - Get verse understanding
  Example: `/api/understanding/verse/John 3:16`

- **`GET /api/understanding/verses`** - List all verses in library

- **`GET /api/understanding/stats`** - Get library statistics

- **`POST /api/understanding/generate`** - Generate understanding
  ```json
  {
    "verse_ref": "John 3:16",
    "verse_text": "For God so loved the world..."
  }
  ```

---

## Example Usage

### Get Commentary for a Verse

```bash
curl -X POST http://localhost:8000/api/commentary \
  -H "Content-Type: application/json" \
  -d '{
    "book": "John",
    "chapter": 3,
    "verse": 16,
    "text": "For God so loved the world, that he gave his only begotten Son...",
    "category": "theological"
  }'
```

### Search Commentary

```bash
curl "http://localhost:8000/api/search?query=love&limit=5"
```

### Get Suggestions

```bash
curl "http://localhost:8000/api/suggestions/John/3/16"
```

### Get Understanding

```bash
curl "http://localhost:8000/api/understanding/verse/John 3:16"
```

---

## API Response Examples

### Commentary Response

```json
{
  "reference": "John 3:16",
  "book": "John",
  "chapter": 3,
  "verse": 16,
  "category": "theological",
  "commentary": "This verse reveals the heart of God's love...",
  "themes": ["love", "salvation", "eternal life"],
  "related_verses": [
    {
      "reference": "Romans 5:8",
      "text": "But God commendeth his love...",
      "similarity": 0.85
    }
  ]
}
```

### Suggestions Response

```json
{
  "reference": "John 3:16",
  "suggestions": {
    "related_verses": [
      {
        "reference": "Romans 5:8",
        "text": "But God commendeth his love...",
        "similarity": 0.85
      }
    ],
    "themes": ["love", "salvation"],
    "study_paths": [
      "Explore theme: love",
      "Explore theme: salvation"
    ]
  }
}
```

---

## Integration

### In Your App

```python
import requests

# Get commentary
response = requests.post("http://localhost:8000/api/commentary", json={
    "book": "John",
    "chapter": 3,
    "verse": 16,
    "text": "For God so loved the world...",
    "category": "theological"
})
commentary = response.json()

# Get suggestions
response = requests.get("http://localhost:8000/api/suggestions/John/3/16")
suggestions = response.json()

# Search
response = requests.get("http://localhost:8000/api/search", params={
    "query": "love",
    "limit": 10
})
results = response.json()
```

### In JavaScript

```javascript
// Get commentary
const response = await fetch('http://localhost:8000/api/commentary', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        book: 'John',
        chapter: 3,
        verse: 16,
        text: 'For God so loved the world...',
        category: 'theological'
    })
});
const commentary = await response.json();

// Get suggestions
const suggestions = await fetch('http://localhost:8000/api/suggestions/John/3/16')
    .then(r => r.json());

// Search
const results = await fetch('http://localhost:8000/api/search?query=love&limit=10')
    .then(r => r.json());
```

---

## Features

### ✅ Unified API
- All endpoints in one place
- Consistent response format
- Easy to use

### ✅ Understanding Library Integration
- Automatic understanding generation
- Verse and passage support
- Theme-based search

### ✅ Commentary API
- Build commentary on demand
- Category-based filtering
- Search functionality
- Suggestions for study

### ✅ Web Interfaces
- Understanding Library interface
- Bible study tools
- AI and LLM interfaces

---

## API Documentation

### Interactive Docs

Once the server is running:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Root Endpoint

Visit `http://localhost:8000/` to see:
- All available endpoints
- API version
- Status information

---

## Troubleshooting

### Port Already in Use

The server automatically finds a free port. Check the console output for the actual port number.

### Endpoint Not Found

Make sure:
1. Server is running
2. Using correct endpoint path
3. Check `/docs` for available endpoints

### No Commentary Found

If commentary doesn't exist:
1. Use `/api/commentary` POST to generate it
2. Or use `/api/understanding/generate` to create understanding

---

## Summary

**You now have:**
- ✅ Unified API with all endpoints
- ✅ Understanding Library integrated
- ✅ Commentary API working
- ✅ Web interfaces available
- ✅ Search and suggestions
- ✅ Category filtering

**To use:**
1. Run: `python unified_bible_api.py`
2. Open: `http://localhost:8000`
3. Use any endpoint you need!

**Everything is unified and ready to use!**