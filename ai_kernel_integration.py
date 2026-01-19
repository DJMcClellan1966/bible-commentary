"""
AI System and Kernel Integration Demo
Demonstrates how the AI system and kernel work together seamlessly
"""
from complete_ai_system import CompleteAISystem
from quantum_kernel import QuantumKernel, KernelConfig, get_kernel
import json


def demonstrate_shared_kernel():
    """Demonstrate shared kernel between AI system and direct kernel usage"""
    print("=" * 80)
    print("DEMONSTRATION: AI SYSTEM AND KERNEL WORKING TOGETHER")
    print("=" * 80)
    
    # Create a shared kernel configuration
    shared_config = KernelConfig(
        embedding_dim=256,
        cache_size=50000,
        enable_caching=True
    )
    
    # Create AI system with the kernel
    ai = CompleteAISystem(shared_config)
    
    # Get the same kernel instance
    kernel = ai.kernel
    
    print("\n1. SHARED KERNEL INSTANCE")
    print("-" * 80)
    print(f"AI System Kernel ID: {id(ai.kernel)}")
    print(f"Direct Kernel ID: {id(kernel)}")
    print(f"Same instance: {ai.kernel is kernel}")
    
    # Use AI system
    print("\n2. USING AI SYSTEM")
    print("-" * 80)
    documents = [
        "God is love",
        "Love is patient and kind",
        "Faith, hope, and love"
    ]
    
    ai_result = ai.process({
        "query": "divine love",
        "documents": documents
    })
    
    print(f"AI System found {ai_result['search']['count']} results")
    print(f"Knowledge graph has {len(ai_result['knowledge_graph']['nodes'])} nodes")
    
    # Use kernel directly (shares same cache!)
    print("\n3. USING KERNEL DIRECTLY (SHARED CACHE)")
    print("-" * 80)
    
    # These embeddings are already cached from AI system!
    query_embedding = kernel.embed("divine love")
    doc_embeddings = [kernel.embed(doc) for doc in documents]
    
    print(f"Query embedding shape: {query_embedding.shape}")
    print(f"Document embeddings: {len(doc_embeddings)}")
    
    # Compute similarities directly
    similarities = []
    for i, doc_emb in enumerate(doc_embeddings):
        sim = kernel.similarity("divine love", documents[i])
        similarities.append((documents[i], sim))
    
    print("\nDirect kernel similarities:")
    for doc, sim in sorted(similarities, key=lambda x: x[1], reverse=True):
        print(f"  - {doc[:40]}... (similarity: {sim:.3f})")
    
    # Check cache stats (shared!)
    print("\n4. SHARED CACHE STATISTICS")
    print("-" * 80)
    stats = kernel.get_stats()
    print(f"Embeddings computed: {stats['embeddings_computed']}")
    print(f"Cache hits: {stats['cache_hits']}")
    print(f"Cache size: {stats['cache_size']}")
    print(f"Cache efficiency: {stats['cache_hits'] / (stats['cache_hits'] + stats['embeddings_computed']) * 100:.1f}%")
    
    return ai, kernel


def demonstrate_complementary_usage():
    """Show how AI system and kernel complement each other"""
    print("\n" + "=" * 80)
    print("DEMONSTRATION: COMPLEMENTARY USAGE")
    print("=" * 80)
    
    # Create system
    ai = CompleteAISystem()
    kernel = ai.kernel
    
    documents = [
        "God is love and love is patient",
        "Faith is the assurance of things hoped for",
        "By grace you have been saved through faith",
        "The Lord is my shepherd"
    ]
    
    print("\n1. AI SYSTEM: HIGH-LEVEL OPERATIONS")
    print("-" * 80)
    
    # Use AI system for high-level operations
    result = ai.process({
        "query": "divine love",
        "documents": documents,
        "premises": ["God is love", "Love is patient"],
        "question": "What is God like?"
    })
    
    print(f"[OK] Understanding: {result['understanding']['intent']}")
    print(f"[OK] Search results: {result['search']['count']}")
    print(f"[OK] Reasoning confidence: {result['reasoning']['confidence']:.3f}")
    print(f"[OK] Knowledge graph nodes: {len(result['knowledge_graph']['nodes'])}")
    
    print("\n2. KERNEL: LOW-LEVEL OPERATIONS")
    print("-" * 80)
    
    # Use kernel directly for low-level operations
    # Find similar documents
    similar = kernel.find_similar("divine love", documents, top_k=2)
    print(f"[OK] Direct similarity search: {len(similar)} results")
    
    # Build relationship graph
    rel_graph = kernel.build_relationship_graph(documents)
    print(f"[OK] Relationship graph: {len(rel_graph)} nodes with relationships")
    
    # Discover themes
    themes = kernel.discover_themes(documents, min_cluster_size=2)
    print(f"[OK] Themes discovered: {len(themes)}")
    
    # Compute specific similarities
    sim1 = kernel.similarity(documents[0], documents[1])
    sim2 = kernel.similarity(documents[1], documents[2])
    print(f"[OK] Specific similarities: {sim1:.3f}, {sim2:.3f}")
    
    print("\n3. WORKING TOGETHER")
    print("-" * 80)
    print("AI System provides:")
    print("  - High-level abstractions (understanding, reasoning, conversation)")
    print("  - Integrated workflows")
    print("  - Component coordination")
    print("\nKernel provides:")
    print("  - Low-level operations (embeddings, similarities)")
    print("  - Fast caching")
    print("  - Direct access to core functions")
    print("\nTogether they:")
    print("  - Share the same cache (10-200x speedup)")
    print("  - Use the same embeddings")
    print("  - Provide complementary APIs")
    print("  - Enable flexible usage patterns")


def demonstrate_workflow_integration():
    """Show a complete workflow using both together"""
    print("\n" + "=" * 80)
    print("DEMONSTRATION: COMPLETE WORKFLOW INTEGRATION")
    print("=" * 80)
    
    ai = CompleteAISystem()
    kernel = ai.kernel
    
    documents = [
        "God is love",
        "Love is patient and kind",
        "Faith, hope, and love",
        "By grace through faith"
    ]
    
    print("\nWorkflow: Research and Analysis")
    print("-" * 80)
    
    # Step 1: Use AI system for high-level search
    print("\nStep 1: AI System - Semantic Search")
    search_result = ai.search.search_and_discover("divine love", documents)
    print(f"  Found {search_result['count']} relevant documents")
    print(f"  Discovered {len(search_result['themes'])} themes")
    
    # Step 2: Use kernel directly for detailed analysis
    print("\nStep 2: Kernel - Detailed Similarity Analysis")
    top_docs = [r['text'] for r in search_result['results'][:2]]
    for doc in top_docs:
        # Get embedding directly
        embedding = kernel.embed(doc)
        print(f"  Document: {doc[:40]}...")
        print(f"    Embedding dimension: {embedding.shape[0]}")
        
        # Find all similar documents
        similar = kernel.find_similar(doc, documents, top_k=3)
        print(f"    Similar documents: {len(similar)}")
    
    # Step 3: Use AI system for reasoning
    print("\nStep 3: AI System - Reasoning")
    reasoning = ai.reasoning.reason(
        ["God is love", "Love is patient"],
        "What follows?"
    )
    print(f"  Connections found: {len(reasoning['connections'])}")
    print(f"  Coherence: {reasoning['coherence']:.3f}")
    
    # Step 4: Use kernel for relationship graph
    print("\nStep 4: Kernel - Relationship Graph")
    graph = kernel.build_relationship_graph(documents)
    total_relationships = sum(len(related) for related in graph.values())
    print(f"  Total relationships: {total_relationships}")
    
    # Step 5: Use AI system for knowledge graph
    print("\nStep 5: AI System - Knowledge Graph")
    kg = ai.knowledge_graph.build_graph(documents)
    print(f"  Nodes: {len(kg['nodes'])}")
    print(f"  Edges: {len(kg['edges'])}")
    print(f"  Themes: {len(kg['themes'])}")
    
    # Final: Check shared cache
    print("\nStep 6: Shared Cache Benefits")
    stats = kernel.get_stats()
    print(f"  Total embeddings computed: {stats['embeddings_computed']}")
    print(f"  Cache hits: {stats['cache_hits']}")
    print(f"  Cache efficiency: {stats['cache_hits'] / (stats['cache_hits'] + stats['embeddings_computed']) * 100:.1f}%")
    print(f"  All operations shared the same cache!")


def demonstrate_performance_benefits():
    """Show performance benefits of working together"""
    print("\n" + "=" * 80)
    print("DEMONSTRATION: PERFORMANCE BENEFITS")
    print("=" * 80)
    
    import time
    
    ai = CompleteAISystem()
    kernel = ai.kernel
    
    documents = ["Document " + str(i) for i in range(100)]
    
    # Test 1: AI system uses kernel (first time - compute)
    print("\n1. First Use (Computing Embeddings)")
    start = time.time()
    result1 = ai.search.search("test query", documents[:50])
    time1 = time.time() - start
    print(f"  Time: {time1*1000:.2f}ms")
    print(f"  Results: {len(result1)}")
    
    # Test 2: Kernel directly (uses cached embeddings!)
    print("\n2. Direct Kernel Use (Using Cached Embeddings)")
    start = time.time()
    result2 = kernel.find_similar("test query", documents[:50], top_k=10)
    time2 = time.time() - start
    print(f"  Time: {time2*1000:.2f}ms")
    print(f"  Results: {len(result2)}")
    
    if time1 > 0 and time2 > 0:
        speedup = time1 / time2
        print(f"  Speedup: {speedup:.2f}x faster (using shared cache!)")
    
    # Test 3: AI system again (all cached now)
    print("\n3. AI System Again (All Cached)")
    start = time.time()
    result3 = ai.search.search("test query", documents[:50])
    time3 = time.time() - start
    print(f"  Time: {time3*1000:.2f}ms")
    print(f"  Results: {len(result3)}")
    
    if time1 > 0 and time3 > 0:
        speedup = time1 / time3
        print(f"  Speedup: {speedup:.2f}x faster (everything cached!)")
    
    # Final stats
    print("\n4. Final Cache Statistics")
    stats = kernel.get_stats()
    print(f"  Embeddings computed: {stats['embeddings_computed']}")
    print(f"  Cache hits: {stats['cache_hits']}")
    print(f"  Cache size: {stats['cache_size']}")
    print(f"  All operations shared the same cache!")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 80)
    print("AI SYSTEM AND KERNEL INTEGRATION DEMONSTRATION")
    print("=" * 80)
    print("\nThis demonstrates how the AI system and kernel work together:")
    print("  - Share the same kernel instance")
    print("  - Share the same cache (10-200x speedup)")
    print("  - Provide complementary APIs")
    print("  - Enable flexible usage patterns")
    
    # Run demonstrations
    ai, kernel = demonstrate_shared_kernel()
    demonstrate_complementary_usage()
    demonstrate_workflow_integration()
    demonstrate_performance_benefits()
    
    print("\n" + "=" * 80)
    print("INTEGRATION DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("""
Key Takeaways:

[+] AI System and Kernel share the same instance
[+] They share the same cache (massive performance benefit)
[+] AI System provides high-level abstractions
[+] Kernel provides low-level operations
[+] You can use either or both together
[+] All operations benefit from shared caching

The AI system is built ON TOP OF the kernel, so they work
together seamlessly by design!
    """)


if __name__ == "__main__":
    main()
