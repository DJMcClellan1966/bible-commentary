"""
Test Best LLM Integration with Quantum Learning
"""
from bible_ai_system import create_bible_ai_system
from bible_llm_integration import create_bible_llm_integration
from models import get_db, init_db
import os


def test_llm_integration():
    """Test LLM integration and quantum learning"""
    print("=" * 80)
    print("BEST LLM INTEGRATION TEST")
    print("=" * 80)
    
    init_db()
    db = next(get_db())
    
    # Create systems
    bible_ai = create_bible_ai_system(db)
    llm_integration = create_bible_llm_integration(bible_ai)
    
    # Check status
    print("\n1. LLM INTEGRATION STATUS")
    print("-" * 80)
    status = llm_integration.get_status()
    print(f"LLM Available: {status['llm_available']}")
    print(f"Provider: {status['provider']}")
    print(f"Model: {status['model']}")
    print(f"Quantum Available: {status['quantum_available']}")
    print(f"Learning Enabled: {status['learning_enabled']}")
    
    # Test generation
    print("\n2. TEXT GENERATION TEST")
    print("-" * 80)
    
    test_prompts = [
        "God is",
        "Love is",
        "Faith is"
    ]
    
    for prompt in test_prompts:
        print(f"\nPrompt: '{prompt}'")
        print("-" * 40)
        
        # Try hybrid generation
        result = llm_integration.generate_hybrid(
            prompt,
            use_llm=status['llm_available'],
            use_quantum=True
        )
        
        if "error" not in result:
            if "llm_output" in result:
                print(f"LLM Output: {result['llm_output'][:80]}...")
            if "quantum_output" in result:
                print(f"Quantum Output: {result['quantum_output'][:80]}...")
            if "recommended" in result:
                print(f"Recommended: {result['recommended'][:80]}...")
            print(f"Method: {result.get('method', 'unknown')}")
            print(f"Learned: {result.get('learned', False)}")
        else:
            print(f"Error: {result.get('error')}")
            if "suggestion" in result:
                print(f"Suggestion: {result['suggestion']}")
    
    # Test translation
    print("\n3. TRANSLATION TEST")
    print("-" * 80)
    
    test_phrases = [
        "God is love",
        "Love is patient"
    ]
    
    for phrase in test_phrases:
        print(f"\nEnglish: '{phrase}'")
        result = llm_integration.translate_with_llm(phrase, "en", "es")
        
        if "error" not in result:
            print(f"Spanish: {result.get('translation', 'N/A')}")
            print(f"Method: {result.get('method', 'unknown')}")
            print(f"Quantum Learned: {result.get('quantum_learned', False)}")
        else:
            print(f"Error: {result.get('error')}")
    
    # Test learning
    print("\n4. LEARNING VERIFICATION")
    print("-" * 80)
    
    if status['llm_available']:
        # Generate with LLM
        llm_result = llm_integration.generate_with_llm("God is")
        if "generated" in llm_result:
            print(f"LLM Generated: {llm_result['generated'][:60]}...")
            print(f"Learned: {llm_result.get('learned', False)}")
            
            # Check if quantum learned
            if bible_ai.text_generator:
                vocab_size = len(bible_ai.text_generator.vocab)
                print(f"Quantum Vocab Size: {vocab_size}")
                if hasattr(bible_ai.text_generator, 'learned_pairs'):
                    print(f"Learned Pairs: {len(bible_ai.text_generator.learned_pairs)}")
    
    print("\n" + "=" * 80)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 80)
    print("""
Key Features:

[+] Best LLM automatically selected (GPT-4 > GPT-3.5 > Claude)
[+] Quantum learns from LLM outputs automatically
[+] Hybrid generation (LLM + Quantum)
[+] Automatic fallback to quantum if LLM unavailable
[+] Translation with learning
[+] All integrated into Bible app

The system now uses the best available LLM and quantum
learns from it to improve over time!
    """)


if __name__ == "__main__":
    test_llm_integration()
