# Best LLM Setup for Bible App

## Overview

The Bible app now has **best LLM integration** that automatically selects the best available LLM and enables quantum learning from LLM outputs.

---

## Supported LLMs (Priority Order)

### 1. **OpenAI GPT-4** (Best Quality) ⭐
- **Best for:** Highest quality Bible study responses
- **Setup:** Set `OPENAI_API_KEY` environment variable
- **Model:** `gpt-4`
- **Cost:** Higher, but best quality

### 2. **OpenAI GPT-3.5-turbo** (Fast & Cost-Effective)
- **Best for:** Faster responses, lower cost
- **Setup:** Set `OPENAI_API_KEY` environment variable
- **Model:** `gpt-3.5-turbo`
- **Cost:** Lower, still good quality

### 3. **Anthropic Claude** (Alternative)
- **Best for:** Alternative to OpenAI
- **Setup:** Set `ANTHROPIC_API_KEY` environment variable
- **Model:** `claude-3-opus`
- **Cost:** Similar to GPT-4

### 4. **Phi-3 (Microsoft)** (Local, Free) ⭐ NEW!
- **Best for:** Local, private, free LLM
- **Setup:** Install Ollama and run `ollama pull phi3:mini`
- **Model:** `phi3:mini` or `phi3:medium`
- **Cost:** FREE (runs locally)
- **See:** `PHI3_SETUP.md` for detailed instructions

---

## Setup Instructions

### Option 1: OpenAI GPT-4 (Recommended for Best Quality)

1. **Get API Key:**
   - Go to https://platform.openai.com/
   - Create account and get API key

2. **Set Environment Variable:**
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # Windows CMD
   set OPENAI_API_KEY=your-api-key-here
   
   # Linux/Mac
   export OPENAI_API_KEY=your-api-key-here
   ```

3. **Or use .env file:**
   Create `.env` file in project root:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

4. **Verify:**
   ```python
   from bible_llm_integration import create_bible_llm_integration
   from bible_ai_system import create_bible_ai_system
   from models import get_db
   
   db = next(get_db())
   bible_ai = create_bible_ai_system(db)
   llm = create_bible_llm_integration(bible_ai)
   
   status = llm.get_status()
   print(f"LLM Available: {status['llm_available']}")
   print(f"Provider: {status['provider']}")
   print(f"Model: {status['model']}")
   ```

### Option 2: OpenAI GPT-3.5-turbo (Faster/Cheaper)

Same setup as GPT-4, but the system will automatically use GPT-3.5 if GPT-4 is unavailable or you prefer it.

### Option 3: Anthropic Claude

1. **Get API Key:**
   - Go to https://console.anthropic.com/
   - Create account and get API key

2. **Set Environment Variable:**
   ```bash
   export ANTHROPIC_API_KEY=your-api-key-here
   ```

---

## How It Works

### Automatic LLM Selection

The system automatically selects the best available LLM:

```
1. Try GPT-4 (best quality)
   ↓ (if unavailable)
2. Try GPT-3.5-turbo (fast, cost-effective)
   ↓ (if unavailable)
3. Try Claude (alternative)
   ↓ (if unavailable)
4. Use Quantum-only mode (works without LLM)
```

### Quantum Learning

**Automatic Learning:**
- Every LLM output is automatically learned by quantum
- Quantum vocabulary grows with LLM examples
- Quantum patterns improve over time

**Manual Learning:**
- You can also manually trigger learning
- Useful for batch learning from LLM outputs

---

## Usage Examples

### Python Code

```python
from bible_ai_system import create_bible_ai_system
from bible_llm_integration import create_bible_llm_integration
from models import get_db

# Get database session
db = next(get_db())

# Create systems
bible_ai = create_bible_ai_system(db)
llm_integration = create_bible_llm_integration(bible_ai)

# Check status
status = llm_integration.get_status()
print(f"LLM Available: {status['llm_available']}")
print(f"Provider: {status['provider']}")  # "openai", "anthropic", or None
print(f"Model: {status['model']}")  # "gpt-4", "gpt-3.5-turbo", "claude-3-opus", or None

# Generate with LLM (quantum learns automatically)
result = llm_integration.generate_with_llm("God is", context="Bible study")
print(result['generated'])
print(f"Learned: {result['learned']}")

# Hybrid generation (LLM + Quantum)
result = llm_integration.generate_hybrid("Love is", use_llm=True, use_quantum=True)
print(f"LLM Output: {result['llm_output']}")
print(f"Quantum Output: {result['quantum_output']}")

# Translate with LLM (quantum learns)
result = llm_integration.translate_with_llm("God is love", "en", "es")
print(f"Translation: {result['translation']}")
print(f"Quantum Learned: {result['quantum_learned']}")
```

### API Calls

```bash
# Check status
curl http://localhost:8000/api/bible-llm/status

# Generate with LLM (quantum learns automatically)
curl -X POST http://localhost:8000/api/bible-llm/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "God is",
    "context": "Bible study",
    "use_llm": true,
    "use_quantum": true
  }'

# Translate with LLM (quantum learns)
curl -X POST http://localhost:8000/api/bible-llm/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "God is love",
    "source_lang": "en",
    "target_lang": "es",
    "use_llm": true
  }'
```

---

## Features

### ✅ Automatic LLM Selection
- Tries best LLM first (GPT-4)
- Falls back to alternatives
- Works without LLM (quantum-only)

### ✅ Automatic Quantum Learning
- Every LLM output is learned
- Quantum vocabulary grows
- Patterns improve over time

### ✅ Hybrid Generation
- Use LLM for quality
- Use Quantum for speed
- Compare both outputs

### ✅ Smart Fallback
- If LLM unavailable → uses quantum
- If quantum unavailable → uses LLM
- Always has a working solution

---

## Benefits

### With LLM:
- ✅ **High Quality** - Best LLM (GPT-4) for Bible study
- ✅ **Quantum Learning** - Quantum improves from LLM
- ✅ **Hybrid Approach** - Best of both worlds

### Without LLM:
- ✅ **Still Works** - Quantum-only mode
- ✅ **Fast & Private** - No external dependencies
- ✅ **Free** - No API costs

---

## Cost Considerations

### GPT-4
- **Cost:** ~$0.03 per 1K tokens (input), ~$0.06 per 1K tokens (output)
- **Best for:** Critical quality needs

### GPT-3.5-turbo
- **Cost:** ~$0.0015 per 1K tokens (input), ~$0.002 per 1K tokens (output)
- **Best for:** Regular use, cost-effective

### Quantum
- **Cost:** Free (no API calls)
- **Best for:** Speed, privacy, offline use

---

## Recommendations

### For Bible App:

**Best Setup:**
1. **Set up GPT-4** for highest quality
2. **Let quantum learn** from GPT-4 outputs
3. **Use hybrid** for best results
4. **Fallback to quantum** when LLM unavailable

**Cost-Effective Setup:**
1. **Set up GPT-3.5-turbo** for lower cost
2. **Let quantum learn** from outputs
3. **Use quantum** for most requests
4. **Use LLM** only when quality critical

**Privacy-Focused Setup:**
1. **Don't set API key** (quantum-only)
2. **Use quantum** for everything
3. **Fast, private, free**

---

## Conclusion

The Bible app now has **best LLM integration**:

✅ **Automatic selection** of best available LLM
✅ **Quantum learning** from LLM outputs
✅ **Hybrid generation** for best results
✅ **Smart fallback** if LLM unavailable
✅ **Works without LLM** (quantum-only mode)

**Set up your API key and the system will automatically use the best LLM, with quantum learning from every output!**
