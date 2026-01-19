# Bible Commentary Agent - Usage Guide

## Quick Examples

### 1. Using the API (Recommended)

The API server is running at `http://localhost:8000`

#### Build a Commentary

**Using curl:**
```bash
curl -X POST "http://localhost:8000/api/commentary" ^
  -H "Content-Type: application/json" ^
  -d "{\"book\": \"Genesis\", \"chapter\": 1, \"verse\": 1, \"synthesize\": true}"
```

**Using PowerShell:**
```powershell
$body = @{
    book = "Genesis"
    chapter = 1
    verse = 1
    synthesize = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/commentary" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

#### Get Commentary by Category

```powershell
# Get Church Fathers commentary
Invoke-RestMethod -Uri "http://localhost:8000/api/commentary/Genesis/1/1/church_fathers"

# Get Modern commentaries
Invoke-RestMethod -Uri "http://localhost:8000/api/commentary/Genesis/1/1/modern"

# Get Jewish commentaries
Invoke-RestMethod -Uri "http://localhost:8000/api/commentary/Genesis/1/1/jewish"
```

#### Search Commentaries

```powershell
$body = @{
    query = "creation"
    book = "Genesis"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/search" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

#### Get Improvement Suggestions

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/suggestions/Genesis/1/1"
```

### 2. Using the CLI

#### Build Commentary
```bash
python cli.py build --book Genesis --chapter 1 --verse 1
```

#### Get by Category
```bash
python cli.py get --book Genesis --chapter 1 --verse 1 --category church_fathers
```

#### Search
```bash
python cli.py search --query "creation" --book Genesis
```

#### Get Suggestions
```bash
python cli.py suggest --book Genesis --chapter 1 --verse 1
```

#### Save to File
```bash
python cli.py build --book Genesis --chapter 1 --verse 1 --output genesis_1_1.json
```

### 3. Using Python Directly

```python
from agent import BibleCommentaryAgent
from models import init_db

# Initialize
init_db()
agent = BibleCommentaryAgent()

# Build commentary
result = agent.build_commentary(
    book="Genesis",
    chapter=1,
    verse=1,
    source_types=["modern", "church_fathers", "jewish"],
    synthesize=True
)

# Print synthesized commentary
print(result['synthesized'])

# Get by category
fathers = agent.get_commentary_by_category(
    book="Genesis",
    chapter=1,
    verse=1,
    category="church_fathers"
)

# Search
results = agent.search_commentaries(
    query="creation",
    book="Genesis"
)

# Get suggestions
suggestions = agent.suggest_improvements(
    book="Genesis",
    chapter=1,
    verse=1
)
```

## Common Use Cases

### Use Case 1: Study a Specific Verse

```powershell
# Get comprehensive commentary
Invoke-RestMethod -Uri "http://localhost:8000/api/commentary/John/3/16"
```

### Use Case 2: Compare Different Traditions

```powershell
# Get Church Fathers view
$fathers = Invoke-RestMethod -Uri "http://localhost:8000/api/commentary/Genesis/1/1/church_fathers"

# Get Modern view
$modern = Invoke-RestMethod -Uri "http://localhost:8000/api/commentary/Genesis/1/1/modern"

# Get Jewish view
$jewish = Invoke-RestMethod -Uri "http://localhost:8000/api/commentary/Genesis/1/1/jewish"
```

### Use Case 3: Research a Topic

```powershell
# Search for commentaries about "love"
$results = Invoke-RestMethod -Uri "http://localhost:8000/api/search" `
  -Method POST `
  -ContentType "application/json" `
  -Body (@{query="love"} | ConvertTo-Json)
```

### Use Case 4: Process Multiple Verses

```python
from agent import BibleCommentaryAgent
from models import init_db

init_db()
agent = BibleCommentaryAgent()

# Process a chapter
for verse in range(1, 32):  # Genesis 1 has 31 verses
    result = agent.build_commentary(
        book="Genesis",
        chapter=1,
        verse=verse,
        synthesize=True
    )
    print(f"Verse {verse}: {len(result['commentaries'])} sources found")
```

## Source Types

- **church_fathers**: Early Christian writers (Augustine, Chrysostom, etc.)
- **middle_ages**: Medieval scholars (Aquinas, etc.)
- **modern**: Contemporary biblical scholars
- **jewish**: Jewish commentaries (Sefaria, Chabad, etc.)
- **popes**: Papal documents and encyclicals

## Tips

1. **Start with single verses** to test before batch processing
2. **Use specific source types** if you want focused results
3. **Enable synthesis** for AI-powered combined commentary
4. **Save results** to JSON files for later analysis
5. **Check suggestions** to find additional sources

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive API documentation where you can:
- See all available endpoints
- Test API calls directly in your browser
- View request/response schemas
- Try different parameters
