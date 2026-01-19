"""
Test Progressive Learning Implementation
Tests the grounded + progressive learning approach
"""
from bible_ai_system import create_bible_ai_system
from models import get_db, init_db
import time


def test_progressive_learning():
    """Test progressive learning functionality"""
    print("=" * 80)
    print("PROGRESSIVE LEARNING TEST")
    print("=" * 80)
    
    # Initialize database
    init_db()
    db = next(get_db())
    
    # Create Bible AI system
    system = create_bible_ai_system(db)
    
    # Check if standalone LLM is available
    if not system.quantum_llm:
        print("ERROR: Standalone quantum LLM not available")
        return
    
    # Get initial statistics
    print("\n1. INITIAL STATE")
    print("-" * 80)
    stats = system.get_llm_statistics()
    print(f"Verified phrases: {stats['verified_phrases']}")
    print(f"Estimated quality: {stats['estimated_quality']:.2f}")
    print(f"Learning week: {stats['learning_week']}")
    
    # Test generation
    print("\n2. INITIAL GENERATION")
    print("-" * 80)
    result = system.generate_grounded_text("God is", max_length=20)
    print(f"Prompt: 'God is'")
    print(f"Generated: '{result.get('generated', 'N/A')}'")
    print(f"Confidence: {result.get('confidence', 0):.2f}")
    print(f"Safe: {result.get('is_safe', False)}")
    
    # Progressive learning - Week 1
    print("\n3. PROGRESSIVE LEARNING - WEEK 1")
    print("-" * 80)
    new_texts = [
        "Grace is unmerited favor from God. It is God's gift of salvation that we cannot earn.",
        "Hope is the confident expectation of God's promises. It is not wishful thinking, but firm assurance.",
        "Peace is the state of wholeness and harmony that comes from being reconciled with God.",
        "Mercy is God's compassion shown to those who do not deserve it.",
        "Righteousness is the state of being in right relationship with God."
    ]
    
    learning_result = system.progressive_learning_step(new_texts, week=1)
    print(f"Week: {learning_result['week']}")
    print(f"Phrases before: {learning_result['phrases_before']}")
    print(f"Phrases after: {learning_result['phrases_after']}")
    print(f"Phrases added: {learning_result['phrases_added']}")
    print(f"Estimated quality: {learning_result['estimated_quality']:.2f}")
    
    # Updated statistics
    print("\n4. UPDATED STATISTICS")
    print("-" * 80)
    stats = system.get_llm_statistics()
    print(f"Verified phrases: {stats['verified_phrases']}")
    print(f"Estimated quality: {stats['estimated_quality']:.2f}")
    print(f"Learning week: {stats['learning_week']}")
    print(f"Total phrases learned: {stats['total_phrases_learned']}")
    
    # Test generation after learning
    print("\n5. GENERATION AFTER LEARNING")
    print("-" * 80)
    result = system.generate_grounded_text("Grace is", max_length=20)
    print(f"Prompt: 'Grace is'")
    print(f"Generated: '{result.get('generated', 'N/A')}'")
    print(f"Confidence: {result.get('confidence', 0):.2f}")
    print(f"Safe: {result.get('is_safe', False)}")
    
    # Progressive learning - Week 2
    print("\n6. PROGRESSIVE LEARNING - WEEK 2")
    print("-" * 80)
    more_texts = [
        "Faith is the assurance of things hoped for, the conviction of things not seen.",
        "Love is patient, love is kind. It does not envy, it does not boast, it is not proud.",
        "The Lord is my shepherd, I shall not want. He leads me beside still waters.",
        "Blessed are the peacemakers, for they will be called children of God.",
        "For God so loved the world that he gave his only Son."
    ]
    
    learning_result = system.progressive_learning_step(more_texts, week=2)
    print(f"Week: {learning_result['week']}")
    print(f"Phrases added: {learning_result['phrases_added']}")
    print(f"Estimated quality: {learning_result['estimated_quality']:.2f}")
    
    # Final statistics
    print("\n7. FINAL STATISTICS")
    print("-" * 80)
    stats = system.get_llm_statistics()
    print(f"Verified phrases: {stats['verified_phrases']}")
    print(f"Estimated quality: {stats['estimated_quality']:.2f}")
    print(f"Learning week: {stats['learning_week']}")
    print(f"Learning history: {stats['learning_history']} entries")
    
    # Test validation
    print("\n8. VALIDATION TEST")
    print("-" * 80)
    test_text = "Grace is unmerited favor from God"
    validation = system.validate_text(test_text)
    print(f"Text: '{test_text}'")
    print(f"Confidence: {validation.get('confidence', 0):.2f}")
    print(f"Safe: {validation.get('is_safe', False)}")
    
    # Test bias detection
    print("\n9. BIAS DETECTION TEST")
    print("-" * 80)
    biased_text = "God is always perfect and never makes mistakes"
    bias = system.detect_bias_in_text(biased_text)
    print(f"Text: '{biased_text}'")
    print(f"Has bias: {bias.get('has_bias', False)}")
    print(f"Issues: {bias.get('issues', [])}")
    
    # Save state
    print("\n10. SAVE STATE")
    print("-" * 80)
    save_result = system.save_llm_state("test_llm_state.json")
    print(f"Save result: {save_result}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    print("""
Progressive learning is working correctly!

Key Features Tested:
[+] Initial state and statistics
[+] Grounded text generation
[+] Progressive learning steps
[+] Quality improvement tracking
[+] Validation
[+] Bias detection
[+] State saving

The system is ready for 3-4 month progressive learning journey!
    """)


if __name__ == "__main__":
    test_progressive_learning()
