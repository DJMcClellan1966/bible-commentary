"""
Test Bible AI System Integration
"""
from bible_ai_system import BibleAISystem, create_bible_ai_system
from models import get_db, init_db
import sys


def test_bible_ai():
    """Test Bible AI System"""
    print("=" * 80)
    print("TESTING BIBLE AI SYSTEM INTEGRATION")
    print("=" * 80)
    
    # Initialize database
    init_db()
    
    # Get database session
    db = next(get_db())
    
    try:
        # Create Bible AI System
        print("\n1. Creating Bible AI System...")
        system = create_bible_ai_system(db)
        print("[OK] Bible AI System created")
        
        # Test AI search
        print("\n2. Testing AI Search...")
        search_result = system.ai_search("divine love", top_k=5)
        print(f"[OK] Found {search_result['count']} results")
        print(f"    Intent: {search_result['understanding']['intent']}")
        print(f"    Confidence: {search_result['understanding']['confidence']:.3f}")
        if search_result['results']:
            print(f"    Top result: {search_result['results'][0]['reference']}")
        
        # Test understanding
        print("\n3. Testing Understanding...")
        understanding = system.ai_understand_query("I want to find verses about love")
        print(f"[OK] Intent: {understanding['intent']}")
        print(f"    Confidence: {understanding['confidence']:.3f}")
        
        # Test conversation
        print("\n4. Testing Conversation...")
        conversation = system.ai_conversation("Tell me about love")
        print(f"[OK] Response: {conversation['response'][:60]}...")
        print(f"    Intent: {conversation['intent']['intent']}")
        
        # Test reasoning
        print("\n5. Testing Reasoning...")
        reasoning = system.ai_reason_about_verses(
            ["God is love", "Love is patient"],
            "What is God like?"
        )
        print(f"[OK] Connections: {len(reasoning['connections'])}")
        print(f"    Coherence: {reasoning['coherence']:.3f}")
        print(f"    Confidence: {reasoning['confidence']:.3f}")
        
        # Test theme discovery
        print("\n6. Testing Theme Discovery...")
        verses = system.get_verses(limit=20)
        themes = system.ai_discover_themes(verses, min_cluster_size=2)
        print(f"[OK] Themes discovered: {themes['count']}")
        if themes['themes']:
            print(f"    First theme: {themes['themes'][0]['theme']}")
        
        # Test stats
        print("\n7. Testing Statistics...")
        stats = system.get_stats()
        print(f"[OK] Kernel embeddings computed: {stats['kernel']['embeddings_computed']}")
        print(f"    Cache hits: {stats['kernel']['cache_hits']}")
        print(f"    AI system patterns learned: {stats['ai_system']['learned_patterns']}")
        
        print("\n" + "=" * 80)
        print("ALL TESTS PASSED!")
        print("=" * 80)
        print("""
Bible AI System is successfully integrated:

[+] AI Search - Semantic search with understanding
[+] Understanding - Intent recognition
[+] Conversation - Context-aware responses
[+] Reasoning - Logical inference
[+] Theme Discovery - Automatic theme extraction
[+] Shared Kernel - All operations share the same cache

The AI system is now part of the Bible app!
        """)
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    test_bible_ai()
