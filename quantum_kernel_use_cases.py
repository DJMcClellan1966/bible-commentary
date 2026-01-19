"""
Demonstration: Quantum Kernel Use Cases Across Different App Types
Shows how kernel benefits various application types
"""
from quantum_kernel import QuantumKernel, KernelConfig

def demonstrate_ecommerce():
    """E-commerce: Product recommendations"""
    print("=" * 80)
    print("E-COMMERCE: Product Recommendations")
    print("=" * 80)
    
    kernel = QuantumKernel()
    
    products = [
        "Wireless Bluetooth Headphones",
        "Noise-Canceling Earbuds",
        "Smartphone Case with Stand",
        "USB-C Charging Cable",
        "Portable Phone Charger",
        "Wireless Charging Pad",
        "Laptop Stand",
        "Mechanical Keyboard"
    ]
    
    user_viewing = "Wireless Bluetooth Headphones"
    
    print(f"\nUser viewing: {user_viewing}")
    print("\nQuantum Kernel Recommendations:")
    
    recommendations = kernel.find_similar(user_viewing, products, top_k=5)
    for product, similarity in recommendations:
        if product != user_viewing:
            print(f"  - {product} (similarity: {similarity:.3f})")
    
    print("\nBenefits:")
    print("  - Finds similar products semantically")
    print("  - Suggests complementary items")
    print("  - Understands product relationships")


def demonstrate_elearning():
    """E-Learning: Course recommendations"""
    print("\n" + "=" * 80)
    print("E-LEARNING: Course Recommendations")
    print("=" * 80)
    
    kernel = QuantumKernel()
    
    courses = [
        "Python Programming Basics",
        "Object-Oriented Programming in Python",
        "Data Structures and Algorithms",
        "Machine Learning Fundamentals",
        "Deep Learning with Python",
        "Web Development with Django",
        "Database Design",
        "Software Engineering Principles"
    ]
    
    student_taking = "Python Programming Basics"
    
    print(f"\nStudent taking: {student_taking}")
    print("\nQuantum Kernel Next Steps:")
    
    recommendations = kernel.find_similar(student_taking, courses, top_k=5)
    for course, similarity in recommendations:
        if course != student_taking:
            print(f"  - {course} (similarity: {similarity:.3f})")
    
    print("\nBenefits:")
    print("  - Suggests logical learning paths")
    print("  - Finds related courses")
    print("  - Personalizes learning journey")


def demonstrate_support():
    """Customer Support: Question matching"""
    print("\n" + "=" * 80)
    print("CUSTOMER SUPPORT: Question Matching")
    print("=" * 80)
    
    kernel = QuantumKernel()
    
    past_questions = [
        "How do I reset my password?",
        "I forgot my login credentials",
        "Can I change my email address?",
        "How to update my account settings",
        "What is your refund policy?",
        "How do I cancel my subscription?",
        "Where can I find my order history?",
        "How to contact customer service"
    ]
    
    new_question = "I can't remember my password"
    
    print(f"\nNew question: {new_question}")
    print("\nQuantum Kernel Matches:")
    
    matches = kernel.find_similar(new_question, past_questions, top_k=3)
    for question, similarity in matches:
        print(f"  - {question} (similarity: {similarity:.3f})")
    
    print("\nBenefits:")
    print("  - Finds similar questions semantically")
    print("  - Suggests relevant answers")
    print("  - Understands user intent")


def demonstrate_news():
    """News Platform: Article Discovery"""
    print("\n" + "=" * 80)
    print("NEWS PLATFORM: Article Discovery")
    print("=" * 80)
    
    kernel = QuantumKernel()
    
    articles = [
        "Climate Change Summit Reaches Historic Agreement",
        "Global Warming Effects on Ocean Levels",
        "Renewable Energy Investments Surge",
        "Electric Vehicle Sales Hit Record High",
        "Stock Market Reaches New Peak",
        "Tech Companies Announce AI Initiatives",
        "Healthcare System Faces Challenges",
        "Education Reform Bill Passes Senate"
    ]
    
    user_reading = "Climate Change Summit Reaches Historic Agreement"
    
    print(f"\nUser reading: {user_reading}")
    print("\nQuantum Kernel Related Articles:")
    
    related = kernel.find_similar(user_reading, articles, top_k=5)
    for article, similarity in related:
        if article != user_reading:
            print(f"  - {article} (similarity: {similarity:.3f})")
    
    print("\nBenefits:")
    print("  - Discovers related articles automatically")
    print("  - Groups news by theme")
    print("  - Enhances content discovery")


def demonstrate_research():
    """Research Platform: Paper Discovery"""
    print("\n" + "=" * 80)
    print("RESEARCH PLATFORM: Paper Discovery")
    print("=" * 80)
    
    kernel = QuantumKernel()
    
    papers = [
        "Quantum Machine Learning Algorithms",
        "Neural Network Optimization Techniques",
        "Deep Learning for Natural Language Processing",
        "Quantum Computing Applications",
        "Machine Learning in Healthcare",
        "Reinforcement Learning Strategies",
        "Computer Vision with Deep Learning",
        "Distributed Machine Learning Systems"
    ]
    
    researcher_reading = "Quantum Machine Learning Algorithms"
    
    print(f"\nResearcher reading: {researcher_reading}")
    print("\nQuantum Kernel Related Papers:")
    
    related = kernel.find_similar(researcher_reading, papers, top_k=5)
    for paper, similarity in related:
        if paper != researcher_reading:
            print(f"  - {paper} (similarity: {similarity:.3f})")
    
    print("\nBenefits:")
    print("  - Finds related research automatically")
    print("  - Discovers citation relationships")
    print("  - Enhances literature review")


def main():
    """Demonstrate quantum kernel across different app types"""
    print("\n" + "=" * 80)
    print("QUANTUM KERNEL: UNIVERSAL APPLICATION BENEFITS")
    print("=" * 80)
    print("\nDemonstrating how quantum kernel benefits different app types...")
    
    demonstrate_ecommerce()
    demonstrate_elearning()
    demonstrate_support()
    demonstrate_news()
    demonstrate_research()
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
The quantum kernel provides universal benefits:

[+] Semantic Understanding
   - All apps benefit from understanding meaning
   - Not just keyword matching
   - Better user experience

[+] Relationship Discovery
   - Automatic connection finding
   - No manual curation needed
   - Scales to any size

[+] Performance
   - Caching benefits all apps
   - Parallel processing helps everyone
   - 10-200x speedup possible

[+] Consistency
   - Same algorithms everywhere
   - Predictable behavior
   - Reliable results

The quantum kernel is a universal foundation that makes
ANY application smarter, faster, and more capable!
    """)


if __name__ == "__main__":
    main()
