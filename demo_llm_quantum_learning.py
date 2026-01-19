"""
Demo: Best LLM + Quantum Learning
Shows how the system works with and without LLM
"""
from bible_ai_system import create_bible_ai_system
from bible_llm_integration import create_bible_llm_integration
from models import get_db, init_db
import os


def demo_with_llm():
    """Demo with LLM available"""
    print("=" * 80)
    print("DEMO: BEST LLM + QUANTUM LEARNING (With LLM)")
    print("=" * 80)
    
    init_db()
    db = next(get_db())
    
    bible_ai = create_bible_ai_system(db)
    llm_integration = create_bible_llm_integration(bible_ai)
    
    status = llm_integration.get_status()
    
    print(f"\nLLM Status:")
    print(f"  Available: {status['llm_available']}")
    print(f"  Provider: {status['provider']}")
    print(f"  Model: {status['model']}")
    
    if status['llm_available']:
        print("\n1. GENERATING WITH LLM (Quantum Learns Automatically)")
        print("-" * 80)
        
        prompt = "God is"
        result = llm_integration.generate_with_llm(prompt, context="Bible study")
        
        if "error" not in result:
            print(f"Prompt: '{prompt}'")
            print(f"LLM Output: {result['generated'][:100]}...")
            print(f"Provider: {result['provider']}")
            print(f"Model: {result['model']}")
            print(f"Learned by Quantum: {result.get('learned', False)}")
            
            # Check quantum improvement
            if bible_ai.text_generator:
                vocab_size = len(bible_ai.text_generator.vocab)
                print(f"\nQuantum Vocabulary: {vocab_size} words")
                if hasattr(bible_ai.text_generator, 'learned_pairs'):
                    print(f"Learned Pairs: {len(bible_ai.text_generator.learned_pairs)}")
        
        print("\n2. HYBRID GENERATION (LLM + Quantum)")
        print("-" * 80)
        
        result = llm_integration.generate_hybrid("Love is", use_llm=True, use_quantum=True)
        
        if "llm_output" in result:
            print(f"LLM Output: {result['llm_output'][:80]}...")
        if "quantum_output" in result:
            print(f"Quantum Output: {result['quantum_output'][:80]}...")
        print(f"Recommended: {result.get('recommended', '')[:80]}...")
        
        print("\n3. TRANSLATION WITH LLM (Quantum Learns)")
        print("-" * 80)
        
        result = llm_integration.translate_with_llm("God is love", "en", "es")
        
        if "error" not in result:
            print(f"English: 'God is love'")
            print(f"Spanish: {result['translation']}")
            print(f"Quantum Learned: {result.get('quantum_learned', False)}")
    else:
        print("\n[INFO] No LLM available. Using quantum-only mode.")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY to enable LLM.")


def demo_quantum_only():
    """Demo without LLM (quantum-only)"""
    print("\n" + "=" * 80)
    print("DEMO: QUANTUM-ONLY MODE (No LLM)")
    print("=" * 80)
    
    init_db()
    db = next(get_db())
    
    bible_ai = create_bible_ai_system(db)
    llm_integration = create_bible_llm_integration(bible_ai)
    
    status = llm_integration.get_status()
    
    print(f"\nStatus:")
    print(f"  LLM Available: {status['llm_available']}")
    print(f"  Quantum Available: {status['quantum_available']}")
    
    if not status['llm_available']:
        print("\n1. QUANTUM GENERATION (Works Without LLM)")
        print("-" * 80)
        
        result = bible_ai.generate_text("God is", max_length=15)
        
        if "error" not in result:
            print(f"Prompt: 'God is'")
            print(f"Generated: {result['generated'][:80]}...")
            print(f"Method: {result['method']}")
        
        print("\n2. QUANTUM TRANSLATION (Works Without LLM)")
        print("-" * 80)
        
        # Learn some pairs first
        if bible_ai.translator:
            bible_ai.translator.learn_from_examples([
                ("God is love", "Dios es amor", "en", "es"),
                ("Love is patient", "El amor es paciente", "en", "es")
            ])
        
        result = bible_ai.translate_text("God is love", "en", "es")
        
        if "error" not in result:
            print(f"English: 'God is love'")
            print(f"Spanish: {result['translation']}")
            print(f"Method: {result['method']}")
        
        print("\n[OK] Quantum works completely without LLM!")
        print("     Fast, private, free, and offline!")


def main():
    """Run demos"""
    print("\n" + "=" * 80)
    print("BEST LLM + QUANTUM LEARNING DEMONSTRATION")
    print("=" * 80)
    print("\nThis demonstrates:")
    print("  - Automatic LLM selection (GPT-4 > GPT-3.5 > Claude)")
    print("  - Quantum learning from LLM outputs")
    print("  - Hybrid generation (LLM + Quantum)")
    print("  - Smart fallback (quantum-only if no LLM)")
    
    # Demo with/without LLM
    demo_with_llm()
    demo_quantum_only()
    
    print("\n" + "=" * 80)
    print("SETUP INSTRUCTIONS")
    print("=" * 80)
    print("""
To enable LLM:

1. Get API Key:
   - OpenAI: https://platform.openai.com/
   - Anthropic: https://console.anthropic.com/

2. Set Environment Variable:
   Windows: $env:OPENAI_API_KEY="your-key"
   Linux/Mac: export OPENAI_API_KEY="your-key"

3. Or create .env file:
   OPENAI_API_KEY=your-key-here

4. Restart the app

The system will automatically:
- Select best available LLM
- Use it for generation
- Let quantum learn from outputs
- Fallback to quantum if LLM unavailable

Best of both worlds!
    """)


if __name__ == "__main__":
    main()
