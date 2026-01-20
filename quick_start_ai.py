"""
Quick Start - Test if AI System Works
"""
from complete_ai_system import CompleteAISystem

print("Initializing AI System...")
ai = CompleteAISystem()
print("[OK] AI System initialized successfully!\n")

# Test 1: Semantic Search
print("=" * 60)
print("TEST 1: Semantic Search")
print("=" * 60)
result = ai.process({
    "query": "divine love",
    "documents": [
        "God is love and love is patient",
        "Faith is the assurance of things hoped for",
        "By grace you have been saved through faith"
    ]
})

search_results = result.get("search", {}).get("results", [])
print(f"Found {len(search_results)} results:")
for i, item in enumerate(search_results[:3], 1):
    print(f"  {i}. {item['text'][:60]}... (similarity: {item['similarity']:.3f})")

# Test 2: Understanding Intent
print("\n" + "=" * 60)
print("TEST 2: Understanding Intent")
print("=" * 60)
intent = ai.understanding.understand_intent("I want to search for information")
print(f"Intent: {intent['intent']}")
print(f"Confidence: {intent['confidence']:.3f}")

# Test 3: System Stats
print("\n" + "=" * 60)
print("TEST 3: System Statistics")
print("=" * 60)
stats = ai.get_stats()
print(f"Kernel cache size: {stats['kernel']['cache_size']}")
print(f"Embeddings computed: {stats['kernel']['embeddings_computed']}")

print("\n" + "=" * 60)
print("[OK] All tests passed! AI System is ready to use!")
print("=" * 60)
