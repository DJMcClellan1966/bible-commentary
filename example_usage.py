"""
Example usage of the Bible Commentary Agent
"""
from agent import BibleCommentaryAgent
from models import init_db

# Initialize database
init_db()

# Create agent
agent = BibleCommentaryAgent()

# Example 1: Build commentary for Genesis 1:1
print("=" * 60)
print("Example 1: Building commentary for Genesis 1:1")
print("=" * 60)
result = agent.build_commentary(
    book="Genesis",
    chapter=1,
    verse=1,
    source_types=["modern", "church_fathers"],
    synthesize=True
)
print(f"\nFound {len(result['commentaries'])} commentaries")
if result.get('synthesized'):
    print(f"\nSynthesized Commentary:\n{result['synthesized'][:500]}...")

# Example 2: Get Church Fathers commentary only
print("\n" + "=" * 60)
print("Example 2: Getting Church Fathers commentary for Genesis 1:1")
print("=" * 60)
fathers_result = agent.get_commentary_by_category(
    book="Genesis",
    chapter=1,
    verse=1,
    category="church_fathers"
)
print(f"\nFound {len(fathers_result['commentaries'])} Church Fathers commentaries")

# Example 3: Search commentaries
print("\n" + "=" * 60)
print("Example 3: Searching for commentaries about 'creation'")
print("=" * 60)
search_results = agent.search_commentaries(
    query="creation",
    book="Genesis"
)
print(f"\nFound {len(search_results)} matching commentaries")

# Example 4: Get improvement suggestions
print("\n" + "=" * 60)
print("Example 4: Getting improvement suggestions")
print("=" * 60)
suggestions = agent.suggest_improvements(
    book="Genesis",
    chapter=1,
    verse=1
)
print("\nSuggestions:")
for i, suggestion in enumerate(suggestions, 1):
    print(f"{i}. {suggestion}")

print("\n" + "=" * 60)
print("Examples completed!")
print("=" * 60)
