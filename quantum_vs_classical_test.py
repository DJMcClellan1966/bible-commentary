"""
Comparison Test: Quantum-Inspired vs Classical Tokenizer & LLM
"""
import time
import numpy as np
import torch
import torch.nn as nn
from quantum_tokenizer import QuantumTokenizer
from quantum_llm import QuantumLLM, QuantumLLMTrainer
from typing import List, Dict, Optional
import json

# Classical tokenizer (simple implementation)
class ClassicalTokenizer:
    """Standard classical tokenizer for comparison"""
    
    def __init__(self, vocab_size: int = 50000):
        self.vocab_size = vocab_size
        self.vocab: Dict[str, int] = {}
        self.id_to_token: Dict[int, str] = {}
        self.token_to_id: Dict[str, int] = {}
        self.token_counts: Dict[str, int] = {}
        
    def train(self, texts: List[str], min_frequency: int = 2):
        """Train classical tokenizer"""
        from collections import Counter
        import re
        
        token_counts = Counter()
        for text in texts:
            tokens = re.findall(r'\b\w+\b|[.,!?;:]', text.lower())
            token_counts.update(tokens)
        
        filtered_tokens = {
            token: count for token, count in token_counts.items()
            if count >= min_frequency
        }
        
        sorted_tokens = sorted(
            filtered_tokens.items(),
            key=lambda x: x[1],
            reverse=True
        )[:self.vocab_size]
        
        for idx, (token, count) in enumerate(sorted_tokens):
            self.vocab[token] = idx
            self.token_to_id[token] = idx
            self.id_to_token[idx] = token
            self.token_counts[token] = count
        
        return self
    
    def encode(self, text: str) -> List[int]:
        """Encode text to token IDs"""
        import re
        tokens = re.findall(r'\b\w+\b|[.,!?;:]', text.lower())
        return [self.token_to_id.get(token, 0) for token in tokens]
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs to text"""
        tokens = [self.id_to_token.get(id, "<UNK>") for id in token_ids]
        return " ".join(tokens)


# Classical LLM (standard transformer)
class ClassicalLLM(nn.Module):
    """Standard classical transformer LLM"""
    
    def __init__(
        self,
        vocab_size: int,
        d_model: int = 512,
        n_heads: int = 8,
        n_layers: int = 6,
        d_ff: int = 2048,
        max_seq_length: int = 512,
        dropout: float = 0.1
    ):
        super().__init__()
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.max_seq_length = max_seq_length
        
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_seq_length, d_model)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=d_ff,
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        
        self.output_norm = nn.LayerNorm(d_model)
        self.output_projection = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)
        
        # Standard initialization
        self._init_weights()
    
    def _init_weights(self):
        """Standard weight initialization"""
        for param in self.parameters():
            if param.dim() > 1:
                nn.init.xavier_uniform_(param)
    
    def forward(self, input_ids: torch.Tensor, mask: Optional[torch.Tensor] = None):
        batch_size, seq_length = input_ids.shape
        
        positions = torch.arange(0, seq_length, device=input_ids.device).unsqueeze(0)
        
        token_embeds = self.token_embedding(input_ids)
        pos_embeds = self.position_embedding(positions)
        x = self.dropout(token_embeds + pos_embeds)
        
        x = self.transformer(x, src_key_padding_mask=mask)
        
        x = self.output_norm(x)
        logits = self.output_projection(x)
        
        return logits
    
    def generate(
        self,
        tokenizer,
        prompt: str,
        max_length: int = 100,
        temperature: float = 1.0,
        top_k: int = 50,
        top_p: float = 0.9
    ) -> str:
        """Generate text"""
        self.eval()
        
        input_ids = tokenizer.encode(prompt)
        input_tensor = torch.tensor([input_ids], dtype=torch.long)
        
        generated = input_ids.copy()
        
        with torch.no_grad():
            for _ in range(max_length - len(input_ids)):
                logits = self.forward(input_tensor)[0, -1, :]
                logits = logits / temperature
                
                if top_k > 0:
                    indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
                    logits[indices_to_remove] = float('-inf')
                
                if top_p < 1.0:
                    sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                    cumulative_probs = torch.cumsum(torch.softmax(sorted_logits, dim=-1), dim=-1)
                    sorted_indices_to_remove = cumulative_probs > top_p
                    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
                    sorted_indices_to_remove[..., 0] = 0
                    indices_to_remove = sorted_indices_to_remove.scatter(0, sorted_indices, sorted_indices_to_remove)
                    logits[indices_to_remove] = float('-inf')
                
                probs = torch.softmax(logits, dim=-1)
                next_token_id = torch.multinomial(probs, 1).item()
                
                generated.append(next_token_id)
                input_tensor = torch.tensor([generated[-self.max_seq_length:]], dtype=torch.long)
        
        return tokenizer.decode(generated)


class ClassicalLLMTrainer:
    """Trainer for classical LLM"""
    
    def __init__(self, model: ClassicalLLM, tokenizer: ClassicalTokenizer, learning_rate: float = 1e-4):
        self.model = model
        self.tokenizer = tokenizer
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        self.criterion = nn.CrossEntropyLoss(ignore_index=-1)
    
    def train_step(self, batch_texts: List[str]) -> float:
        """Training step"""
        self.model.train()
        self.optimizer.zero_grad()
        
        batch_token_ids = [self.tokenizer.encode(text) for text in batch_texts]
        
        inputs = []
        targets = []
        
        for token_ids in batch_token_ids:
            if len(token_ids) > 1:
                inputs.append(token_ids[:-1])
                targets.append(token_ids[1:])
        
        if not inputs:
            return 0.0
        
        max_len = max(len(seq) for seq in inputs)
        padded_inputs = []
        padded_targets = []
        
        for inp, tgt in zip(inputs, targets):
            padded_inputs.append(inp + [0] * (max_len - len(inp)))
            padded_targets.append(tgt + [-1] * (max_len - len(tgt)))
        
        input_tensor = torch.tensor(padded_inputs, dtype=torch.long)
        target_tensor = torch.tensor(padded_targets, dtype=torch.long)
        
        logits = self.model(input_tensor)
        logits = logits.view(-1, self.model.vocab_size)
        targets = target_tensor.view(-1)
        
        loss = self.criterion(logits, targets)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
        self.optimizer.step()
        
        return loss.item()
    
    def train(self, texts: List[str], epochs: int = 10, batch_size: int = 32):
        """Train model"""
        for epoch in range(epochs):
            total_loss = 0.0
            num_batches = 0
            
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                loss = self.train_step(batch)
                total_loss += loss
                num_batches += 1
            
            avg_loss = total_loss / num_batches if num_batches > 0 else 0.0
            print(f"  Epoch {epoch + 1}/{epochs}, Average Loss: {avg_loss:.4f}")


def run_comparison_test():
    """Run comprehensive comparison test"""
    print("=" * 80)
    print("QUANTUM-INSPIRED vs CLASSICAL TOKENIZER & LLM COMPARISON")
    print("=" * 80)
    
    # Prepare test data
    training_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "In the beginning was the Word, and the Word was with God.",
        "Love your neighbor as yourself.",
        "Faith, hope, and love, but the greatest of these is love.",
        "For God so loved the world that he gave his one and only Son.",
        "The Lord is my shepherd, I shall not want.",
        "Be still and know that I am God.",
        "Trust in the Lord with all your heart.",
    ] * 50  # 400 texts total
    
    test_prompts = [
        "The Word",
        "Love",
        "God",
        "The Lord"
    ]
    
    results = {
        "quantum": {},
        "classical": {}
    }
    
    # ========== QUANTUM TOKENIZER ==========
    print("\n" + "=" * 80)
    print("1. QUANTUM-INSPIRED TOKENIZER")
    print("=" * 80)
    
    start_time = time.time()
    quantum_tokenizer = QuantumTokenizer(vocab_size=500, dimension=128)
    quantum_tokenizer.train(training_texts, min_frequency=2)
    quantum_time = time.time() - start_time
    
    results["quantum"]["tokenizer_time"] = quantum_time
    results["quantum"]["vocab_size"] = len(quantum_tokenizer.vocab)
    
    print(f"[OK] Training time: {quantum_time:.4f} seconds")
    print(f"[OK] Vocabulary size: {len(quantum_tokenizer.vocab)} tokens")
    
    # Test encoding/decoding
    test_text = "The Word was with God"
    encoded = quantum_tokenizer.encode(test_text)
    decoded = quantum_tokenizer.decode(encoded)
    print(f"[OK] Test: '{test_text}' -> {encoded[:5]}... -> '{decoded}'")
    
    # Test quantum features
    if "word" in quantum_tokenizer.vocab:
        measurement = quantum_tokenizer.measure_token("word")
        entangled = quantum_tokenizer.get_entangled_tokens("word", top_k=5)
        print(f"[OK] Quantum measurement for 'word': {measurement['probability']:.4f}")
        print(f"[OK] Entangled tokens: {[t[0] for t in entangled[:3]]}")
    
    # ========== CLASSICAL TOKENIZER ==========
    print("\n" + "=" * 80)
    print("2. CLASSICAL TOKENIZER")
    print("=" * 80)
    
    start_time = time.time()
    classical_tokenizer = ClassicalTokenizer(vocab_size=500)
    classical_tokenizer.train(training_texts, min_frequency=2)
    classical_time = time.time() - start_time
    
    results["classical"]["tokenizer_time"] = classical_time
    results["classical"]["vocab_size"] = len(classical_tokenizer.vocab)
    
    print(f"[OK] Training time: {classical_time:.4f} seconds")
    print(f"[OK] Vocabulary size: {len(classical_tokenizer.vocab)} tokens")
    
    # Test encoding/decoding
    encoded = classical_tokenizer.encode(test_text)
    decoded = classical_tokenizer.decode(encoded)
    print(f"[OK] Test: '{test_text}' -> {encoded[:5]}... -> '{decoded}'")
    
    # ========== QUANTUM LLM ==========
    print("\n" + "=" * 80)
    print("3. QUANTUM-INSPIRED LLM")
    print("=" * 80)
    
    vocab_size = len(quantum_tokenizer.vocab)
    quantum_model = QuantumLLM(
        vocab_size=vocab_size,
        d_model=256,
        n_heads=4,
        n_layers=3,
        d_ff=1024,
        max_seq_length=128
    )
    
    quantum_params = sum(p.numel() for p in quantum_model.parameters())
    results["quantum"]["model_params"] = quantum_params
    print(f"[OK] Model parameters: {quantum_params:,}")
    
    # Training
    print("\nTraining Quantum LLM...")
    start_time = time.time()
    quantum_trainer = QuantumLLMTrainer(quantum_model, quantum_tokenizer, learning_rate=1e-3)
    quantum_trainer.train(training_texts, epochs=5, batch_size=8)
    quantum_training_time = time.time() - start_time
    results["quantum"]["training_time"] = quantum_training_time
    print(f"[OK] Training time: {quantum_training_time:.2f} seconds")
    
    # Generation
    print("\nGenerating text with Quantum LLM...")
    quantum_generations = {}
    for prompt in test_prompts:
        start_time = time.time()
        generated = quantum_model.generate(
            quantum_tokenizer,
            prompt,
            max_length=20,
            temperature=0.8,
            top_k=10
        )
        gen_time = time.time() - start_time
        quantum_generations[prompt] = (generated, gen_time)
        print(f"  Prompt: '{prompt}'")
        print(f"  Generated: '{generated}'")
        print(f"  Time: {gen_time:.4f}s")
    
    results["quantum"]["generations"] = quantum_generations
    
    # ========== CLASSICAL LLM ==========
    print("\n" + "=" * 80)
    print("4. CLASSICAL LLM")
    print("=" * 80)
    
    vocab_size = len(classical_tokenizer.vocab)
    classical_model = ClassicalLLM(
        vocab_size=vocab_size,
        d_model=256,
        n_heads=4,
        n_layers=3,
        d_ff=1024,
        max_seq_length=128
    )
    
    classical_params = sum(p.numel() for p in classical_model.parameters())
    results["classical"]["model_params"] = classical_params
    print(f"[OK] Model parameters: {classical_params:,}")
    
    # Training
    print("\nTraining Classical LLM...")
    start_time = time.time()
    classical_trainer = ClassicalLLMTrainer(classical_model, classical_tokenizer, learning_rate=1e-3)
    classical_trainer.train(training_texts, epochs=5, batch_size=8)
    classical_training_time = time.time() - start_time
    results["classical"]["training_time"] = classical_training_time
    print(f"[OK] Training time: {classical_training_time:.2f} seconds")
    
    # Generation
    print("\nGenerating text with Classical LLM...")
    classical_generations = {}
    for prompt in test_prompts:
        start_time = time.time()
        generated = classical_model.generate(
            classical_tokenizer,
            prompt,
            max_length=20,
            temperature=0.8,
            top_k=10
        )
        gen_time = time.time() - start_time
        classical_generations[prompt] = (generated, gen_time)
        print(f"  Prompt: '{prompt}'")
        print(f"  Generated: '{generated}'")
        print(f"  Time: {gen_time:.4f}s")
    
    results["classical"]["generations"] = classical_generations
    
    # ========== COMPARISON SUMMARY ==========
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    
    print("\n[RESULTS] Tokenizer Performance:")
    print(f"  Quantum:   {results['quantum']['tokenizer_time']:.4f}s")
    print(f"  Classical: {results['classical']['tokenizer_time']:.4f}s")
    print(f"  Difference: {abs(results['quantum']['tokenizer_time'] - results['classical']['tokenizer_time']):.4f}s")
    
    print("\n[RESULTS] Model Size:")
    print(f"  Quantum:   {results['quantum']['model_params']:,} parameters")
    print(f"  Classical: {results['classical']['model_params']:,} parameters")
    print(f"  Difference: {abs(results['quantum']['model_params'] - results['classical']['model_params']):,} parameters")
    
    print("\n[RESULTS] Training Time:")
    print(f"  Quantum:   {results['quantum']['training_time']:.2f}s")
    print(f"  Classical: {results['classical']['training_time']:.2f}s")
    print(f"  Difference: {abs(results['quantum']['training_time'] - results['classical']['training_time']):.2f}s")
    
    print("\n[RESULTS] Generation Examples:")
    for prompt in test_prompts:
        print(f"\n  Prompt: '{prompt}'")
        q_gen, q_time = results['quantum']['generations'][prompt]
        c_gen, c_time = results['classical']['generations'][prompt]
        print(f"    Quantum:   '{q_gen}' ({q_time:.4f}s)")
        print(f"    Classical: '{c_gen}' ({c_time:.4f}s)")
    
    print("\n" + "=" * 80)
    print("KEY DIFFERENCES")
    print("=" * 80)
    print("""
Quantum-Inspired Approach:
  + Uses quantum superposition states for tokens
  + Implements quantum entanglement between related tokens
  + Quantum measurement for probabilistic token selection
  + Quantum amplitudes in attention mechanism
  + Can identify semantically related tokens through entanglement

Classical Approach:
  + Standard frequency-based tokenization
  + Direct token-to-ID mapping
  + Standard transformer architecture
  + Traditional attention mechanism
  + Simpler and faster for basic tasks
    """)
    
    print("=" * 80)
    print("Test Complete!")
    print("=" * 80)
    
    return results


if __name__ == "__main__":
    results = run_comparison_test()
    
    # Save results
    # Convert results to JSON-serializable format
    json_results = {
        "quantum": {
            "tokenizer_time": results["quantum"]["tokenizer_time"],
            "vocab_size": results["quantum"]["vocab_size"],
            "model_params": results["quantum"]["model_params"],
            "training_time": results["quantum"]["training_time"],
            "generations": {k: (v[0], v[1]) for k, v in results["quantum"]["generations"].items()}
        },
        "classical": {
            "tokenizer_time": results["classical"]["tokenizer_time"],
            "vocab_size": results["classical"]["vocab_size"],
            "model_params": results["classical"]["model_params"],
            "training_time": results["classical"]["training_time"],
            "generations": {k: (v[0], v[1]) for k, v in results["classical"]["generations"].items()}
        }
    }
    
    with open("comparison_results.json", "w") as f:
        json.dump(json_results, f, indent=2)
    
    print("\nResults saved to comparison_results.json")
