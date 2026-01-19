# Phi-3 LLM Setup Guide

## What is Phi-3?

**Phi-3** is Microsoft's efficient, small language model that:
- ✅ Runs **locally** (no API costs)
- ✅ **Fast** inference (3.8B parameters for Mini)
- ✅ **High quality** for its size
- ✅ **Free** to use
- ✅ **Private** (data stays local)

## Installation Options

### Option 1: Ollama (Recommended - Easiest)

**Ollama** is the easiest way to run Phi-3 locally.

#### Step 1: Install Ollama
1. Download from: https://ollama.com
2. Install and run Ollama
3. It will start a local server automatically

#### Step 2: Pull Phi-3 Model
```bash
ollama pull phi3:mini
```

This downloads Phi-3 Mini (~2.3GB). Options:
- `phi3:mini` - 3.8B parameters, 4K context (recommended)
- `phi3:medium` - 14B parameters, 4K context (better quality, needs more RAM)
- `phi3-mini-128k-instruct` - 3.8B, 128K context (for long contexts)

#### Step 3: Verify Installation
```bash
ollama run phi3:mini
```

Type a test prompt. If it works, you're ready!

#### Step 4: Use in Bible App
The app will automatically detect and use Phi-3 if Ollama is running!

**That's it!** No API keys needed.

---

### Option 2: Hugging Face (Cloud API)

If you prefer cloud-based inference:

#### Step 1: Get Hugging Face API Key
1. Go to https://huggingface.co
2. Create account
3. Get API key from: https://huggingface.co/settings/tokens

#### Step 2: Set Environment Variable
```bash
# Windows PowerShell
$env:HUGGINGFACE_API_KEY="your-api-key-here"

# Windows CMD
set HUGGINGFACE_API_KEY=your-api-key-here

# Linux/Mac
export HUGGINGFACE_API_KEY=your-api-key-here
```

#### Step 3: Or use .env file
Create `.env` file:
```
HUGGINGFACE_API_KEY=your-api-key-here
```

The app will automatically use Phi-3 via Hugging Face!

---

### Option 3: Direct Integration (Advanced)

For direct Python integration without Ollama:

#### Install Dependencies
```bash
pip install transformers torch accelerate
```

#### Use in Code
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/Phi-3-mini-4k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Use model for inference
```

**Note:** This requires significant RAM/VRAM and downloads the full model (~7GB).

---

## Phi-3 Model Variants

### Phi-3 Mini (Recommended)
- **Size:** 3.8B parameters
- **Context:** 4K or 128K tokens
- **RAM:** ~8GB minimum
- **Speed:** Fast
- **Quality:** Excellent for its size

### Phi-3 Medium
- **Size:** 14B parameters
- **Context:** 4K tokens
- **RAM:** ~16GB minimum
- **Speed:** Slower
- **Quality:** Better than Mini

### Which to Choose?
- **Most users:** Phi-3 Mini (4K) - Best balance
- **Long documents:** Phi-3 Mini (128K) - For long contexts
- **Better quality:** Phi-3 Medium - If you have RAM

---

## Usage in Bible App

### Automatic Detection
The app automatically tries Phi-3 in this order:
1. **Ollama** (if installed and running)
2. **Hugging Face** (if API key provided)
3. Falls back to other LLMs if Phi-3 unavailable

### Priority Order
The app uses this priority:
1. OpenAI GPT-4 (if API key)
2. OpenAI GPT-3.5 (if API key)
3. Anthropic Claude (if API key)
4. **Phi-3 via Ollama** (local, free) ⭐
5. Google Gemini (if API key)
6. Hugging Face Phi-3 (if API key)
7. Other free LLMs
8. Quantum-only (fallback)

### Check Status
Visit: `http://localhost:8000/api/bible-llm/status`

You'll see:
```json
{
  "llm_available": true,
  "provider": "ollama",
  "model": "phi3:mini",
  "quantum_available": true
}
```

---

## Performance Tips

### For Best Speed:
1. Use **Phi-3 Mini** (faster than Medium)
2. Use **4K context** (faster than 128K)
3. Use **GPU** if available (much faster)
4. Use **quantized models** (smaller, faster)

### For Best Quality:
1. Use **Phi-3 Medium** (better quality)
2. Use **128K context** (for long documents)
3. Combine with **quantum learning** (improves over time)

### Hardware Requirements:
- **CPU only:** Works, but slower (30-60s per response)
- **GPU (8GB+):** Much faster (5-10s per response)
- **GPU (16GB+):** Can run Medium model

---

## Troubleshooting

### "Ollama not available"
- Make sure Ollama is installed and running
- Check: `ollama list` (should show phi3:mini)
- Restart Ollama if needed

### "Model not found"
- Pull the model: `ollama pull phi3:mini`
- Wait for download to complete

### "Out of memory"
- Use Phi-3 Mini instead of Medium
- Close other applications
- Use quantized version if available

### "Slow responses"
- Normal for CPU-only (30-60s)
- Much faster with GPU
- Consider using cloud API (Hugging Face) for speed

---

## Benefits of Phi-3

✅ **Free** - No API costs
✅ **Private** - Data stays local
✅ **Fast** - Efficient inference
✅ **Quality** - Good for its size
✅ **Local** - Works offline
✅ **Customizable** - Can fine-tune

---

## Next Steps

1. **Install Ollama** (easiest option)
2. **Pull Phi-3:** `ollama pull phi3:mini`
3. **Start Bible App** - It will auto-detect Phi-3!
4. **Enjoy** free, local, high-quality LLM!

---

## Resources

- **Ollama:** https://ollama.com
- **Phi-3 Models:** https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
- **Microsoft Phi-3:** https://www.microsoft.com/en-us/research/blog/phi-3-the-recap/
