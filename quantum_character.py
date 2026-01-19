"""
Quantum-Based Character Model
Uses quantum entanglement and superposition for more meaningful responses
"""
import numpy as np
import torch
import torch.nn as nn
from typing import List, Dict, Tuple, Optional
from quantum_tokenizer import QuantumTokenizer
from quantum_llm import QuantumLLM, QuantumLLMTrainer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QuantumCharacter:
    """
    Quantum-based character model that generates more meaningful responses
    by leveraging quantum entanglement and semantic understanding
    """
    
    def __init__(
        self,
        tokenizer: QuantumTokenizer,
        model: QuantumLLM,
        personality_traits: Optional[Dict[str, float]] = None,
        knowledge_base: Optional[List[str]] = None
    ):
        self.tokenizer = tokenizer
        self.model = model
        self.personality_traits = personality_traits or {}
        self.knowledge_base = knowledge_base or []
        self.conversation_history = []
        
    def _get_context_quantum_state(self, conversation: List[str]) -> np.ndarray:
        """Get quantum state representing conversation context"""
        if not conversation:
            return np.zeros(self.tokenizer.dimension, dtype=complex)
        
        # Combine all conversation turns
        combined_text = " ".join(conversation)
        tokens = self.tokenizer.encode(combined_text)
        
        context_state = np.zeros(self.tokenizer.dimension, dtype=complex)
        
        for token_id in tokens:
            token = self.tokenizer.id_to_token.get(token_id)
            if token and token in self.tokenizer.vocab:
                qt = self.tokenizer.vocab[token]
                if qt.quantum_state is not None:
                    # Weight by position (more recent = higher weight)
                    weight = 1.0 + (len(conversation) - conversation.index(conversation[-1])) * 0.1
                    context_state += weight * qt.amplitude * qt.quantum_state
        
        norm = np.linalg.norm(context_state)
        if norm > 0:
            context_state = context_state / norm
        
        return context_state
    
    def _find_semantically_relevant_knowledge(
        self,
        query_state: np.ndarray,
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """Find knowledge base entries semantically relevant to query"""
        if not self.knowledge_base:
            return []
        
        relevant = []
        
        for knowledge in self.knowledge_base:
            knowledge_state = self._get_text_quantum_state(knowledge)
            similarity = np.abs(np.vdot(query_state, knowledge_state))
            
            # Also check entanglement
            query_tokens = set(self.tokenizer.encode(self.conversation_history[-1] if self.conversation_history else ""))
            knowledge_tokens = set(self.tokenizer.encode(knowledge))
            
            entanglement_score = 0.0
            for q_token_id in query_tokens:
                q_token = self.tokenizer.id_to_token.get(q_token_id)
                if q_token and q_token in self.tokenizer.vocab:
                    entangled = self.tokenizer.get_entangled_tokens(q_token, top_k=10)
                    for k_token_id in knowledge_tokens:
                        k_token = self.tokenizer.id_to_token.get(k_token_id)
                        if k_token:
                            for ent_token, strength in entangled:
                                if ent_token == k_token:
                                    entanglement_score += strength
            
            total_score = similarity * (1 + entanglement_score / max(len(query_tokens), 1))
            relevant.append((knowledge, float(total_score)))
        
        relevant.sort(key=lambda x: x[1], reverse=True)
        return relevant[:top_k]
    
    def _get_text_quantum_state(self, text: str) -> np.ndarray:
        """Get quantum state for text"""
        tokens = self.tokenizer.encode(text)
        
        if not tokens:
            return np.zeros(self.tokenizer.dimension, dtype=complex)
        
        text_state = np.zeros(self.tokenizer.dimension, dtype=complex)
        
        for token_id in tokens:
            token = self.tokenizer.id_to_token.get(token_id)
            if token and token in self.tokenizer.vocab:
                qt = self.tokenizer.vocab[token]
                if qt.quantum_state is not None:
                    text_state += qt.amplitude * qt.quantum_state
        
        norm = np.linalg.norm(text_state)
        if norm > 0:
            text_state = text_state / norm
        
        return text_state
    
    def _apply_personality(self, response: str) -> str:
        """Apply personality traits to response"""
        # This is a simplified personality system
        # In production, you'd have more sophisticated personality modeling
        
        if self.personality_traits.get("warmth", 0) > 0.7:
            # Make response warmer
            response = response.replace(".", "!").replace("?", "?")
        
        if self.personality_traits.get("depth", 0) > 0.7:
            # Add more thoughtful language
            if not any(word in response.lower() for word in ["because", "since", "therefore"]):
                # Add reasoning
                pass
        
        return response
    
    def generate_response(
        self,
        user_input: str,
        use_quantum_context: bool = True,
        use_knowledge_base: bool = True,
        temperature: float = 0.8
    ) -> str:
        """Generate response using quantum methods for deeper understanding"""
        self.conversation_history.append(user_input)
        
        # Get quantum state of user input
        query_state = self._get_text_quantum_state(user_input)
        
        # Get conversation context quantum state
        context_state = self._get_context_quantum_state(self.conversation_history[-5:])  # Last 5 turns
        
        # Find semantically relevant knowledge
        relevant_knowledge = []
        if use_knowledge_base:
            relevant_knowledge = self._find_semantically_relevant_knowledge(query_state, top_k=3)
        
        # Build enhanced prompt with quantum context
        prompt_parts = []
        
        # Add relevant knowledge if found
        if relevant_knowledge:
            prompt_parts.append("Context: " + " ".join([k[0] for k in relevant_knowledge[:2]]))
        
        # Add conversation history
        if len(self.conversation_history) > 1:
            prompt_parts.append("Previous: " + self.conversation_history[-2])
        
        prompt_parts.append("User: " + user_input)
        prompt_parts.append("Response:")
        
        enhanced_prompt = " ".join(prompt_parts)
        
        # Generate using quantum LLM
        response = self.model.generate(
            self.tokenizer,
            enhanced_prompt,
            max_length=150,
            temperature=temperature,
            top_k=50,
            top_p=0.9
        )
        
        # Extract just the response part (remove prompt)
        if "Response:" in response:
            response = response.split("Response:")[-1].strip()
        
        # Apply personality
        response = self._apply_personality(response)
        
        self.conversation_history.append(response)
        return response
    
    def generate_quantum_enhanced_response(
        self,
        user_input: str,
        temperature: float = 0.8
    ) -> Dict:
        """Generate response with quantum enhancement and analysis"""
        # Standard generation
        standard_response = self.generate_response(
            user_input,
            use_quantum_context=False,
            use_knowledge_base=False,
            temperature=temperature
        )
        
        # Quantum-enhanced generation
        quantum_response = self.generate_response(
            user_input,
            use_quantum_context=True,
            use_knowledge_base=True,
            temperature=temperature
        )
        
        # Analyze semantic depth
        query_state = self._get_text_quantum_state(user_input)
        standard_state = self._get_text_quantum_state(standard_response)
        quantum_state = self._get_text_quantum_state(quantum_response)
        
        standard_relevance = np.abs(np.vdot(query_state, standard_state))
        quantum_relevance = np.abs(np.vdot(query_state, quantum_state))
        
        # Find semantic connections
        query_tokens = set(self.tokenizer.encode(user_input))
        quantum_tokens = set(self.tokenizer.encode(quantum_response))
        
        semantic_connections = []
        for q_token_id in query_tokens:
            q_token = self.tokenizer.id_to_token.get(q_token_id)
            if q_token and q_token in self.tokenizer.vocab:
                entangled = self.tokenizer.get_entangled_tokens(q_token, top_k=10)
                for qt_token_id in quantum_tokens:
                    qt_token = self.tokenizer.id_to_token.get(qt_token_id)
                    if qt_token:
                        for ent_token, strength in entangled:
                            if ent_token == qt_token:
                                semantic_connections.append((q_token, qt_token, float(strength)))
        
        return {
            "standard_response": standard_response,
            "quantum_response": quantum_response,
            "standard_relevance": float(standard_relevance),
            "quantum_relevance": float(quantum_relevance),
            "improvement": float((quantum_relevance - standard_relevance) / standard_relevance * 100) if standard_relevance > 0 else 0,
            "semantic_connections": semantic_connections[:5]
        }


class ClassicalCharacter:
    """Classical character model for comparison"""
    
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model
        self.conversation_history = []
    
    def generate_response(self, user_input: str, temperature: float = 0.8) -> str:
        """Generate standard response"""
        self.conversation_history.append(user_input)
        
        # Simple prompt
        prompt = " ".join(self.conversation_history[-3:])  # Last 3 turns
        
        response = self.model.generate(
            self.tokenizer,
            prompt,
            max_length=150,
            temperature=temperature,
            top_k=50,
            top_p=0.9
        )
        
        # Extract response
        if user_input in response:
            response = response.split(user_input)[-1].strip()
        
        self.conversation_history.append(response)
        return response


def create_quantum_character(
    training_texts: List[str],
    personality_traits: Optional[Dict] = None,
    knowledge_base: Optional[List[str]] = None
) -> QuantumCharacter:
    """Create and train a quantum character"""
    logger.info("Creating quantum character...")
    
    # Train tokenizer
    tokenizer = QuantumTokenizer(vocab_size=5000, dimension=256)
    tokenizer.train(training_texts, min_frequency=2)
    
    # Create and train model
    model = QuantumLLM(
        vocab_size=len(tokenizer.vocab),
        d_model=256,
        n_heads=4,
        n_layers=3,
        d_ff=1024,
        max_seq_length=256
    )
    
    trainer = QuantumLLMTrainer(model, tokenizer, learning_rate=1e-3)
    trainer.train(training_texts, epochs=5, batch_size=8)
    
    # Create character
    character = QuantumCharacter(
        tokenizer=tokenizer,
        model=model,
        personality_traits=personality_traits,
        knowledge_base=knowledge_base
    )
    
    return character


def create_classical_character(training_texts: List[str]):
    """Create classical character for comparison"""
    from quantum_vs_classical_test import ClassicalTokenizer, ClassicalLLM, ClassicalLLMTrainer
    
    tokenizer = ClassicalTokenizer(vocab_size=5000)
    tokenizer.train(training_texts, min_frequency=2)
    
    model = ClassicalLLM(
        vocab_size=len(tokenizer.vocab),
        d_model=256,
        n_heads=4,
        n_layers=3,
        d_ff=1024,
        max_seq_length=256
    )
    
    trainer = ClassicalLLMTrainer(model, tokenizer, learning_rate=1e-3)
    trainer.train(training_texts, epochs=5, batch_size=8)
    
    return ClassicalCharacter(tokenizer, model)
