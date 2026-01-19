"""
Configuration settings for Quantum AI Framework
"""
import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./quantum_ai.db")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")

# Phi-3 Configuration (for local models)
PHI3_MODEL = os.getenv("PHI3_MODEL", "phi3:mini")  # Options: phi3:mini, phi3:medium, phi3-mini-4k-instruct
PHI3_USE_LOCAL = os.getenv("PHI3_USE_LOCAL", "true").lower() == "true"  # Use local Ollama if available

# Web Scraping (for general data collection)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3

# AI System Settings
AGENT_TEMPERATURE = 0.7
MAX_TOKENS = 2000
ENABLE_WEB_SEARCH = True
ENABLE_LEARNING = True

# Quantum Kernel Settings
KERNEL_EMBEDDING_DIM = 256
KERNEL_CACHE_SIZE = 50000
KERNEL_ENABLE_CACHING = True
