# Quick Start Guide

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create environment file:**
   ```bash
   # Copy the example and add your API key
   cp .env.example .env
   # Edit .env and add: OPENAI_API_KEY=your_key_here
   ```

3. **Initialize database:**
   ```bash
   python -c "from models import init_db; init_db()"
   ```

## Basic Usage

### Using the CLI

```bash
# Build a commentary for Genesis 1:1
python cli.py build --book Genesis --chapter 1 --verse 1

# Get only Church Fathers commentary
python cli.py get --book Genesis --chapter 1 --verse 1 --category church_fathers

# Search for commentaries
python cli.py search --query "creation" --book Genesis

# Get improvement suggestions
python cli.py suggest --book Genesis --chapter 1 --verse 1
```

### Using the API

1. **Start the server:**
   ```bash
   uvicorn api:app --reload
   ```

2. **Access the API:**
   - API docs: http://localhost:8000/docs
   - Build commentary: POST http://localhost:8000/api/commentary
   - Get commentary: GET http://localhost:8000/api/commentary/Genesis/1/1

### Using Python

```python
from agent import BibleCommentaryAgent
from models import init_db

init_db()
agent = BibleCommentaryAgent()

# Build commentary
result = agent.build_commentary(
    book="Genesis",
    chapter=1,
    verse=1,
    synthesize=True
)

print(result['synthesized'])
```

## Batch Processing

Process entire books or ranges:

```bash
# Process a single chapter
python batch_processor.py --book Genesis --chapter 1

# Process an entire book
python batch_processor.py --book Genesis

# Process a range of books
python batch_processor.py --start-book Genesis --end-book Exodus
```

**Note:** Batch processing can take a very long time. Start with single chapters or verses.

## Source Types

You can specify which sources to use:

- `church_fathers` - Early Christian writers
- `middle_ages` - Medieval scholars
- `modern` - Contemporary scholars
- `jewish` - Jewish commentaries
- `popes` - Papal documents

Example:
```bash
python cli.py build --book Genesis --chapter 1 --verse 1 \
  --source-types church_fathers modern jewish
```

## Tips

1. **Start small:** Test with a few verses before batch processing
2. **Rate limiting:** The scraper includes delays to respect websites
3. **API key:** OpenAI API key is optional but enables AI synthesis
4. **Database:** All commentaries are stored locally in SQLite
5. **Customization:** Edit `config.py` to add more sources

## Troubleshooting

- **No commentaries found:** Some sources may require different URL formats or authentication
- **Scraping errors:** Check internet connection and source availability
- **AI synthesis not working:** Verify OPENAI_API_KEY is set correctly
- **Database errors:** Ensure write permissions in the project directory
