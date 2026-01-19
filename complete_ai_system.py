"""
Complete AI System Built Around Quantum Kernel
Demonstrates what can be built on top of the kernel
"""
from quantum_kernel import QuantumKernel, KernelConfig, get_kernel
from typing import List, Dict, Tuple, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SemanticUnderstandingEngine:
    """Understand meaning, intent, and context"""
    
    def __init__(self, kernel: QuantumKernel):
        self.kernel = kernel
        self.known_intents = [
            "search for information",
            "ask a question",
            "request recommendation",
            "create content",
            "analyze data",
            "find relationships"
        ]
    
    def understand_intent(self, query: str, context: List[str] = None) -> Dict:
        """Understand user intent"""
        # Find similar intents
        similar_intents = self.kernel.find_similar(
            query, self.known_intents, top_k=3
        )
        
        # Context relevance
        context_relevance = 0.0
        if context:
            context_text = " ".join(context)
            context_relevance = self.kernel.similarity(context_text, query)
        
        return {
            "intent": similar_intents[0][0] if similar_intents else "unknown",
            "confidence": similar_intents[0][1] if similar_intents else 0.0,
            "context_relevance": context_relevance,
            "alternative_intents": [
                {"intent": intent, "confidence": conf}
                for intent, conf in similar_intents[1:]
            ]
        }


class KnowledgeGraphBuilder:
    """Build and maintain knowledge graphs"""
    
    def __init__(self, kernel: QuantumKernel):
        self.kernel = kernel
        self.graph = {}
    
    def build_graph(self, documents: List[str]) -> Dict:
        """Build knowledge graph from documents"""
        # Discover relationships
        relationship_graph = self.kernel.build_relationship_graph(documents)
        
        # Discover themes
        themes = self.kernel.discover_themes(documents, min_cluster_size=2)
        
        # Build graph structure
        graph = {
            "nodes": [
                {"id": i, "text": doc, "embedding": self.kernel.embed(doc).tolist()}
                for i, doc in enumerate(documents)
            ],
            "edges": [
                {
                    "source": i,
                    "target": j,
                    "weight": sim,
                    "type": "semantic_similarity"
                }
                for i, (text, related) in enumerate(relationship_graph.items())
                for rel_text, sim in related
                for j, doc in enumerate(documents)
                if doc == rel_text
            ],
            "themes": [
                {
                    "theme": theme["theme"],
                    "nodes": [documents.index(t) for t in theme["texts"]],
                    "confidence": theme["confidence"]
                }
                for theme in themes
            ]
        }
        
        self.graph = graph
        return graph


class IntelligentSearch:
    """Advanced search with discovery"""
    
    def __init__(self, kernel: QuantumKernel):
        self.kernel = kernel
    
    def search_and_discover(self, query: str, corpus: List[str]) -> Dict:
        """Search and discover related concepts"""
        # Semantic search
        results = self.kernel.find_similar(query, corpus, top_k=20)
        
        # Discover related concepts from top results
        top_results_texts = [text for text, _ in results[:5]]
        if top_results_texts:
            related_concepts = self.kernel.build_relationship_graph(top_results_texts)
        else:
            related_concepts = {}
        
        # Find patterns
        if len(results) >= 3:
            themes = self.kernel.discover_themes(
                [text for text, _ in results[:10]], min_cluster_size=2
            )
        else:
            themes = []
        
        return {
            "query": query,
            "results": [
                {"text": text, "similarity": sim}
                for text, sim in results
            ],
            "related_concepts": related_concepts,
            "themes": themes,
            "count": len(results)
        }


class ReasoningEngine:
    """Logical and causal reasoning"""
    
    def __init__(self, kernel: QuantumKernel):
        self.kernel = kernel
        self.reasoning_patterns = [
            "if A then B",
            "A causes B",
            "A is similar to B",
            "A implies B"
        ]
    
    def reason(self, premises: List[str], question: str) -> Dict:
        """Perform reasoning"""
        # Build relationship graph of premises
        premise_graph = self.kernel.build_relationship_graph(premises)
        
        # Find logical connections
        connections = []
        for premise, related in premise_graph.items():
            for rel_premise, similarity in related:
                if similarity > 0.7:  # Strong connection
                    connections.append({
                        "from": premise,
                        "to": rel_premise,
                        "strength": similarity,
                        "type": "semantic_connection"
                    })
        
        # Compute overall coherence
        coherence = self._compute_coherence(premises, premise_graph)
        
        # Answer question based on premises
        answer_relevance = self.kernel.similarity(
            " ".join(premises), question
        )
        
        return {
            "premises": premises,
            "question": question,
            "connections": connections,
            "coherence": coherence,
            "answer_relevance": answer_relevance,
            "confidence": min(coherence, answer_relevance)
        }
    
    def _compute_coherence(self, premises: List[str], graph: Dict) -> float:
        """Compute how coherent the premises are"""
        if len(premises) < 2:
            return 1.0
        
        similarities = []
        for i, p1 in enumerate(premises):
            for p2 in premises[i+1:]:
                sim = self.kernel.similarity(p1, p2)
                similarities.append(sim)
        
        return float(sum(similarities) / len(similarities)) if similarities else 0.0


class LearningSystem:
    """Continuous learning and adaptation"""
    
    def __init__(self, kernel: QuantumKernel):
        self.kernel = kernel
        self.learned_patterns = {}
    
    def learn_from_examples(self, examples: List[Tuple[str, str]]) -> Dict:
        """Learn patterns from examples"""
        input_texts = [ex[0] for ex in examples]
        output_texts = [ex[1] for ex in examples]
        
        # Discover themes in inputs
        input_themes = self.kernel.discover_themes(input_texts, min_cluster_size=2)
        
        # Discover themes in outputs
        output_themes = self.kernel.discover_themes(output_texts, min_cluster_size=2)
        
        # Map input themes to output themes
        patterns = {}
        for in_theme in input_themes:
            # Find which output themes correspond
            best_match = None
            best_score = 0.0
            
            for out_theme in output_themes:
                # Compute similarity between theme texts
                in_text = " ".join(in_theme["texts"])
                out_text = " ".join(out_theme["texts"])
                score = self.kernel.similarity(in_text, out_text)
                
                if score > best_score:
                    best_score = score
                    best_match = out_theme
            
            if best_match and best_score > 0.6:
                patterns[in_theme["theme"]] = {
                    "output_theme": best_match["theme"],
                    "confidence": best_score
                }
        
        self.learned_patterns.update(patterns)
        
        return {
            "patterns_learned": len(patterns),
            "input_themes": len(input_themes),
            "output_themes": len(output_themes),
            "patterns": patterns
        }


class ConversationalAI:
    """Natural conversation with context"""
    
    def __init__(self, kernel: QuantumKernel):
        self.kernel = kernel
        self.conversation_history = []
        self.responses = {
            "search for information": "I found some relevant information for you.",
            "ask a question": "Let me help answer that question.",
            "request recommendation": "Based on your preferences, I recommend:",
            "create content": "I can help create content on that topic.",
            "analyze data": "Let me analyze that data for you.",
            "find relationships": "I discovered some interesting relationships."
        }
    
    def respond(self, user_message: str) -> str:
        """Generate contextual response"""
        # Find relevant conversation history
        if self.conversation_history:
            recent_messages = [
                msg.get("user", "") or msg.get("text", "")
                for msg in self.conversation_history[-5:]
            ]
            recent_messages = [m for m in recent_messages if m]
            if recent_messages:
                relevant = self.kernel.find_similar(
                    user_message, recent_messages, top_k=2
                )
            else:
                relevant = []
        else:
            relevant = []
        
        # Understand intent
        understanding = SemanticUnderstandingEngine(self.kernel)
        context_messages = [
            msg.get("user", "") or msg.get("text", "")
            for msg in self.conversation_history[-3:]
        ]
        context_messages = [m for m in context_messages if m]
        intent_result = understanding.understand_intent(
            user_message,
            context_messages
        )
        
        # Generate response
        intent = intent_result["intent"]
        base_response = self.responses.get(intent, "I understand. Let me help with that.")
        
        # Add context if relevant
        if relevant:
            context_note = f" (Related to our previous discussion about '{relevant[0][0][:30]}...')"
            response = base_response + context_note
        else:
            response = base_response
        
        # Update history
        self.conversation_history.append({
            "user": user_message,
            "assistant": response,
            "intent": intent
        })
        
        return response


class CompleteAISystem:
    """
    Complete AI system built around quantum kernel
    Demonstrates full capabilities
    """
    
    def __init__(self):
        # Initialize kernel
        self.kernel = get_kernel(KernelConfig(
            embedding_dim=256,
            cache_size=50000,
            enable_caching=True
        ))
        
        # Build all components
        self.understanding = SemanticUnderstandingEngine(self.kernel)
        self.knowledge_graph = KnowledgeGraphBuilder(self.kernel)
        self.search = IntelligentSearch(self.kernel)
        self.reasoning = ReasoningEngine(self.kernel)
        self.learning = LearningSystem(self.kernel)
        self.conversation = ConversationalAI(self.kernel)
        
        logger.info("Complete AI System initialized")
    
    def process(self, input_data: Dict) -> Dict:
        """Process input through complete AI system"""
        query = input_data.get("query", "")
        message = input_data.get("message", "")
        premises = input_data.get("premises", [])
        question = input_data.get("question", "")
        documents = input_data.get("documents", [])
        
        results = {}
        
        # Understanding
        if query or message:
            text = query or message
            results["understanding"] = self.understanding.understand_intent(
                text, input_data.get("context", [])
            )
        
        # Search
        if query and documents:
            results["search"] = self.search.search_and_discover(query, documents)
        
        # Reasoning
        if premises and question:
            results["reasoning"] = self.reasoning.reason(premises, question)
        
        # Conversation
        if message:
            results["conversation"] = self.conversation.respond(message)
        
        # Knowledge graph
        if documents:
            results["knowledge_graph"] = self.knowledge_graph.build_graph(documents)
        
        # Learning
        if input_data.get("examples"):
            results["learning"] = self.learning.learn_from_examples(
                input_data["examples"]
            )
        
        results["kernel_stats"] = self.kernel.get_stats()
        
        return results


def demonstrate_complete_system():
    """Demonstrate the complete AI system"""
    print("=" * 80)
    print("COMPLETE AI SYSTEM BUILT AROUND QUANTUM KERNEL")
    print("=" * 80)
    
    # Create system
    system = CompleteAISystem()
    
    # Test documents
    documents = [
        "God is love and love is patient",
        "Faith is the assurance of things hoped for",
        "By grace you have been saved through faith",
        "The Lord is my shepherd, I shall not want",
        "In the beginning was the Word"
    ]
    
    # Test 1: Understanding
    print("\n1. SEMANTIC UNDERSTANDING")
    print("-" * 80)
    understanding = system.understanding.understand_intent(
        "I want to search for information about divine love"
    )
    print(f"Query: 'I want to search for information about divine love'")
    print(f"Intent: {understanding['intent']}")
    print(f"Confidence: {understanding['confidence']:.3f}")
    
    # Test 2: Knowledge Graph
    print("\n2. KNOWLEDGE GRAPH BUILDING")
    print("-" * 80)
    graph = system.knowledge_graph.build_graph(documents)
    print(f"Nodes: {len(graph['nodes'])}")
    print(f"Edges: {len(graph['edges'])}")
    print(f"Themes: {len(graph['themes'])}")
    for theme in graph['themes'][:2]:
        print(f"  - {theme['theme']}: {len(theme['nodes'])} nodes")
    
    # Test 3: Intelligent Search
    print("\n3. INTELLIGENT SEARCH")
    print("-" * 80)
    search_results = system.search.search_and_discover("divine love", documents)
    print(f"Query: 'divine love'")
    print(f"Results: {search_results['count']}")
    print(f"Themes discovered: {len(search_results['themes'])}")
    for result in search_results['results'][:3]:
        print(f"  - {result['text'][:50]}... (similarity: {result['similarity']:.3f})")
    
    # Test 4: Reasoning
    print("\n4. REASONING")
    print("-" * 80)
    reasoning = system.reasoning.reason(
        ["God is love", "Love is patient"],
        "What is God like?"
    )
    print(f"Premises: {reasoning['premises']}")
    print(f"Question: {reasoning['question']}")
    print(f"Connections: {len(reasoning['connections'])}")
    print(f"Coherence: {reasoning['coherence']:.3f}")
    print(f"Confidence: {reasoning['confidence']:.3f}")
    
    # Test 5: Learning
    print("\n5. LEARNING")
    print("-" * 80)
    examples = [
        ("What is love?", "Love is patient and kind"),
        ("What is faith?", "Faith is the assurance of things hoped for"),
        ("What is grace?", "Grace is unmerited favor")
    ]
    learning = system.learning.learn_from_examples(examples)
    print(f"Examples: {len(examples)}")
    print(f"Patterns learned: {learning['patterns_learned']}")
    print(f"Input themes: {learning['input_themes']}")
    print(f"Output themes: {learning['output_themes']}")
    
    # Test 6: Conversation
    print("\n6. CONVERSATION")
    print("-" * 80)
    response1 = system.conversation.respond("I want to search for information")
    print(f"User: 'I want to search for information'")
    print(f"AI: {response1}")
    
    response2 = system.conversation.respond("Tell me about love")
    print(f"\nUser: 'Tell me about love'")
    print(f"AI: {response2}")
    
    # Test 7: Complete Processing
    print("\n7. COMPLETE PROCESSING")
    print("-" * 80)
    result = system.process({
        "query": "divine love",
        "documents": documents,
        "premises": ["God is love", "Love is patient"],
        "question": "What is God like?",
        "message": "Help me understand love"
    })
    
    print("Processed through complete system:")
    print(f"  Understanding: {result.get('understanding', {}).get('intent', 'N/A')}")
    print(f"  Search results: {result.get('search', {}).get('count', 0)}")
    print(f"  Reasoning confidence: {result.get('reasoning', {}).get('confidence', 0):.3f}")
    print(f"  Conversation: {result.get('conversation', 'N/A')[:50]}...")
    
    # Final stats
    print("\n8. KERNEL STATISTICS")
    print("-" * 80)
    stats = system.kernel.get_stats()
    print(f"Embeddings computed: {stats['embeddings_computed']}")
    print(f"Similarities computed: {stats['similarities_computed']}")
    print(f"Cache hits: {stats['cache_hits']}")
    print(f"Cache size: {stats['cache_size']}")
    
    print("\n" + "=" * 80)
    print("SYSTEM DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("""
The complete AI system demonstrates:

[+] Semantic Understanding - Understands intent and context
[+] Knowledge Graphs - Builds relationships automatically
[+] Intelligent Search - Discovers related concepts
[+] Reasoning - Logical inference capabilities
[+] Learning - Pattern extraction from examples
[+] Conversation - Context-aware responses

All built on the quantum kernel foundation!
    """)


if __name__ == "__main__":
    demonstrate_complete_system()
