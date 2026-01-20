"""
App Template - Best Practice Architecture
Build your app on top of Kernel, AI System, and LLM
"""
from complete_ai_system import CompleteAISystem
from quantum_llm_standalone import StandaloneQuantumLLM
from quantum_kernel import KernelConfig, get_kernel
from typing import List, Dict, Optional


class MyApp:
    """
    Template Application
    Built on Quantum Kernel + AI System + LLM
    """
    
    def __init__(self, enable_llm: bool = False, source_texts: Optional[List[str]] = None):
        """
        Initialize app with AI components
        
        Args:
            enable_llm: Whether to enable LLM for text generation
            source_texts: Source texts for grounded LLM generation
        """
        # Step 1: Configure kernel
        config = KernelConfig(
            embedding_dim=256,      # Adjust based on your needs
            cache_size=50000,       # Larger for bigger apps
            enable_caching=True,    # Always True for performance
            similarity_threshold=0.7
        )
        
        # Step 2: Initialize AI System (creates kernel internally)
        self.ai = CompleteAISystem(config)
        
        # Step 3: Get shared kernel instance
        self.kernel = self.ai.kernel
        
        # Step 4: Optionally initialize LLM with shared kernel
        self.llm = None
        if enable_llm:
            self.llm = StandaloneQuantumLLM(
                kernel=self.kernel,  # Use shared kernel!
                source_texts=source_texts or []
            )
        
        # Step 5: Your app data
        self.items = []
    
    # ==================== Basic Operations ====================
    
    def add_item(self, item: str):
        """Add an item to your app"""
        self.items.append(item)
        
        # Optionally add to LLM sources for grounded generation
        if self.llm:
            self.llm.add_source_text(item)
    
    def get_items(self) -> List[str]:
        """Get all items"""
        return self.items
    
    # ==================== Search Operations ====================
    
    def search(self, query: str, top_k: int = 10) -> Dict:
        """
        Semantic search using AI system
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            Dictionary with search results
        """
        result = self.ai.search.search_and_discover(query, self.items)
        # Limit to top_k
        if 'results' in result:
            result['results'] = result['results'][:top_k]
        return result
    
    def search_simple(self, query: str, top_k: int = 10) -> List[tuple]:
        """
        Simple search using kernel directly
        
        Args:
            query: Search query
            top_k: Number of results
        
        Returns:
            List of (item, similarity) tuples
        """
        return self.kernel.find_similar(query, self.items, top_k=top_k)
    
    # ==================== Understanding ====================
    
    def understand_intent(self, text: str, context: List[str] = None) -> Dict:
        """Understand user intent"""
        return self.ai.understanding.understand_intent(text, context)
    
    # ==================== Knowledge Graph ====================
    
    def build_knowledge_graph(self) -> Dict:
        """Build knowledge graph of all items"""
        return self.ai.knowledge_graph.build_graph(self.items)
    
    def find_relationships(self) -> Dict:
        """Find relationships between items"""
        return self.kernel.build_relationship_graph(self.items)
    
    def discover_themes(self, min_cluster_size: int = 3) -> List[Dict]:
        """Discover themes in items"""
        return self.kernel.discover_themes(self.items, min_cluster_size)
    
    # ==================== Reasoning ====================
    
    def reason(self, premises: List[str], question: str) -> Dict:
        """Logical reasoning"""
        return self.ai.reasoning.reason(premises, question)
    
    # ==================== Conversation ====================
    
    def chat(self, message: str) -> str:
        """Conversational interface"""
        return self.ai.conversation.respond(message)
    
    # ==================== Text Generation (if LLM enabled) ====================
    
    def generate_text(self, prompt: str, max_length: int = 200) -> Dict:
        """
        Generate grounded text (requires LLM)
        
        Args:
            prompt: Generation prompt
            max_length: Maximum length of generated text
        
        Returns:
            Dictionary with generated text and metadata
        """
        if not self.llm:
            raise ValueError("LLM not enabled. Initialize with enable_llm=True")
        
        return self.llm.generate_grounded(
            prompt, 
            max_length=max_length,
            require_validation=True
        )
    
    def chat_with_generation(self, message: str) -> Dict:
        """
        Conversational interface with text generation
        
        Args:
            message: User message
        
        Returns:
            Dictionary with response and metadata
        """
        if not self.llm:
            raise ValueError("LLM not enabled. Initialize with enable_llm=True")
        
        # Understand intent
        intent = self.understand_intent(message)
        
        # Search for relevant context
        search_results = self.search(message, top_k=3)
        
        # Build context from search results
        context = "\n".join([
            result['text'] for result in search_results.get('results', [])[:3]
        ])
        
        # Generate grounded response
        prompt = f"Based on this context:\n{context}\n\nAnswer: {message}"
        generation = self.generate_text(prompt, max_length=150)
        
        return {
            "response": generation['generated'],
            "intent": intent,
            "confidence": generation['confidence'],
            "is_safe": generation['is_safe'],
            "sources": generation.get('sources', [])
        }
    
    # ==================== Learning ====================
    
    def learn_from_examples(self, examples: List[tuple]) -> Dict:
        """
        Learn from examples
        
        Args:
            examples: List of (input, output) tuples
        
        Returns:
            Learning results
        """
        return self.ai.learning.learn_from_examples(examples)
    
    # ==================== Statistics ====================
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        stats = self.ai.get_stats()
        stats['items_count'] = len(self.items)
        stats['llm_enabled'] = self.llm is not None
        return stats
    
    def get_kernel_stats(self) -> Dict:
        """Get kernel statistics"""
        return self.kernel.get_stats()
    
    # ==================== Utility ====================
    
    def clear_cache(self):
        """Clear kernel cache"""
        self.kernel.clear_cache()
    
    def reset(self):
        """Reset the entire system"""
        self.ai.reset()
        self.items.clear()
        if self.llm:
            # Reset LLM if needed
            pass


# ==================== Example Usage ====================

def example_usage():
    """Example of how to use the app"""
    
    print("=" * 80)
    print("APP TEMPLATE - EXAMPLE USAGE")
    print("=" * 80)
    
    # Create app without LLM (for search, understanding, etc.)
    print("\n[1] Creating app without LLM...")
    app = MyApp(enable_llm=False)
    
    # Add items
    print("\n[2] Adding items...")
    app.add_item("God is love")
    app.add_item("Love is patient and kind")
    app.add_item("Faith, hope, and love - but the greatest is love")
    app.add_item("By grace you have been saved through faith")
    
    # Search
    print("\n[3] Searching...")
    results = app.search("divine love", top_k=3)
    print(f"Found {len(results['results'])} results:")
    for result in results['results']:
        print(f"  - {result['text'][:50]}... (similarity: {result['similarity']:.3f})")
    
    # Understand intent
    print("\n[4] Understanding intent...")
    intent = app.understand_intent("I want to search for information about love")
    print(f"Intent: {intent['intent']}")
    print(f"Confidence: {intent['confidence']:.3f}")
    
    # Build knowledge graph
    print("\n[5] Building knowledge graph...")
    graph = app.build_knowledge_graph()
    print(f"Nodes: {len(graph['nodes'])}")
    print(f"Edges: {len(graph['edges'])}")
    print(f"Themes: {len(graph['themes'])}")
    
    # Discover themes
    print("\n[6] Discovering themes...")
    themes = app.discover_themes()
    print(f"Found {len(themes)} themes:")
    for theme in themes:
        print(f"  - {theme['theme']}: {theme['size']} items")
    
    # Chat
    print("\n[7] Conversational interface...")
    response = app.chat("Tell me about love")
    print(f"Response: {response}")
    
    # Get stats
    print("\n[8] System statistics...")
    stats = app.get_stats()
    print(f"Items: {stats['items_count']}")
    print(f"Cache size: {stats['kernel']['cache_size']}")
    print(f"Embeddings computed: {stats['kernel']['embeddings_computed']}")
    
    print("\n" + "=" * 80)
    print("EXAMPLE COMPLETE")
    print("=" * 80)
    
    # Example with LLM
    print("\n" + "=" * 80)
    print("EXAMPLE WITH LLM")
    print("=" * 80)
    
    print("\n[1] Creating app with LLM...")
    app_with_llm = MyApp(
        enable_llm=True,
        source_texts=[
            "God is love",
            "Love is patient and kind",
            "Faith, hope, and love"
        ]
    )
    
    print("\n[2] Generating text...")
    generation = app_with_llm.generate_text("Explain what love means", max_length=100)
    print(f"Generated: {generation['generated']}")
    print(f"Confidence: {generation['confidence']:.3f}")
    print(f"Safe: {generation['is_safe']}")
    
    print("\n[3] Chat with generation...")
    chat_result = app_with_llm.chat_with_generation("What is love?")
    print(f"Response: {chat_result['response']}")
    print(f"Confidence: {chat_result['confidence']:.3f}")
    
    print("\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    example_usage()
