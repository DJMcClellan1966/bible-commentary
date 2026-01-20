"""
Book Library System for Bible Study App
Manages AI-generated books and provides library functionality
"""
import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class BookLibrary:
    """
    Manages a library of AI-generated Bible study books
    """
    
    def __init__(self, library_dir: str = "book_library"):
        """Initialize the book library"""
        self.library_dir = library_dir
        self.books_dir = os.path.join(library_dir, "books")
        self.metadata_file = os.path.join(library_dir, "library_metadata.json")
        
        # Create directories
        os.makedirs(self.books_dir, exist_ok=True)
        os.makedirs(library_dir, exist_ok=True)
        
        # Load library metadata
        self.metadata = self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Load library metadata"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "books": [],
            "last_updated": datetime.now().isoformat(),
            "total_books": 0
        }
    
    def _save_metadata(self):
        """Save library metadata"""
        self.metadata["last_updated"] = datetime.now().isoformat()
        self.metadata["total_books"] = len(self.metadata["books"])
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, indent=2)
    
    def add_book(self, book_path: str, title: str, description: str = "", 
                 category: str = "General", tags: List[str] = None,
                 author: str = "AI-Powered Biblical Analysis") -> bool:
        """
        Add a book to the library
        
        Args:
            book_path: Path to the book markdown file
            title: Book title
            description: Book description
            category: Book category
            tags: List of tags
            author: Book author
        """
        if not os.path.exists(book_path):
            return False
        
        # Copy book to library
        book_filename = os.path.basename(book_path)
        library_book_path = os.path.join(self.books_dir, book_filename)
        
        # Copy file
        import shutil
        shutil.copy2(book_path, library_book_path)
        
        # Get book stats
        with open(book_path, 'r', encoding='utf-8') as f:
            content = f.read()
            word_count = len(content.split())
            char_count = len(content)
        
        # Add to metadata
        book_entry = {
            "id": len(self.metadata["books"]) + 1,
            "title": title,
            "description": description,
            "category": category,
            "tags": tags or [],
            "author": author,
            "file_path": library_book_path,
            "original_path": book_path,
            "word_count": word_count,
            "char_count": char_count,
            "added_date": datetime.now().isoformat(),
            "last_read": None,
            "read_count": 0
        }
        
        self.metadata["books"].append(book_entry)
        self._save_metadata()
        
        return True
    
    def get_book(self, book_id: int) -> Optional[Dict]:
        """Get a book by ID"""
        for book in self.metadata["books"]:
            if book["id"] == book_id:
                return book
        return None
    
    def get_all_books(self) -> List[Dict]:
        """Get all books in library"""
        return self.metadata["books"]
    
    def search_books(self, query: str) -> List[Dict]:
        """Search books by title, description, or tags"""
        query_lower = query.lower()
        results = []
        
        for book in self.metadata["books"]:
            if (query_lower in book["title"].lower() or
                query_lower in book.get("description", "").lower() or
                any(query_lower in tag.lower() for tag in book.get("tags", []))):
                results.append(book)
        
        return results
    
    def get_books_by_category(self, category: str) -> List[Dict]:
        """Get books by category"""
        return [b for b in self.metadata["books"] if b["category"] == category]
    
    def get_books_by_tag(self, tag: str) -> List[Dict]:
        """Get books by tag"""
        return [b for b in self.metadata["books"] if tag.lower() in [t.lower() for t in b.get("tags", [])]]
    
    def read_book(self, book_id: int) -> Optional[str]:
        """Read a book's content"""
        book = self.get_book(book_id)
        if not book or not os.path.exists(book["file_path"]):
            return None
        
        # Update read stats
        book["last_read"] = datetime.now().isoformat()
        book["read_count"] = book.get("read_count", 0) + 1
        self._save_metadata()
        
        # Read content
        with open(book["file_path"], 'r', encoding='utf-8') as f:
            return f.read()
    
    def get_categories(self) -> List[str]:
        """Get all categories"""
        categories = set()
        for book in self.metadata["books"]:
            categories.add(book.get("category", "General"))
        return sorted(list(categories))
    
    def get_tags(self) -> List[str]:
        """Get all tags"""
        tags = set()
        for book in self.metadata["books"]:
            tags.update(book.get("tags", []))
        return sorted(list(tags))
    
    def get_statistics(self) -> Dict:
        """Get library statistics"""
        return {
            "total_books": len(self.metadata["books"]),
            "categories": len(self.get_categories()),
            "tags": len(self.get_tags()),
            "total_words": sum(b.get("word_count", 0) for b in self.metadata["books"]),
            "most_read": sorted(self.metadata["books"], 
                              key=lambda x: x.get("read_count", 0), 
                              reverse=True)[:5] if self.metadata["books"] else []
        }


# Book generator catalog
BOOK_TYPES = {
    "Topical Studies": [
        {"title": "Love in the Bible", "description": "Exploring God's love throughout Scripture", "tags": ["love", "relationships", "god"]},
        {"title": "Faith Throughout Scripture", "description": "How faith is revealed from Genesis to Revelation", "tags": ["faith", "trust", "belief"]},
        {"title": "Grace and Mercy", "description": "God's unmerited favor and compassion", "tags": ["grace", "mercy", "forgiveness"]},
        {"title": "Hope and Encouragement", "description": "Biblical hope in difficult times", "tags": ["hope", "encouragement", "comfort"]},
        {"title": "Prayer and Intercession", "description": "The power and practice of prayer", "tags": ["prayer", "intercession", "worship"]},
    ],
    "Character Studies": [
        {"title": "Abraham: The Father of Faith", "description": "The life and faith of Abraham", "tags": ["abraham", "faith", "covenant"]},
        {"title": "Moses: The Deliverer", "description": "Moses' journey from prince to prophet", "tags": ["moses", "exodus", "leadership"]},
        {"title": "David: A Man After God's Heart", "description": "The shepherd who became king", "tags": ["david", "psalms", "worship"]},
        {"title": "Paul: Apostle to the Nations", "description": "From persecutor to preacher", "tags": ["paul", "apostle", "missions"]},
    ],
    "Devotional Books": [
        {"title": "365-Day Devotional", "description": "Daily readings for the year", "tags": ["devotional", "daily", "year"]},
        {"title": "Morning Devotions", "description": "Start each day with Scripture", "tags": ["devotional", "morning", "daily"]},
        {"title": "Evening Reflections", "description": "End each day with God's Word", "tags": ["devotional", "evening", "reflection"]},
    ],
    "Thematic Studies": [
        {"title": "The Parables of Jesus", "description": "All parables explained and connected", "tags": ["parables", "jesus", "teaching"]},
        {"title": "The Miracles of Jesus", "description": "Jesus' miracles and their meaning", "tags": ["miracles", "jesus", "power"]},
        {"title": "The 'I Am' Sayings of Jesus", "description": "Jesus' declarations of identity", "tags": ["jesus", "identity", "gospel"]},
        {"title": "The Beatitudes", "description": "The path to blessedness", "tags": ["beatitudes", "jesus", "sermon"]},
    ],
    "Book Studies": [
        {"title": "The Book of Psalms", "description": "Exploring all 150 psalms", "tags": ["psalms", "worship", "prayer"]},
        {"title": "The Book of Proverbs", "description": "Wisdom for daily living", "tags": ["proverbs", "wisdom", "practical"]},
        {"title": "The Gospel of John", "description": "The gospel of life and love", "tags": ["john", "gospel", "jesus"]},
    ]
}


def initialize_library_with_existing_books():
    """Initialize library with books we've already generated"""
    library = BookLibrary()
    
    # Add Mysteries book if it exists
    mysteries_path = "bible_mysteries_book/bible_mysteries_book.md"
    if os.path.exists(mysteries_path):
        library.add_book(
            mysteries_path,
            "The Mysteries of the Bible: How Divine Mysteries Reveal God's Grand Design",
            "A comprehensive exploration of 20 biblical mysteries and how they relate to the whole of Scripture",
            category="Theological Studies",
            tags=["mysteries", "theology", "biblical studies", "relationships"]
        )
    
    # Add Red Letters book if it exists
    red_letters_path = "red_letters_book/red_letters_book.md"
    if os.path.exists(red_letters_path):
        library.add_book(
            red_letters_path,
            "Red Letters: How Jesus' Words Reveal the Way to Relationship with God",
            "Exploring Jesus' sayings from the Gospels and how they relate to the whole Bible and reveal relationships",
            category="Gospel Studies",
            tags=["jesus", "gospels", "red letters", "relationships", "discipleship"]
        )
    
    print(f"Library initialized with {len(library.get_all_books())} books")
    return library


if __name__ == "__main__":
    library = initialize_library_with_existing_books()
    
    print("\nLibrary Statistics:")
    stats = library.get_statistics()
    print(f"  Total books: {stats['total_books']}")
    print(f"  Categories: {stats['categories']}")
    print(f"  Total words: {stats['total_words']:,}")
    
    print("\nAvailable Books:")
    for book in library.get_all_books():
        print(f"  - {book['title']} ({book['category']})")