"""
Quantum-Inspired Text Generation
Uses quantum techniques for text generation without external LLMs
"""
import numpy as np
from quantum_kernel import QuantumKernel, get_kernel, KernelConfig
from typing import List, Dict, Optional
import random


class QuantumTextGenerator:
    """
    Text generation using quantum-inspired techniques
    Uses quantum superposition and measurement for token prediction
    """
    
    def __init__(self, kernel: Optional[QuantumKernel] = None):
        self.kernel = kernel or get_kernel(KernelConfig())
        self.vocab = {}
        self.token_embeddings = {}
        self.context_window = []
        self.max_context = 10
    
    def build_vocab(self, texts: List[str], merge: bool = True):
        """Build vocabulary from texts"""
        words = set()
        for text in texts:
            # Clean text - remove special characters, keep only words
            import re
            clean_text = re.sub(r'[^\w\s]', ' ', text.lower())
            words.update(clean_text.split())
        
        # Merge with existing vocab or replace
        if merge and self.vocab:
            self.vocab.update({word: len(self.vocab) + i for i, word in enumerate(sorted(words - set(self.vocab.keys())))})
        else:
            self.vocab = {word: i for i, word in enumerate(sorted(words))}
        
        # Create/update embeddings for new words
        for word in words:
            if word not in self.token_embeddings:
                self.token_embeddings[word] = self.kernel.embed(word)
        
        if not merge:
            print(f"Built vocabulary: {len(self.vocab)} words")
    
    def quantum_token_prediction(self, context: str, top_k: int = 5) -> List[tuple]:
        """
        Predict next tokens using quantum superposition
        Uses semantic similarity to find likely next words
        Also considers learned patterns from LLM outputs
        """
        # Embed the context
        context_embedding = self.kernel.embed(context)
        
        # Check learned pairs for better context matching
        learned_boost = {}
        if hasattr(self, 'learned_pairs'):
            for prompt, output in self.learned_pairs:
                # If context matches learned prompt, boost words from that output
                prompt_sim = self.kernel.similarity(context, prompt)
                if prompt_sim > 0.6:  # Strong match
                    output_words = output.lower().split()
                    context_words = context.lower().split()
                    # Boost words that come after context in learned output
                    for i, word in enumerate(output_words):
                        if i > 0 and output_words[i-1] in context_words:
                            if word not in learned_boost:
                                learned_boost[word] = 0
                            learned_boost[word] += prompt_sim * 0.3  # Boost factor
        
        # Find semantically similar words (quantum search)
        candidates = []
        for word, word_embedding in self.token_embeddings.items():
            # Compute similarity (quantum measurement)
            similarity = float(np.abs(np.dot(context_embedding, word_embedding)))
            
            # Apply learned boost if available
            if word in learned_boost:
                similarity += learned_boost[word]
            
            candidates.append((word, similarity))
        
        # Sort by similarity (quantum amplitude)
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k (quantum measurement result)
        return candidates[:top_k]
    
    def generate_text(self, prompt: str, max_length: int = 50, temperature: float = 0.7) -> str:
        """
        Generate text using quantum-inspired techniques
        """
        generated = prompt.split()
        context = prompt
        
        for _ in range(max_length):
            # Predict next tokens using quantum superposition
            candidates = self.quantum_token_prediction(context, top_k=10)
            
            if not candidates:
                break
            
            # Apply temperature for diversity (quantum probability)
            if temperature > 0:
                # Convert similarities to probabilities
                similarities = np.array([c[1] for c in candidates])
                # Apply temperature
                probabilities = np.exp(similarities / temperature)
                probabilities = probabilities / probabilities.sum()
                
                # Sample from distribution (quantum measurement)
                next_word = np.random.choice(
                    [c[0] for c in candidates],
                    p=probabilities
                )
            else:
                # Deterministic (highest probability)
                next_word = candidates[0][0]
            
            generated.append(next_word)
            
            # Update context (sliding window)
            context = " ".join(generated[-self.max_context:])
            
            # Stop if we hit a natural stopping point
            if next_word in ['.', '!', '?'] and len(generated) > 10:
                break
        
        return " ".join(generated)
    
    def generate_continuation(self, prompt: str, length: int = 20) -> str:
        """Generate continuation of text"""
        if not self.vocab:
            return prompt  # No vocab built yet
        
        continuation = self.generate_text(prompt, max_length=length)
        # Return only the continuation part
        prompt_words = prompt.split()
        continuation_words = continuation.split()
        if len(continuation_words) > len(prompt_words):
            return " ".join(continuation_words[len(prompt_words):])
        return ""
    
    def beam_search_generate(self, prompt: str, beam_width: int = 3, max_length: int = 30) -> str:
        """
        Generate text using beam search (quantum-inspired parallel exploration)
        """
        beams = [(prompt.split(), 1.0)]  # (sequence, score)
        
        for _ in range(max_length):
            new_beams = []
            
            for sequence, score in beams:
                context = " ".join(sequence[-self.max_context:])
                candidates = self.quantum_token_prediction(context, top_k=beam_width)
                
                for word, similarity in candidates:
                    new_sequence = sequence + [word]
                    new_score = score * similarity  # Cumulative probability
                    new_beams.append((new_sequence, new_score))
            
            # Keep top beams (quantum amplitude amplification)
            beams = sorted(new_beams, key=lambda x: x[1], reverse=True)[:beam_width]
            
            # Check for stopping
            if beams[0][0][-1] in ['.', '!', '?']:
                break
        
        # Return best beam
        return " ".join(beams[0][0])


class QuantumTranslator:
    """
    Translation using quantum-inspired semantic matching
    Uses semantic embeddings to find equivalent meanings across languages
    """
    
    def __init__(self, kernel: Optional[QuantumKernel] = None):
        self.kernel = kernel or get_kernel(KernelConfig())
        self.source_lang_phrases = {}  # source_lang -> {phrase: embedding}
        self.target_lang_phrases = {}  # target_lang -> {phrase: embedding}
        self.translation_pairs = []  # [(source, target, similarity)]
    
    def add_bilingual_pair(self, source_text: str, target_text: str, source_lang: str = "en", target_lang: str = "es"):
        """Add a translation pair for learning"""
        source_embedding = self.kernel.embed(source_text)
        target_embedding = self.kernel.embed(target_text)
        
        if source_lang not in self.source_lang_phrases:
            self.source_lang_phrases[source_lang] = {}
        if target_lang not in self.target_lang_phrases:
            self.target_lang_phrases[target_lang] = {}
        
        self.source_lang_phrases[source_lang][source_text] = source_embedding
        self.target_lang_phrases[target_lang][target_text] = target_embedding
        
        # Store translation pair
        similarity = self.kernel.similarity(source_text, target_text)
        self.translation_pairs.append((source_text, target_text, similarity, source_lang, target_lang))
    
    def translate(self, text: str, source_lang: str = "en", target_lang: str = "es") -> str:
        """
        Translate text using quantum semantic matching
        Finds semantically equivalent text in target language
        """
        # Embed source text
        source_embedding = self.kernel.embed(text)
        
        # Find most similar target language phrase (quantum search)
        best_match = None
        best_similarity = 0.0
        
        if target_lang in self.target_lang_phrases:
            for target_text, target_embedding in self.target_lang_phrases[target_lang].items():
                # Compute semantic similarity (quantum measurement)
                similarity = float(np.abs(np.dot(source_embedding, target_embedding)))
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = target_text
        
        if best_match and best_similarity > 0.5:  # Threshold
            return best_match
        
        # Fallback: word-by-word translation using learned pairs
        words = text.split()
        translated_words = []
        
        for word in words:
            # Find best matching word in target language
            word_embedding = self.kernel.embed(word)
            best_word = word
            best_sim = 0.0
            
            if target_lang in self.target_lang_phrases:
                for target_phrase, target_emb in self.target_lang_phrases[target_lang].items():
                    # Check if this phrase contains a word similar to our word
                    target_words = target_phrase.split()
                    for target_word in target_words:
                        if len(target_word) > 2:  # Skip very short words
                            target_word_emb = self.kernel.embed(target_word)
                            sim = float(np.abs(np.dot(word_embedding, target_word_emb)))
                            if sim > best_sim:
                                best_sim = sim
                                best_word = target_word
            
            if best_sim > 0.6:
                translated_words.append(best_word)
            else:
                translated_words.append(word)  # Keep original if no match
        
        return " ".join(translated_words)
    
    def learn_from_examples(self, examples: List[tuple]):
        """Learn translation patterns from examples"""
        for source, target, source_lang, target_lang in examples:
            self.add_bilingual_pair(source, target, source_lang, target_lang)
        
        print(f"Learned {len(self.translation_pairs)} translation pairs")


def demonstrate_quantum_text_generation():
    """Demonstrate quantum text generation"""
    print("=" * 80)
    print("QUANTUM TEXT GENERATION")
    print("=" * 80)
    
    # Training texts
    training_texts = [
        "God is love and love is patient",
        "Faith is the assurance of things hoped for",
        "By grace you have been saved through faith",
        "The Lord is my shepherd I shall not want",
        "In the beginning was the Word",
        "Love is patient love is kind",
        "For God so loved the world",
        "Blessed are the peacemakers"
    ]
    
    # Create generator
    generator = QuantumTextGenerator()
    generator.build_vocab(training_texts)
    
    # Generate text
    print("\n1. Text Generation")
    print("-" * 80)
    prompt = "God is"
    generated = generator.generate_text(prompt, max_length=15, temperature=0.7)
    print(f"Prompt: '{prompt}'")
    print(f"Generated: '{generated}'")
    
    print("\n2. Continuation")
    print("-" * 80)
    prompt2 = "Love is"
    continuation = generator.generate_continuation(prompt2, length=10)
    print(f"Prompt: '{prompt2}'")
    print(f"Continuation: '{continuation}'")
    
    print("\n3. Beam Search Generation")
    print("-" * 80)
    prompt3 = "Faith is"
    beam_result = generator.beam_search_generate(prompt3, beam_width=3, max_length=10)
    print(f"Prompt: '{prompt3}'")
    print(f"Beam Search: '{beam_result}'")


def demonstrate_quantum_translation():
    """Demonstrate quantum translation"""
    print("\n" + "=" * 80)
    print("QUANTUM TRANSLATION")
    print("=" * 80)
    
    # Create translator
    translator = QuantumTranslator()
    
    # Learn from examples
    examples = [
        ("God is love", "Dios es amor", "en", "es"),
        ("Love is patient", "El amor es paciente", "en", "es"),
        ("Faith is the assurance", "La fe es la certeza", "en", "es"),
        ("The Lord is my shepherd", "El Señor es mi pastor", "en", "es"),
        ("Blessed are the peacemakers", "Bienaventurados los pacificadores", "en", "es")
    ]
    
    translator.learn_from_examples(examples)
    
    # Translate
    print("\n1. Phrase Translation")
    print("-" * 80)
    test_phrases = [
        "God is love",
        "Love is patient",
        "Faith is the assurance"
    ]
    
    for phrase in test_phrases:
        translation = translator.translate(phrase, source_lang="en", target_lang="es")
        print(f"English: '{phrase}'")
        print(f"Spanish: '{translation}'")
        print()
    
    print("\n2. Word-by-Word Translation")
    print("-" * 80)
    test_text = "The Lord is my shepherd"
    translation = translator.translate(test_text, source_lang="en", target_lang="es")
    print(f"English: '{test_text}'")
    print(f"Spanish: '{translation}'")


def main():
    """Run all demonstrations"""
    demonstrate_quantum_text_generation()
    demonstrate_quantum_translation()
    
    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print("""
Quantum-inspired techniques CAN be used for:

[+] Text Generation
    - Uses quantum superposition for token prediction
    - Semantic similarity for next-word selection
    - Quantum measurement for sampling
    - Beam search for parallel exploration

[+] Translation
    - Uses semantic embeddings for meaning matching
    - Quantum search to find equivalent phrases
    - Word-by-word translation using learned pairs
    - Semantic similarity for accuracy

These techniques work by:
1. Using semantic embeddings (quantum states)
2. Finding similar meanings (quantum search)
3. Sampling from distributions (quantum measurement)
4. Exploring multiple paths (quantum superposition)

While not as sophisticated as large language models,
quantum techniques provide a lightweight alternative
that works entirely within the quantum AI system!
    """)


if __name__ == "__main__":
    main()
