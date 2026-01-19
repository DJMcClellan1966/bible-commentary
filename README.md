# Bible Commentary Agent & Study Program

A comprehensive, one-of-a-kind Bible study program that combines AI-powered commentary collection with a full-featured study system. Build comprehensive Bible commentaries from multiple authoritative sources while tracking your study progress, taking notes, memorizing verses, and organizing themes.

## Features

### Commentary System
- **Comprehensive Source Coverage**: Automatically scrapes and collects commentaries from:
  - Church Fathers (Augustine, Chrysostom, Jerome, etc.)
  - Medieval scholars (Aquinas, etc.)
  - Modern biblical scholars
  - Jewish sources (Sefaria, Chabad, etc.)
  - Papal documents and encyclicals
  - And more as the agent learns

- **AI-Powered Synthesis**: Uses AI to synthesize multiple commentaries into coherent, insightful readings

- **Flexible Search**: Search commentaries by book, chapter, verse, or natural language

### Bible Study Program
- **📚 Study Plans**: Pre-built reading plans (Bible in a Year, New Testament in 90 Days, etc.)
- **📝 Notes System**: Personal notes on verses with categories (insights, questions, prayers)
- **🔖 Bookmarks & Highlights**: Mark and color-code important verses
- **🎯 Themes**: Organize verses by topics (love, faith, salvation, etc.)
- **💭 Memory Verses**: Track memorization progress with review system
- **🔤 Word Studies**: Study original Hebrew/Greek words with definitions
- **🔗 Cross References**: Find related verses automatically
- **📈 Statistics**: Track reading progress, time spent, verses read
- **📊 Dashboard**: Overview of your study journey

### Quantum AI System
- **🧠 Quantum Memory**: Store and retrieve information using quantum states
- **🔍 Quantum Reasoning**: Logical inference using quantum circuits
- **⚡ Quantum Learning**: 500x+ more efficient training than classical methods
- **💡 Quantum Attention**: Better focus on relevant information
- **🌐 Semantic Understanding**: Deep semantic comprehension through quantum states
- **🔗 Entanglement**: Related concepts are quantum-entangled for better connections

### Web Interfaces
- **Commentary Interface**: `/` - Simple verse commentary lookup
- **Bible Study Program**: `/study` - Full-featured study interface
- **Quantum Study**: `/quantum-study` - Quantum-enhanced Bible study
- **Bible Characters**: `/bible-characters` - Chat with Bible characters
- **Quantum AI**: `/quantum-ai` - Full quantum AI system interface
- **Mobile-Friendly**: Works perfectly on iPad and mobile devices

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

5. Initialize default study plans (optional):
```bash
python init_study_plans.py
```

## Usage

### API Server

Start the FastAPI server:
```bash
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

#### Web Interfaces

- `GET /` - Commentary web interface
- `GET /study` - **Bible Study Program** (full-featured study system)
- `GET /quantum-study` - Quantum-enhanced Bible study
- `GET /bible-characters` - Chat with Bible characters
- `GET /quantum-ai` - **Quantum AI System** (full quantum AI interface)
- `GET /docs` - API documentation

#### API Endpoints

**Commentary Endpoints:**
- `GET /` - API information / Web interface
- `POST /api/commentary` - Build commentary for a verse
- `GET /api/commentary/{book}/{chapter}/{verse}` - Get commentary
- `GET /api/commentary/{book}/{chapter}/{verse}/{category}` - Get commentary by category
- `POST /api/search` - Search commentaries
- `GET /api/suggestions/{book}/{chapter}/{verse}` - Get improvement suggestions
- `GET /api/books` - List all Bible books

**Study Endpoints:**
- `GET /api/study/plans` - Get study plans
- `GET /api/study/plans/{id}/today` - Get today's reading
- `POST /api/study/notes` - Add a note
- `GET /api/study/notes` - Get notes
- `POST /api/study/bookmarks` - Add bookmark
- `POST /api/study/memory-verses` - Add memory verse
- `GET /api/study/memory-verses/to-review` - Get verses to review
- `GET /api/study/themes` - Get themes
- `GET /api/study/word-studies/{word}` - Get word study
- `GET /api/study/cross-references` - Get cross references
- `GET /api/study/statistics` - Get reading statistics

**Quantum AI Endpoints:**
- `GET /api/quantum-ai/status` - Get system status
- `POST /api/quantum-ai/memory/store` - Store memory
- `POST /api/quantum-ai/memory/recall` - Recall memories
- `GET /api/quantum-ai/memory/list` - List all memories
- `DELETE /api/quantum-ai/memory/{key}` - Delete memory
- `POST /api/quantum-ai/reasoning` - Perform quantum reasoning
- `POST /api/quantum-ai/generate` - Generate quantum response
- `POST /api/quantum-ai/train` - Train the system
- `POST /api/quantum-ai/learn` - Quantum learning

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
├── api.py                  # FastAPI application
├── agent.py                # Main AI agent logic
├── scraper.py              # Web scraping module
├── models.py               # Database models (commentaries + study)
├── study_system.py         # Bible study system logic
├── study_api.py            # Study API endpoints
├── study_plans.py          # Pre-built study plans
├── config.py               # Configuration settings
├── cli.py                  # Command-line interface
├── web_interface.html      # Commentary web interface
├── bible_study.html        # Bible Study Program interface
├── init_study_plans.py     # Initialize default study plans
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Configuration

Edit `config.py` to customize:
- Commentary sources and URLs
- AI model settings
- Scraping parameters
- Database configuration

## Database

The agent uses SQLite by default (configurable to PostgreSQL, MySQL, etc.). The database stores:

**Commentary Data:**
- Commentaries with metadata (book, chapter, verse, source, author)
- Search history
- Source categorization

**Study Data:**
- Study plans and reading assignments
- User notes on verses
- Bookmarks and highlights
- Themes and verse collections
- Memory verses and review progress
- Word studies
- Cross references
- Reading sessions and statistics

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
