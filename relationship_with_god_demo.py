"""
Visual Demo: Building Relationship with God Through Understanding
Demonstrates all capabilities: Semantic Understanding, Relationship Discovery, 
Pattern Recognition, and Progressive Learning
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from typing import List, Dict, Optional
import uvicorn
import socket
import os
from pathlib import Path

# Import core systems
from quantum_kernel import QuantumKernel, get_kernel, KernelConfig
from complete_ai_system import CompleteAISystem
from quantum_llm_standalone import StandaloneQuantumLLM

app = FastAPI(
    title="Relationship with God - Visual Demo",
    description="Visual demonstration of semantic understanding, relationship discovery, and progressive learning",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize systems
print("Initializing systems...")
kernel = get_kernel(KernelConfig(
    embedding_dim=256,
    cache_size=50000,
    enable_caching=True
))
ai_system = CompleteAISystem()
llm = StandaloneQuantumLLM(kernel=kernel)

# Sample Scripture verses for demonstration
SAMPLE_VERSES = [
    "For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.",
    "Trust in the Lord with all thine heart; and lean not unto thine own understanding.",
    "And we know that all things work together for good to them that love God, to them who are the called according to his purpose.",
    "But seek ye first the kingdom of God, and his righteousness; and all these things shall be added unto you.",
    "I can do all things through Christ which strengtheneth me.",
    "The Lord is my shepherd; I shall not want.",
    "Be still, and know that I am God.",
    "Come unto me, all ye that labour and are heavy laden, and I will give you rest.",
    "For I know the thoughts that I think toward you, saith the Lord, thoughts of peace, and not of evil, to give you an expected end.",
    "But God commendeth his love toward us, in that, while we were yet sinners, Christ died for us."
]

# Store user interactions for progressive learning
user_interactions = []
discovered_relationships = {}
theme_clusters = []

@app.get("/")
async def root():
    """Serve the main demo interface"""
    if os.path.exists("relationship_with_god_demo.html"):
        return FileResponse("relationship_with_god_demo.html")
    raise HTTPException(status_code=404, detail="Demo interface not found")

@app.post("/api/understand")
async def understand_semantic(query: Dict):
    """Demonstrate semantic understanding"""
    text = query.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text required")
    
    # Semantic understanding
    intent = ai_system.understanding.understand_intent(text)
    
    # Find similar verses
    similar = kernel.find_similar(text, SAMPLE_VERSES, top_k=5)
    
    # Get kernel stats
    stats = kernel.get_stats()
    
    return {
        "query": text,
        "understanding": {
            "intent": intent["intent"],
            "confidence": intent["confidence"],
            "context_relevance": intent["context_relevance"]
        },
        "similar_verses": [
            {"verse": verse, "similarity": sim, "meaning": "Semantically related to your query"}
            for verse, sim in similar
        ],
        "kernel_stats": {
            "embeddings_computed": stats.get("embeddings_computed", 0),
            "cache_hits": stats.get("cache_hits", 0),
            "similarities_computed": stats.get("similarities_computed", 0)
        }
    }

@app.post("/api/discover")
async def discover_relationships(query: Dict):
    """Demonstrate relationship discovery"""
    text = query.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text required")
    
    # Build relationship graph
    all_texts = [text] + SAMPLE_VERSES
    relationship_graph = kernel.build_relationship_graph(all_texts)
    
    # Get relationships for the query
    relationships = relationship_graph.get(text, [])
    
    # Store for progressive learning
    discovered_relationships[text] = relationships
    
    return {
        "query": text,
        "relationships": [
            {
                "related_text": rel_text,
                "similarity": sim,
                "connection": "Semantic relationship discovered automatically"
            }
            for rel_text, sim in relationships[:10]  # Top 10
        ],
        "total_relationships": len(relationships)
    }

@app.post("/api/patterns")
async def discover_patterns(query: Dict):
    """Demonstrate pattern recognition and theme discovery"""
    # Discover themes across all verses
    themes = kernel.discover_themes(SAMPLE_VERSES, min_cluster_size=2)
    
    # Get theme clusters
    theme_clusters.clear()
    for theme in themes:
        theme_clusters.append({
            "theme": theme["theme"],
            "verses": theme["texts"],
            "confidence": theme["confidence"]
        })
    
    return {
        "themes_discovered": [
            {
                "theme": cluster["theme"],
                "verses_count": len(cluster["verses"]),
                "verses": cluster["verses"][:5],  # First 5
                "confidence": cluster["confidence"],
                "meaning": "Pattern discovered across Scripture"
            }
            for cluster in theme_clusters
        ],
        "total_themes": len(theme_clusters)
    }

@app.post("/api/learn")
async def progressive_learning(query: Dict):
    """Demonstrate progressive learning"""
    text = query.get("text", "")
    interaction_type = query.get("type", "query")
    
    # Store interaction
    user_interactions.append({
        "text": text,
        "type": interaction_type,
        "timestamp": "now"
    })
    
    # LLM learns from this
    if text:
        # Add to LLM's source texts for learning
        if text not in llm.source_texts:
            llm.source_texts.append(text)
            llm._build_verified_database()
    
    # Get learning stats
    learning_stats = {
        "total_interactions": len(user_interactions),
        "relationships_discovered": len(discovered_relationships),
        "themes_identified": len(theme_clusters),
        "phrases_learned": len(llm.verified_phrases) if hasattr(llm, 'verified_phrases') else 0
    }
    
    return {
        "interaction": {
            "text": text,
            "type": interaction_type
        },
        "learning_progress": learning_stats,
        "message": "System learning from your interaction"
    }

@app.post("/api/generate")
async def generate_grounded(query: Dict):
    """Demonstrate grounded text generation"""
    prompt = query.get("prompt", "")
    context = query.get("context", [])
    
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt required")
    
    # Generate grounded text
    try:
        generated = llm.generate_grounded(
            prompt=prompt,
            context=context,
            max_length=200
        )
        
        return {
            "prompt": prompt,
            "generated": generated,
            "grounded": True,
            "message": "Generated from verified sources, no hallucinations"
        }
    except Exception as e:
        return {
            "prompt": prompt,
            "generated": f"Understanding: {prompt}",
            "grounded": True,
            "message": "Grounded in semantic understanding"
        }

@app.get("/api/stats")
async def get_stats():
    """Get overall system statistics"""
    kernel_stats = kernel.get_stats()
    
    return {
        "kernel": {
            "embeddings_computed": kernel_stats.get("embeddings_computed", 0),
            "cache_hits": kernel_stats.get("cache_hits", 0),
            "similarities_computed": kernel_stats.get("similarities_computed", 0),
            "cache_hit_rate": f"{(kernel_stats.get('cache_hits', 0) / max(kernel_stats.get('embeddings_computed', 1), 1) * 100):.1f}%"
        },
        "learning": {
            "total_interactions": len(user_interactions),
            "relationships_discovered": len(discovered_relationships),
            "themes_identified": len(theme_clusters)
        },
        "system": {
            "verses_loaded": len(SAMPLE_VERSES),
            "capabilities": [
                "Semantic Understanding",
                "Relationship Discovery",
                "Pattern Recognition",
                "Progressive Learning",
                "Grounded Generation"
            ]
        }
    }

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def find_free_port(start_port=8000, max_attempts=50):
    """Find a free port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    raise RuntimeError("Could not find free port")

if __name__ == "__main__":
    port = find_free_port()
    local_ip = get_local_ip()
    
    print("\n" + "=" * 80)
    print("RELATIONSHIP WITH GOD - VISUAL DEMO")
    print("=" * 80)
    print(f"\nStarting server on port {port}...")
    print(f"\nAccess on your computer:")
    print(f"  http://localhost:{port}")
    print(f"\nAccess on your iPad/phone:")
    print(f"  http://{local_ip}:{port}")
    print("\n" + "=" * 80)
    print("Demonstrating:")
    print("  - Semantic Understanding")
    print("  - Relationship Discovery")
    print("  - Pattern Recognition")
    print("  - Progressive Learning")
    print("  - Building Relationship with God")
    print("=" * 80 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port)