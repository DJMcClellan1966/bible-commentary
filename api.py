"""
FastAPI application for Quantum AI Framework
General-purpose AI system API
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional
import os

# Import quantum AI system
try:
    from quantum_ai_api import router as quantum_ai_router
    QUANTUM_AI_AVAILABLE = True
except ImportError:
    QUANTUM_AI_AVAILABLE = False
    quantum_ai_router = None

app = FastAPI(
    title="Quantum AI Framework API",
    description="General-purpose AI system built on quantum-inspired principles",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include quantum AI router if available
if QUANTUM_AI_AVAILABLE and quantum_ai_router:
    app.include_router(quantum_ai_router)

# Bible API availability check
try:
    from bible_api import BIBLE_APP_AVAILABLE
    BIBLE_API_AVAILABLE = BIBLE_APP_AVAILABLE
except ImportError:
    BIBLE_API_AVAILABLE = False

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Quantum AI Framework API",
        "version": "1.0.0",
        "description": "General-purpose AI system built on quantum-inspired principles",
        "endpoints": {
            "health": "/health",
            "api_docs": "/docs",
            "quantum_ai": "/quantum-ai" if QUANTUM_AI_AVAILABLE else "Not available",
            "bible_app": "Run 'python start_bible_app.py' for Bible app" if BIBLE_API_AVAILABLE else "Not available"
        }
    }

@app.get("/quantum-ai")
async def quantum_ai_interface():
    """Serve Quantum AI interface"""
    if os.path.exists("quantum_ai_interface.html"):
        return FileResponse("quantum_ai_interface.html")
    raise HTTPException(status_code=404, detail="Quantum AI interface not found")

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "quantum_ai_available": QUANTUM_AI_AVAILABLE
    }

@app.get("/api/info")
async def api_info():
    """API information"""
    return {
        "name": "Quantum AI Framework",
        "version": "1.0.0",
        "description": "General-purpose AI system built on quantum-inspired principles",
        "features": [
            "Quantum Kernel - Universal processing layer",
            "Standalone Quantum LLM - Language model with grounded generation",
            "Complete AI System - Full-featured AI framework",
            "Grounded Generation - Hallucination-free text generation",
            "Progressive Learning - Continuous improvement system"
        ],
        "components": {
            "quantum_kernel": "Available",
            "quantum_llm": "Available",
            "complete_ai_system": "Available",
            "quantum_ai": QUANTUM_AI_AVAILABLE
        }
    }
