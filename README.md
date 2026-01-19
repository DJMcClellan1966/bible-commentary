# Quantum AI Framework

A complete, general-purpose AI framework built on quantum-inspired principles. This framework provides powerful AI capabilities that can be used for any application domain.

## 🎯 What This Framework Provides

### Core Components

1. **Quantum Kernel** (`quantum_kernel/`)
   - Universal processing layer for semantic understanding
   - Works with any text/data, not domain-specific
   - Provides: embeddings, similarity, relationship discovery, theme extraction

2. **Standalone Quantum LLM** (`quantum_llm_standalone.py`)
   - Complete language model with grounded generation
   - Progressive learning system
   - Bias detection and prevention

3. **Complete AI System** (`complete_ai_system/`)
   - Full-featured AI system with 6 integrated components:
     - Semantic Understanding Engine
     - Knowledge Graph Builder
     - Intelligent Search
     - Reasoning Engine
     - Learning System
     - Conversational AI

4. **Grounded Generation** (`quantum_grounded_generation.py`)
   - Prevents hallucinations
   - Uses verified sources only

5. **Example Applications** (`example_applications.py`)
   - Research Platform
   - Knowledge Base
   - Content Platform

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Run the API Server

```bash
python app_launcher.py
```

Or use the batch file:
```bash
START_APP.bat
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

## 📚 Usage Examples

### Using the Quantum Kernel

```python
from quantum_kernel import get_kernel

kernel = get_kernel()
results = kernel.find_similar(query, items, top_k=10)
similarity = kernel.similarity(text1, text2)
themes = kernel.discover_themes(texts)
```

### Using the Complete AI System

```python
from complete_ai_system import CompleteAISystem

ai = CompleteAISystem()
result = ai.process({
    "query": "your query",
    "documents": ["doc1", "doc2"]
})
```

### Using the Standalone Quantum LLM

```python
from quantum_llm_standalone import StandaloneQuantumLLM

llm = StandaloneQuantumLLM(source_texts=["verified source 1", "verified source 2"])
result = llm.generate_grounded_text("your prompt", max_length=500)
```

## 🎨 What You Can Build

This framework can power:

- **Research Platforms** - Semantic paper search, citation discovery
- **Knowledge Management Systems** - Personal knowledge bases, document organization
- **Content Platforms** - Content recommendations, semantic search
- **Business Intelligence** - Document analysis, relationship discovery
- **Educational Platforms** - Learning path generation, concept explanation
- **Customer Support** - Intelligent search, question answering
- **Legal/Medical/Technical** - Document analysis, semantic search
- **Creative Applications** - Writing assistance, idea generation

See `CORE_REUSABLE_COMPONENTS.md` for a complete list of capabilities.

## 📖 Documentation

- **Core Components**: See `CORE_REUSABLE_COMPONENTS.md`
- **Quantum Kernel**: See `quantum_kernel/README.md`
- **Complete AI System**: See `complete_ai_system/README.md`
- **Quantum LLM**: See `QUANTUM_LLM_README.md`
- **What You Can Create**: See `WHAT_YOU_CAN_CREATE.md`

## 🔧 Configuration

Edit `config.py` to configure:
- API keys (OpenAI, Anthropic, Google, etc.)
- Database settings
- AI system parameters
- Quantum kernel settings

## 🏗️ Architecture

```
quantum-ai-framework/
├── quantum_kernel/          # Universal processing layer
├── complete_ai_system/      # Full AI system
├── quantum_llm_standalone.py # Standalone LLM
├── quantum_grounded_generation.py
├── quantum_text_generation.py
├── example_applications.py
├── api.py                   # FastAPI application
└── config.py               # Configuration
```

## 📝 License

This framework is provided as-is for use in any application.

## 🤝 Contributing

This is a general-purpose framework. Adapt it to your needs!
