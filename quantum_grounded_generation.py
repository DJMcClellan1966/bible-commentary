"""
Grounded Quantum Text Generation
Generates text grounded in factual sources (Bible text, commentaries)
Prevents hallucinations, bias, and misinformation
"""
import numpy as np
from quantum_kernel import QuantumKernel, get_kernel, KernelConfig
from typing import List, Dict, Optional, Tuple
import re
from collections import Counter


class GroundedQuantumGenerator:
    """
    Quantum text generator grounded in factual sources
    Prevents hallucinations by only generating from verified content
    """
    
    def __init__(self, kernel: Optional[QuantumKernel] = None, 
                 source_texts: Optional[List[str]] = None):
        """
        Initialize grounded quantum generator
        
        Args:
            kernel: Quantum kernel instance
            source_texts: List of verified source texts (Bible verses, commentaries)
        """
        self.kernel = kernel or get_kernel(KernelConfig())
        self.source_texts = source_texts or []
        self.source_embeddings = {}
        self.verified_phrases = set()
        self.phrase_sources = {}  # phrase -> list of source texts
        self.confidence_threshold = 0.6  # Minimum similarity to source
        
        # Build verified phrase database
        if self.source_texts:
            self._build_verified_database()
    
    def _build_verified_database(self):
        """Build database of verified phrases from source texts"""
        print(f"Building verified database from {len(self.source_texts)} sources...")
        
        for source_text in self.source_texts:
            # Extract phrases (2-5 words)
            phrases = self._extract_phrases(source_text, min_words=2, max_words=5)
            
            for phrase in phrases:
                # Normalize phrase
                normalized = self._normalize_phrase(phrase)
                
                # Store phrase
                self.verified_phrases.add(normalized)
                
                # Track sources
                if normalized not in self.phrase_sources:
                    self.phrase_sources[normalized] = []
                self.phrase_sources[normalized].append(source_text[:100])  # Store excerpt
        
        # Create embeddings for all verified phrases
        for phrase in self.verified_phrases:
            self.source_embeddings[phrase] = self.kernel.embed(phrase)
        
        print(f"Built database: {len(self.verified_phrases)} verified phrases")
    
    def _extract_phrases(self, text: str, min_words: int = 2, max_words: int = 5) -> List[str]:
        """Extract phrases of various lengths from text"""
        words = re.findall(r'\b\w+\b', text.lower())
        phrases = []
        
        for length in range(min_words, max_words + 1):
            for i in range(len(words) - length + 1):
                phrase = " ".join(words[i:i+length])
                phrases.append(phrase)
        
        return phrases
    
    def _normalize_phrase(self, phrase: str) -> str:
        """Normalize phrase for matching"""
        # Remove extra spaces, lowercase
        return " ".join(phrase.lower().split())
    
    def add_source_texts(self, texts: List[str]):
        """Add more verified source texts"""
        self.source_texts.extend(texts)
        self._build_verified_database()
    
    def validate_against_sources(self, text: str) -> Dict:
        """
        Validate generated text against verified sources
        Returns confidence score and detected issues
        """
        words = text.lower().split()
        verified_words = 0
        unverified_phrases = []
        confidence_scores = []
        
        # Check phrases of various lengths
        for length in range(2, min(6, len(words) + 1)):
            for i in range(len(words) - length + 1):
                phrase = " ".join(words[i:i+length])
                normalized = self._normalize_phrase(phrase)
                
                # Check if phrase is verified
                if normalized in self.verified_phrases:
                    verified_words += length
                    confidence_scores.append(1.0)
                else:
                    # Check similarity to verified phrases
                    phrase_embedding = self.kernel.embed(phrase)
                    best_similarity = 0.0
                    best_match = None
                    
                    for verified_phrase, verified_embedding in self.source_embeddings.items():
                        similarity = float(np.abs(np.dot(phrase_embedding, verified_embedding)))
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_match = verified_phrase
                    
                    if best_similarity >= self.confidence_threshold:
                        verified_words += length
                        confidence_scores.append(best_similarity)
                    else:
                        unverified_phrases.append((phrase, best_similarity, best_match))
                        confidence_scores.append(best_similarity)
        
        # Calculate overall confidence
        total_checks = len(confidence_scores) if confidence_scores else 1
        avg_confidence = sum(confidence_scores) / total_checks if confidence_scores else 0.0
        
        # Detect potential issues
        issues = []
        if avg_confidence < self.confidence_threshold:
            issues.append("low_confidence")
        if len(unverified_phrases) > len(words) * 0.3:  # More than 30% unverified
            issues.append("high_unverified_content")
        if any(score < 0.3 for score in confidence_scores):
            issues.append("potential_hallucination")
        
        return {
            "confidence": avg_confidence,
            "verified_ratio": verified_words / len(words) if words else 0.0,
            "unverified_phrases": unverified_phrases[:5],  # Top 5
            "issues": issues,
            "is_safe": avg_confidence >= self.confidence_threshold and len(issues) == 0
        }
    
    def generate_grounded(self, prompt: str, max_length: int = 50, 
                         temperature: float = 0.7, require_validation: bool = True) -> Dict:
        """
        Generate text grounded in verified sources
        Only uses phrases that match verified content
        """
        # Find verified phrases similar to prompt
        prompt_embedding = self.kernel.embed(prompt)
        
        # Find best matching verified phrases
        candidate_phrases = []
        for phrase, phrase_embedding in self.source_embeddings.items():
            similarity = float(np.abs(np.dot(prompt_embedding, phrase_embedding)))
            if similarity >= self.confidence_threshold * 0.8:  # Slightly lower threshold for candidates
                candidate_phrases.append((phrase, similarity))
        
        # Sort by similarity
        candidate_phrases.sort(key=lambda x: x[1], reverse=True)
        
        if not candidate_phrases:
            return {
                "generated": prompt,
                "confidence": 0.0,
                "warning": "No verified content found matching prompt",
                "is_safe": False
            }
        
        # Build generation from verified phrases
        generated_words = prompt.split()
        context = prompt
        
        for _ in range(max_length):
            # Find next verified phrase that matches context
            context_embedding = self.kernel.embed(context)
            
            best_phrase = None
            best_similarity = 0.0
            
            for phrase, phrase_similarity in candidate_phrases:
                phrase_embedding = self.source_embeddings[phrase]
                context_sim = float(np.abs(np.dot(context_embedding, phrase_embedding)))
                
                # Combined score: phrase relevance + context match
                combined_score = (phrase_similarity * 0.4) + (context_sim * 0.6)
                
                if combined_score > best_similarity and combined_score >= self.confidence_threshold:
                    # Check if phrase words would continue naturally
                    phrase_words = phrase.split()
                    if len(generated_words) > 0:
                        last_words = " ".join(generated_words[-2:]).lower()
                        if phrase.startswith(last_words) or context_sim > 0.7:
                            best_phrase = phrase
                            best_similarity = combined_score
            
            if best_phrase:
                # Add words from phrase that aren't already in context
                phrase_words = best_phrase.split()
                context_words = context.lower().split()
                
                for word in phrase_words:
                    if word not in context_words[-3:]:  # Don't repeat recent words
                        generated_words.append(word)
                        break  # Add one word at a time
                
                context = " ".join(generated_words[-5:])  # Update context
            else:
                break  # No more verified content
        
        generated_text = " ".join(generated_words)
        
        # Validate generated text
        validation = self.validate_against_sources(generated_text)
        
        # If validation fails and required, return warning
        if require_validation and not validation["is_safe"]:
            return {
                "generated": generated_text,
                "confidence": validation["confidence"],
                "validation": validation,
                "warning": "Generated text has low confidence or potential issues",
                "is_safe": False
            }
        
        return {
            "generated": generated_text,
            "confidence": validation["confidence"],
            "validation": validation,
            "is_safe": validation["is_safe"],
            "sources": self.phrase_sources.get(generated_text[:50], [])[:3]  # Top 3 sources
        }
    
    def generate_with_fallback(self, prompt: str, max_length: int = 50) -> Dict:
        """
        Generate with fallback: if grounded generation fails, return best matching source
        """
        result = self.generate_grounded(prompt, max_length, require_validation=False)
        
        if not result["is_safe"] or result["confidence"] < self.confidence_threshold:
            # Fallback: return most similar source text
            prompt_embedding = self.kernel.embed(prompt)
            best_source = None
            best_similarity = 0.0
            
            for source_text in self.source_texts:
                source_embedding = self.kernel.embed(source_text)
                similarity = float(np.abs(np.dot(prompt_embedding, source_embedding)))
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_source = source_text
            
            if best_source and best_similarity > 0.5:
                return {
                    "generated": best_source[:200],  # First 200 chars
                    "confidence": best_similarity,
                    "method": "fallback_to_source",
                    "is_safe": True,
                    "validation": {"confidence": 1.0, "is_safe": True}
                }
        
        return result
    
    def detect_bias(self, text: str) -> Dict:
        """
        Detect potential bias in text
        Checks for one-sided language, missing perspectives, etc.
        """
        # Simple bias detection: check for balanced language
        bias_indicators = {
            "absolute_claims": len(re.findall(r'\b(always|never|all|none|every)\b', text.lower())),
            "emotional_language": len(re.findall(r'\b(amazing|terrible|awful|perfect|horrible)\b', text.lower())),
            "exclusive_language": len(re.findall(r'\b(only|solely|exclusively)\b', text.lower())),
        }
        
        # Check for diverse perspectives (if multiple sources available)
        source_diversity = len(set(self.phrase_sources.get(text[:50], [])))
        
        issues = []
        if bias_indicators["absolute_claims"] > 3:
            issues.append("too_many_absolute_claims")
        if bias_indicators["emotional_language"] > 5:
            issues.append("excessive_emotional_language")
        if bias_indicators["exclusive_language"] > 2:
            issues.append("exclusive_language_detected")
        if source_diversity < 2 and len(self.source_texts) > 5:
            issues.append("low_source_diversity")
        
        return {
            "bias_score": sum(bias_indicators.values()) / max(len(text.split()), 1),
            "indicators": bias_indicators,
            "source_diversity": source_diversity,
            "issues": issues,
            "has_bias": len(issues) > 0
        }
    
    def get_statistics(self) -> Dict:
        """Get statistics about the grounded generator"""
        return {
            "source_texts": len(self.source_texts),
            "verified_phrases": len(self.verified_phrases),
            "phrase_sources": len(self.phrase_sources),
            "confidence_threshold": self.confidence_threshold,
            "average_phrases_per_source": len(self.verified_phrases) / max(len(self.source_texts), 1)
        }


def demonstrate_grounded_generation():
    """Demonstrate grounded quantum generation"""
    print("=" * 80)
    print("GROUNDED QUANTUM TEXT GENERATION")
    print("=" * 80)
    
    # Sample Bible verses and commentaries (verified sources)
    source_texts = [
        "God is love and love is patient and kind",
        "Faith is the assurance of things hoped for, the conviction of things not seen",
        "By grace you have been saved through faith, and this is not your own doing",
        "The Lord is my shepherd, I shall not want",
        "In the beginning was the Word, and the Word was with God",
        "Love is patient, love is kind. It does not envy, it does not boast",
        "For God so loved the world that he gave his only Son",
        "Blessed are the peacemakers, for they will be called children of God",
        "Jesus said, I am the way, and the truth, and the life",
        "The Word became flesh and dwelt among us"
    ]
    
    # Create grounded generator
    generator = GroundedQuantumGenerator(source_texts=source_texts)
    
    print(f"\nStatistics:")
    stats = generator.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test generation
    print("\n" + "=" * 80)
    print("TEST 1: Grounded Generation")
    print("=" * 80)
    prompt = "God is"
    result = generator.generate_grounded(prompt, max_length=20)
    print(f"Prompt: '{prompt}'")
    print(f"Generated: '{result['generated']}'")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Safe: {result['is_safe']}")
    if result.get('validation'):
        print(f"Verified Ratio: {result['validation']['verified_ratio']:.2f}")
    
    # Test validation
    print("\n" + "=" * 80)
    print("TEST 2: Validation")
    print("=" * 80)
    test_text = "God is love and love is patient"
    validation = generator.validate_against_sources(test_text)
    print(f"Text: '{test_text}'")
    print(f"Confidence: {validation['confidence']:.2f}")
    print(f"Verified Ratio: {validation['verified_ratio']:.2f}")
    print(f"Safe: {validation['is_safe']}")
    if validation['issues']:
        print(f"Issues: {validation['issues']}")
    
    # Test with unverified content (should detect)
    print("\n" + "=" * 80)
    print("TEST 3: Hallucination Detection")
    print("=" * 80)
    unverified_text = "God is a purple elephant who flies through space"
    validation = generator.validate_against_sources(unverified_text)
    print(f"Text: '{unverified_text}'")
    print(f"Confidence: {validation['confidence']:.2f}")
    print(f"Safe: {validation['is_safe']}")
    print(f"Issues: {validation['issues']}")
    if validation['unverified_phrases']:
        print(f"Unverified Phrases: {validation['unverified_phrases'][:3]}")
    
    # Test bias detection
    print("\n" + "=" * 80)
    print("TEST 4: Bias Detection")
    print("=" * 80)
    biased_text = "God is always perfect and never makes mistakes and everyone must believe this"
    bias = generator.detect_bias(biased_text)
    print(f"Text: '{biased_text}'")
    print(f"Bias Score: {bias['bias_score']:.2f}")
    print(f"Has Bias: {bias['has_bias']}")
    print(f"Issues: {bias['issues']}")
    
    # Test fallback
    print("\n" + "=" * 80)
    print("TEST 5: Fallback to Source")
    print("=" * 80)
    prompt2 = "Tell me about salvation"
    result = generator.generate_with_fallback(prompt2, max_length=30)
    print(f"Prompt: '{prompt2}'")
    print(f"Generated: '{result['generated']}'")
    print(f"Method: {result.get('method', 'grounded')}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Safe: {result['is_safe']}")


if __name__ == "__main__":
    demonstrate_grounded_generation()
