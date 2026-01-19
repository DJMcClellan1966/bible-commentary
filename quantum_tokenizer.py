"""
Quantum-Inspired Tokenizer for LLM Training
A quantum computing approach to text tokenization using quantum superposition states
"""
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import Counter, defaultdict
import hashlib
import json
from dataclasses import dataclass
from scipy.sparse import csr_matrix
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class QuantumToken:
    """Represents a token in quantum superposition state"""
    text: str
    amplitude: complex  # Quantum amplitude
    frequency: int
    embeddings: Optional[np.ndarray] = None
    quantum_state: Optional[np.ndarray] = None


class QuantumTokenizer:
    """
    Quantum-inspired tokenizer that uses quantum superposition principles
    to represent tokens in multiple states simultaneously
    """
    
    def __init__(self, vocab_size: int = 50000, dimension: int = 512):
        self.vocab_size = vocab_size
        self.dimension = dimension
        self.vocab: Dict[str, QuantumToken] = {}
        self.token_to_id: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}
        self.quantum_states: np.ndarray = None
        self.entanglement_matrix: Optional[np.ndarray] = None
        
    def _quantum_hash(self, text: str) -> int:
        """Create a quantum-inspired hash for token representation"""
        # Use quantum-like hashing with multiple hash functions
        hash1 = int(hashlib.md5(text.encode()).hexdigest(), 16)
        hash2 = int(hashlib.sha256(text.encode()).hexdigest(), 16)
        # Combine in quantum superposition
        return (hash1 ^ hash2) % self.vocab_size
    
    def _create_quantum_state(self, token: str, frequency: int) -> np.ndarray:
        """Create a quantum state vector for a token"""
        # Initialize quantum state in superposition
        state = np.zeros(self.dimension, dtype=complex)
        
        # Use frequency to determine amplitude
        amplitude = np.sqrt(frequency) / np.sqrt(frequency + 1)
        
        # Create superposition of basis states
        for i in range(min(self.dimension, len(token) * 10)):
            idx = (hash(token) + i) % self.dimension
            phase = 2 * np.pi * i / self.dimension
            state[idx] = amplitude * np.exp(1j * phase)
        
        # Normalize quantum state
        norm = np.linalg.norm(state)
        if norm > 0:
            state = state / norm
        
        return state
    
    def _build_entanglement_matrix(self):
        """Build quantum entanglement matrix between tokens"""
        n = len(self.vocab)
        if n == 0:
            return None
        
        entanglement = np.zeros((n, n), dtype=complex)
        
        for i, (token1, qt1) in enumerate(self.vocab.items()):
            for j, (token2, qt2) in enumerate(self.vocab.items()):
                if i == j:
                    entanglement[i, j] = 1.0  # Self-entanglement
                else:
                    # Calculate quantum entanglement based on co-occurrence
                    # This is a simplified model
                    overlap = np.abs(np.vdot(qt1.quantum_state, qt2.quantum_state))
                    entanglement[i, j] = overlap
        
        return entanglement
    
    def train(self, texts: List[str], min_frequency: int = 2):
        """Train the quantum tokenizer on a corpus"""
        logger.info(f"Training quantum tokenizer on {len(texts)} texts...")
        
        # Count token frequencies
        token_counts = Counter()
        for text in texts:
            # Simple tokenization (can be enhanced with BPE, WordPiece, etc.)
            tokens = self._simple_tokenize(text)
            token_counts.update(tokens)
        
        # Filter by minimum frequency
        filtered_tokens = {
            token: count for token, count in token_counts.items()
            if count >= min_frequency
        }
        
        # Sort by frequency and take top vocab_size
        sorted_tokens = sorted(
            filtered_tokens.items(),
            key=lambda x: x[1],
            reverse=True
        )[:self.vocab_size]
        
        # Build vocabulary with quantum states
        for idx, (token, frequency) in enumerate(sorted_tokens):
            quantum_state = self._create_quantum_state(token, frequency)
            amplitude = np.sqrt(frequency) / np.sqrt(sum(t[1] for t in sorted_tokens))
            
            self.vocab[token] = QuantumToken(
                text=token,
                amplitude=amplitude,
                frequency=frequency,
                quantum_state=quantum_state
            )
            self.token_to_id[token] = idx
            self.id_to_token[idx] = token
        
        # Build entanglement matrix
        logger.info("Building quantum entanglement matrix...")
        self.entanglement_matrix = self._build_entanglement_matrix()
        
        logger.info(f"Vocabulary built with {len(self.vocab)} tokens")
        return self
    
    def _simple_tokenize(self, text: str) -> List[str]:
        """Simple tokenization (can be replaced with more sophisticated methods)"""
        # Basic tokenization - split on whitespace and punctuation
        import re
        # Keep words and basic punctuation
        tokens = re.findall(r'\b\w+\b|[.,!?;:]', text.lower())
        return tokens
    
    def encode(self, text: str) -> List[int]:
        """Encode text into token IDs using quantum superposition"""
        tokens = self._simple_tokenize(text)
        token_ids = []
        
        for token in tokens:
            if token in self.token_to_id:
                token_ids.append(self.token_to_id[token])
            else:
                # Handle unknown tokens with quantum superposition of similar tokens
                # Find most similar token using quantum state overlap
                if len(self.vocab) > 0:
                    unknown_state = self._create_quantum_state(token, 1)
                    best_match = max(
                        self.vocab.items(),
                        key=lambda x: np.abs(np.vdot(unknown_state, x[1].quantum_state))
                    )
                    token_ids.append(self.token_to_id[best_match[0]])
                else:
                    # Fallback: use hash-based ID
                    token_ids.append(self._quantum_hash(token) % len(self.vocab) if self.vocab else 0)
        
        return token_ids
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs back to text"""
        tokens = [self.id_to_token.get(id, "<UNK>") for id in token_ids]
        return " ".join(tokens)
    
    def get_quantum_embedding(self, token: str) -> Optional[np.ndarray]:
        """Get quantum state embedding for a token"""
        if token in self.vocab:
            return self.vocab[token].quantum_state
        return None
    
    def measure_token(self, token: str, basis: Optional[np.ndarray] = None) -> Dict:
        """Measure a token in a quantum basis (quantum measurement)"""
        if token not in self.vocab:
            return {"probability": 0.0, "state": None}
        
        qt = self.vocab[token]
        
        if basis is None:
            # Measure in computational basis
            probability = np.abs(qt.amplitude) ** 2
        else:
            # Measure in custom basis
            projection = np.vdot(basis, qt.quantum_state)
            probability = np.abs(projection) ** 2
        
        return {
            "token": token,
            "probability": float(probability),
            "amplitude": complex(qt.amplitude),
            "frequency": qt.frequency,
            "quantum_state": qt.quantum_state
        }
    
    def get_entangled_tokens(self, token: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Get tokens that are quantum-entangled with the given token"""
        if token not in self.token_to_id or self.entanglement_matrix is None:
            return []
        
        token_id = self.token_to_id[token]
        entanglements = self.entanglement_matrix[token_id, :]
        
        # Get top-k most entangled tokens
        top_indices = np.argsort(np.abs(entanglements))[-top_k-1:-1][::-1]
        
        results = []
        for idx in top_indices:
            if idx != token_id:
                entangled_token = self.id_to_token[idx]
                entanglement_strength = float(np.abs(entanglements[idx]))
                results.append((entangled_token, entanglement_strength))
        
        return results
    
    def save(self, filepath: str):
        """Save tokenizer to disk"""
        # Helper function to convert complex arrays to JSON-serializable format
        def convert_complex_array(arr):
            if arr is None:
                return None
            if isinstance(arr, np.ndarray):
                if np.iscomplexobj(arr):
                    return {
                        "real": arr.real.tolist(),
                        "imag": arr.imag.tolist(),
                        "dtype": "complex"
                    }
                else:
                    return arr.tolist()
            return arr
        
        data = {
            "vocab_size": self.vocab_size,
            "dimension": self.dimension,
            "vocab": {}
        }
        
        # Build vocab dictionary with proper complex number handling
        for token, qt in self.vocab.items():
            data["vocab"][token] = {
                "text": qt.text,
                "amplitude_real": float(qt.amplitude.real),
                "amplitude_imag": float(qt.amplitude.imag),
                "frequency": qt.frequency,
                "quantum_state": convert_complex_array(qt.quantum_state),
                "embeddings": convert_complex_array(qt.embeddings) if qt.embeddings is not None else None
            }
        
        data["token_to_id"] = self.token_to_id
        data["id_to_token"] = {str(k): v for k, v in self.id_to_token.items()}  # Ensure keys are strings
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Save entanglement matrix separately (can be large)
        if self.entanglement_matrix is not None:
            np.save(filepath.replace('.json', '_entanglement.npy'), self.entanglement_matrix)
        
        logger.info(f"Tokenizer saved to {filepath}")
    
    def load(self, filepath: str):
        """Load tokenizer from disk"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.vocab_size = data["vocab_size"]
        self.dimension = data["dimension"]
        
        self.vocab = {}
        for token, qt_data in data["vocab"].items():
            quantum_state = None
            if qt_data.get("quantum_state_real") is not None:
                real_part = np.array(qt_data["quantum_state_real"])
                imag_part = np.array(qt_data.get("quantum_state_imag", [0] * len(real_part)))
                quantum_state = real_part + 1j * imag_part
            
            amplitude = complex(
                qt_data.get("amplitude_real", qt_data.get("amplitude", "0+0j").split('+')[0] if isinstance(qt_data.get("amplitude"), str) else 0),
                qt_data.get("amplitude_imag", 0)
            )
            
            self.vocab[token] = QuantumToken(
                text=qt_data["text"],
                amplitude=amplitude,
                frequency=qt_data["frequency"],
                quantum_state=quantum_state
            )
        
        self.token_to_id = {k: int(v) for k, v in data["token_to_id"].items()}
        self.id_to_token = {int(k): v for k, v in data["id_to_token"].items()}
        
        # Load entanglement matrix if exists
        entanglement_file = filepath.replace('.json', '_entanglement.npy')
        try:
            self.entanglement_matrix = np.load(entanglement_file)
        except FileNotFoundError:
            logger.warning("Entanglement matrix not found, rebuilding...")
            self.entanglement_matrix = self._build_entanglement_matrix()
        
        logger.info(f"Tokenizer loaded from {filepath}")
