"""
Example Applications Built on Complete AI System
Demonstrates practical use cases
"""
from complete_ai_system import CompleteAISystem
from typing import List, Dict
import json


class ResearchPlatform:
    """Intelligent Research Platform"""
    
    def __init__(self, ai_system: CompleteAISystem):
        self.ai = ai_system
        self.papers = []
    
    def add_paper(self, title: str, abstract: str, authors: List[str]):
        """Add a research paper"""
        paper = {
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "full_text": f"{title}. {abstract}"
        }
        self.papers.append(paper)
        return paper
    
    def search_papers(self, query: str, top_k: int = 10) -> Dict:
        """Search papers semantically"""
        corpus = [p["full_text"] for p in self.papers]
        results = self.ai.search.search_and_discover(query, corpus)
        
        # Map back to papers
        paper_results = []
        for result in results["results"][:top_k]:
            # Find matching paper
            for paper in self.papers:
                if paper["full_text"] == result["text"]:
                    paper_results.append({
                        "title": paper["title"],
                        "authors": paper["authors"],
                        "similarity": result["similarity"],
                        "abstract": paper["abstract"][:200] + "..."
                    })
                    break
        
        return {
            "query": query,
            "results": paper_results,
            "themes": results["themes"],
            "related_concepts": list(results["related_concepts"].keys())[:5]
        }
    
    def build_research_graph(self) -> Dict:
        """Build knowledge graph of research field"""
        corpus = [p["full_text"] for p in self.papers]
        graph = self.ai.knowledge_graph.build_graph(corpus)
        
        return {
            "papers": len(self.papers),
            "nodes": len(graph["nodes"]),
            "edges": len(graph["edges"]),
            "themes": len(graph["themes"]),
            "graph": graph
        }


class PersonalKnowledgeBase:
    """Personal Knowledge Base"""
    
    def __init__(self, ai_system: CompleteAISystem):
        self.ai = ai_system
        self.notes = []
    
    def add_note(self, title: str, content: str, tags: List[str] = None):
        """Add a note"""
        note = {
            "id": len(self.notes),
            "title": title,
            "content": content,
            "tags": tags or [],
            "full_text": f"{title}. {content}"
        }
        self.notes.append(note)
        return note
    
    def search_notes(self, query: str, top_k: int = 10) -> Dict:
        """Search notes semantically"""
        corpus = [n["full_text"] for n in self.notes]
        results = self.ai.search.search_and_discover(query, corpus)
        
        # Map back to notes
        note_results = []
        for result in results["results"][:top_k]:
            for note in self.notes:
                if note["full_text"] == result["text"]:
                    note_results.append({
                        "title": note["title"],
                        "content": note["content"][:150] + "...",
                        "tags": note["tags"],
                        "similarity": result["similarity"]
                    })
                    break
        
        return {
            "query": query,
            "results": note_results,
            "themes": results["themes"]
        }
    
    def discover_connections(self) -> Dict:
        """Discover connections between notes"""
        corpus = [n["full_text"] for n in self.notes]
        graph = self.ai.knowledge_graph.build_graph(corpus)
        
        # Find interesting connections
        connections = []
        for edge in graph["edges"][:20]:  # Top 20 connections
            source_note = self.notes[edge["source"]]
            target_note = self.notes[edge["target"]]
            connections.append({
                "from": source_note["title"],
                "to": target_note["title"],
                "strength": edge["weight"],
                "type": "semantic_connection"
            })
        
        return {
            "notes": len(self.notes),
            "connections": connections,
            "themes": [t["theme"] for t in graph["themes"]]
        }


class ContentPlatform:
    """Intelligent Content Platform"""
    
    def __init__(self, ai_system: CompleteAISystem):
        self.ai = ai_system
        self.articles = []
    
    def add_article(self, title: str, content: str, author: str):
        """Add an article"""
        article = {
            "id": len(self.articles),
            "title": title,
            "content": content,
            "author": author,
            "full_text": f"{title}. {content}"
        }
        self.articles.append(article)
        return article
    
    def search_content(self, query: str, top_k: int = 10) -> Dict:
        """Search content semantically"""
        corpus = [a["full_text"] for a in self.articles]
        results = self.ai.search.search_and_discover(query, corpus)
        
        # Map back to articles
        article_results = []
        for result in results["results"][:top_k]:
            for article in self.articles:
                if article["full_text"] == result["text"]:
                    article_results.append({
                        "title": article["title"],
                        "author": article["author"],
                        "content": article["content"][:200] + "...",
                        "similarity": result["similarity"]
                    })
                    break
        
        return {
            "query": query,
            "results": article_results,
            "themes": results["themes"]
        }
    
    def get_recommendations(self, user_interests: List[str], top_k: int = 5) -> List[Dict]:
        """Get personalized recommendations"""
        # Build user profile
        user_profile = " ".join(user_interests)
        
        # Find similar articles
        corpus = [a["full_text"] for a in self.articles]
        results = self.ai.search.search_and_discover(user_profile, corpus)
        
        # Return recommendations
        recommendations = []
        for result in results["results"][:top_k]:
            for article in self.articles:
                if article["full_text"] == result["text"]:
                    recommendations.append({
                        "title": article["title"],
                        "author": article["author"],
                        "relevance": result["similarity"],
                        "reason": f"Similar to your interest in {user_interests[0]}"
                    })
                    break
        
        return recommendations


def demonstrate_applications():
    """Demonstrate example applications"""
    print("=" * 80)
    print("EXAMPLE APPLICATIONS BUILT ON COMPLETE AI SYSTEM")
    print("=" * 80)
    
    # Create AI system
    ai_system = CompleteAISystem()
    
    # Application 1: Research Platform
    print("\n" + "=" * 80)
    print("APPLICATION 1: INTELLIGENT RESEARCH PLATFORM")
    print("=" * 80)
    
    research = ResearchPlatform(ai_system)
    
    # Add papers
    research.add_paper(
        "Quantum Machine Learning",
        "We explore the application of quantum computing to machine learning algorithms",
        ["Alice Smith", "Bob Jones"]
    )
    research.add_paper(
        "Deep Learning for Natural Language",
        "We present a deep learning approach to natural language processing",
        ["Charlie Brown"]
    )
    research.add_paper(
        "Quantum Algorithms for Optimization",
        "We develop quantum algorithms for solving optimization problems",
        ["David Wilson"]
    )
    
    # Search papers
    print("\n1. Searching for 'machine learning and quantum computing'...")
    search_results = research.search_papers("machine learning and quantum computing")
    print(f"   Found {len(search_results['results'])} papers")
    for result in search_results['results'][:3]:
        print(f"   - {result['title']} (similarity: {result['similarity']:.3f})")
    
    # Build knowledge graph
    print("\n2. Building research knowledge graph...")
    graph = research.build_research_graph()
    print(f"   Papers: {graph['papers']}")
    print(f"   Nodes: {graph['nodes']}")
    print(f"   Edges: {graph['edges']}")
    print(f"   Themes: {graph['themes']}")
    
    # Application 2: Personal Knowledge Base
    print("\n" + "=" * 80)
    print("APPLICATION 2: PERSONAL KNOWLEDGE BASE")
    print("=" * 80)
    
    knowledge_base = PersonalKnowledgeBase(ai_system)
    
    # Add notes
    knowledge_base.add_note(
        "Thoughts on Love",
        "Love is patient and kind. It's about understanding and compassion.",
        ["philosophy", "relationships"]
    )
    knowledge_base.add_note(
        "Learning Machine Learning",
        "Machine learning is about teaching computers to learn from data.",
        ["technology", "learning"]
    )
    knowledge_base.add_note(
        "Understanding Relationships",
        "Relationships require patience, understanding, and mutual respect.",
        ["philosophy", "relationships"]
    )
    
    # Search notes
    print("\n1. Searching for 'understanding relationships'...")
    search_results = knowledge_base.search_notes("understanding relationships")
    print(f"   Found {len(search_results['results'])} notes")
    for result in search_results['results']:
        print(f"   - {result['title']} (similarity: {result['similarity']:.3f})")
    
    # Discover connections
    print("\n2. Discovering connections between notes...")
    connections = knowledge_base.discover_connections()
    print(f"   Notes: {connections['notes']}")
    print(f"   Connections found: {len(connections['connections'])}")
    for conn in connections['connections'][:3]:
        print(f"   - {conn['from']} -> {conn['to']} (strength: {conn['strength']:.3f})")
    print(f"   Themes: {', '.join(connections['themes'][:3])}")
    
    # Application 3: Content Platform
    print("\n" + "=" * 80)
    print("APPLICATION 3: INTELLIGENT CONTENT PLATFORM")
    print("=" * 80)
    
    content = ContentPlatform(ai_system)
    
    # Add articles
    content.add_article(
        "The Future of AI",
        "Artificial intelligence is transforming how we work and live.",
        "Tech Writer"
    )
    content.add_article(
        "Understanding Quantum Computing",
        "Quantum computing promises to solve problems impossible for classical computers.",
        "Science Journalist"
    )
    content.add_article(
        "Machine Learning in Healthcare",
        "Machine learning is revolutionizing healthcare with predictive analytics.",
        "Health Reporter"
    )
    
    # Search content
    print("\n1. Searching for 'artificial intelligence'...")
    search_results = content.search_content("artificial intelligence")
    print(f"   Found {len(search_results['results'])} articles")
    for result in search_results['results']:
        print(f"   - {result['title']} by {result['author']} (similarity: {result['similarity']:.3f})")
    
    # Get recommendations
    print("\n2. Getting recommendations for user interested in 'technology'...")
    recommendations = content.get_recommendations(["technology", "AI", "computing"])
    print(f"   Recommendations: {len(recommendations)}")
    for rec in recommendations:
        print(f"   - {rec['title']} (relevance: {rec['relevance']:.3f})")
        print(f"     Reason: {rec['reason']}")
    
    print("\n" + "=" * 80)
    print("APPLICATIONS DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("""
These examples show how the complete AI system can be used to build:

[+] Research Platform - Find papers, discover connections, build knowledge graphs
[+] Personal Knowledge Base - Search notes, discover relationships, organize by themes
[+] Content Platform - Semantic search, recommendations, theme discovery

All built on the same AI foundation with consistent behavior and performance!
    """)


if __name__ == "__main__":
    demonstrate_applications()
