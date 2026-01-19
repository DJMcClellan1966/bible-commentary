"""
Demo: Interact with Bible Character Models
"""
from bible_characters import get_bible_characters
import time

def main():
    print("=" * 80)
    print("BIBLE CHARACTER MODELS DEMO")
    print("=" * 80)
    print("\nAvailable Characters:")
    print("  - Moses (Law, Authority, Teaching)")
    print("  - David (Worship, Poetry, Passion)")
    print("  - Solomon (Wisdom, Reflection, Practicality)")
    print("  - Paul (Theology, Grace, Encouragement)")
    print("  - John (Love, Intimacy, Revelation)")
    print("\n" + "=" * 80)
    
    system = get_bible_characters()
    
    print("\nInitializing character models...")
    print("This may take a few minutes as we train each character...\n")
    
    start_time = time.time()
    system.initialize_characters()
    init_time = time.time() - start_time
    
    print(f"\nCharacters initialized in {init_time:.2f} seconds\n")
    
    # Demo questions
    questions = [
        "What is the most important thing in life?",
        "How should I live my life?",
        "What is love?",
        "How can I know God?",
        "What is wisdom?",
    ]
    
    for i, question in enumerate(questions, 1):
        print("=" * 80)
        print(f"Question {i}: {question}")
        print("=" * 80)
        
        # Get responses from all characters
        responses = system.compare_characters(question)
        
        for char_name, result in responses["responses"].items():
            if "error" not in result:
                print(f"\n--- {char_name.upper()} ---")
                print(f"Response: {result['response']}")
                print(f"Personality: {', '.join([f'{k}: {v:.2f}' for k, v in result['personality'].items()][:3])}")
            else:
                print(f"\n--- {char_name.upper()} ---")
                print(f"Error: {result['error']}")
        
        print("\n")
        time.sleep(1)
    
    # Individual character chat
    print("=" * 80)
    print("INDIVIDUAL CHARACTER CHAT")
    print("=" * 80)
    
    # Chat with Moses
    print("\n--- Chatting with Moses ---")
    moses_response = system.chat_with_character("Moses", "What is the greatest commandment?")
    print(f"Question: {moses_response['message']}")
    print(f"Response: {moses_response['response']}")
    
    # Chat with David
    print("\n--- Chatting with David ---")
    david_response = system.chat_with_character("David", "How should I worship God?")
    print(f"Question: {david_response['message']}")
    print(f"Response: {david_response['response']}")
    
    # Chat with John
    print("\n--- Chatting with John ---")
    john_response = system.chat_with_character("John", "What is the most important thing?")
    print(f"Question: {john_response['message']}")
    print(f"Response: {john_response['response']}")
    
    print("\n" + "=" * 80)
    print("Demo Complete!")
    print("=" * 80)
    print("\nEach character responds based on their actual Bible writings:")
    print("  - Moses: Law, commandments, reverence")
    print("  - David: Worship, mercy, relationship with God")
    print("  - Solomon: Wisdom, practical living, reflection")
    print("  - Paul: Grace, faith, the gospel")
    print("  - John: Love, the Word, intimate relationship")
    print("\nThe quantum approach ensures each character:")
    print("  - Understands meaning through entanglement")
    print("  - Responds based on their actual writings")
    print("  - Maintains their unique personality")
    print("  - Provides deeper, more meaningful responses")


if __name__ == "__main__":
    main()
