# Bible Commentary Agent

An AI-powered agent that builds comprehensive Bible commentaries by gathering insights from Church Fathers, Medieval scholars, Modern scholars, Jewish sources, Popes, and other authoritative sources.

## Features

- **Comprehensive Source Coverage**: Automatically scrapes and collects commentaries from:
  - Church Fathers (Augustine, Chrysostom, Jerome, etc.)
  - Medieval scholars (Aquinas, etc.)
  - Modern biblical scholars
  - Jewish sources (Sefaria, Chabad, etc.)
  - Papal documents and encyclicals
  - And more as the agent learns

- **AI-Powered Synthesis**: Uses AI to synthesize multiple commentaries into coherent, insightful readings that:
  - Bring out underlying messages and themes
  - Enhance understanding of biblical texts
  - Integrate insights from different traditions
  - Highlight key theological, historical, and literary points

- **Flexible Search**: Search commentaries by:
  - Book, chapter, and verse
  - Natural language queries
  - Source type/category
  - Author or tradition

- **Learning & Improvement**: The agent suggests better methods and additional sources over time

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bible-commentary
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. Initialize the database:
```bash
python -c "from models import init_db; init_db()"
```

## Usage

### API Server

Start the FastAPI server:
```bash
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

#### API Endpoints

- `GET /` - API information
- `POST /api/commentary` - Build commentary for a verse
- `GET /api/commentary/{book}/{chapter}/{verse}` - Get commentary
- `GET /api/commentary/{book}/{chapter}/{verse}/{category}` - Get commentary by category
- `POST /api/search` - Search commentaries
- `GET /api/suggestions/{book}/{chapter}/{verse}` - Get improvement suggestions
- `GET /api/books` - List all Bible books

#### Example API Calls

```bash
# Build commentary for Genesis 1:1
curl -X POST "http://localhost:8000/api/commentary" \
  -H "Content-Type: application/json" \
  -d '{"book": "Genesis", "chapter": 1, "verse": 1, "synthesize": true}'

# Get Church Fathers commentary
curl "http://localhost:8000/api/commentary/Genesis/1/1/church_fathers"

# Search commentaries
curl -X POST "http://localhost:8000/api/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "creation", "book": "Genesis"}'
```

### Command Line Interface

```bash
# Build commentary for a verse
python cli.py build --book Genesis --chapter 1 --verse 1 --synthesize

# Get commentary by category
python cli.py get --book Genesis --chapter 1 --verse 1 --category church_fathers

# Search commentaries
python cli.py search --query "creation" --book Genesis

# Get improvement suggestions
python cli.py suggest --book Genesis --chapter 1 --verse 1

# Save output to file
python cli.py build --book Genesis --chapter 1 --verse 1 --output commentary.json
```

## Project Structure

```
bible-commentary/
├── api.py              # FastAPI application
├── agent.py            # Main AI agent logic
├── scraper.py          # Web scraping module
├── models.py           # Database models
├── config.py           # Configuration settings
├── cli.py              # Command-line interface
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Configuration

Edit `config.py` to customize:
- Commentary sources and URLs
- AI model settings
- Scraping parameters
- Database configuration

## Database

The agent uses SQLite by default (configurable to PostgreSQL, MySQL, etc.). The database stores:
- Commentaries with metadata (book, chapter, verse, source, author)
- Search history
- Source categorization

## Source Types

- `church_fathers`: Early Christian writers (1st-8th centuries)
- `middle_ages`: Medieval scholars (9th-15th centuries)
- `modern`: Contemporary biblical scholars
- `jewish`: Jewish commentaries and rabbinic sources
- `popes`: Papal documents and encyclicals
- `other`: Additional sources

## Contributing

Contributions are welcome! The agent is designed to learn and improve over time. You can:
- Add new commentary sources
- Improve scraping methods
- Enhance AI synthesis prompts
- Add new search capabilities

## License

[Specify your license here]

## Notes

- Web scraping respects robots.txt and rate limits
- Some sources may require API keys or authentication
- The agent works best with an OpenAI API key for synthesis features
- Processing all 66 books from Genesis to Revelation will take significant time
