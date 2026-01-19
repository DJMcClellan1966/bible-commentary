"""
AI System Components
Individual components that can be used independently or together
"""
from quantum_kernel import QuantumKernel
from typing import List, Dict, Tuple, Optional
import logging

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
    
    def add_intent(self, intent: str):
        """Add a new intent to the system"""
        if intent not in self.known_intents:
            self.known_intents.append(intent)
            logger.info(f"Added new intent: {intent}")


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
    
    def get_graph(self) -> Dict:
        """Get the current knowledge graph"""
        return self.graph
    
    def add_document(self, document: str) -> Dict:
        """Add a document and update the graph"""
        # This would require rebuilding the graph
        # For now, return current graph
        logger.warning("add_document requires rebuilding graph - use build_graph with all documents")
        return self.graph


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
    
    def search(self, query: str, corpus: List[str], top_k: int = 10) -> List[Tuple[str, float]]:
        """Simple semantic search"""
        return self.kernel.find_similar(query, corpus, top_k=top_k)


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
    
    def get_patterns(self) -> Dict:
        """Get learned patterns"""
        return self.learned_patterns
    
    def apply_pattern(self, input_text: str) -> Optional[str]:
        """Apply learned pattern to input"""
        # Find matching pattern
        for pattern_input, pattern_data in self.learned_patterns.items():
            similarity = self.kernel.similarity(input_text, pattern_input)
            if similarity > 0.7:
                return pattern_data.get("output_theme")
        return None


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
    
    def get_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def add_response_template(self, intent: str, template: str):
        """Add a custom response template"""
        self.responses[intent] = template
        logger.info(f"Added response template for intent: {intent}")
