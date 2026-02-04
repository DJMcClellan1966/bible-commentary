"""
Profile Manager - Manages your spiritual profile and journey
"""
import json
import os
from datetime import datetime, date
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict, field


@dataclass
class SpiritualInterest:
    """A topic or theme you're interested in"""
    topic: str
    first_encountered: str
    times_explored: int = 1
    last_explored: str = None
    related_verses: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class Struggle:
    """A topic you find difficult to understand"""
    topic: str
    first_encountered: str
    questions_asked: List[str] = field(default_factory=list)
    attempts_to_understand: int = 1
    breakthrough: bool = False
    breakthrough_notes: str = ""


@dataclass
class UserProfile:
    """Your spiritual profile"""
    created: str
    last_active: str
    
    # Core tracking
    interests: Dict[str, SpiritualInterest] = field(default_factory=dict)
    struggles: Dict[str, Struggle] = field(default_factory=dict)
    
    # Reading history
    verses_read: List[str] = field(default_factory=list)
    chapters_completed: List[str] = field(default_factory=list)
    books_explored: List[str] = field(default_factory=list)
    
    # Patterns discovered
    favorite_themes: List[str] = field(default_factory=list)
    reading_patterns: Dict[str, any] = field(default_factory=dict)
    
    # Milestones
    milestones: List[Dict] = field(default_factory=list)
    
    # Preferences
    preferred_version: str = "asv"
    daily_reading_time: str = "morning"  # morning, evening, flexible
    reading_depth: str = "deep"  # quick, moderate, deep


class ProfileManager:
    """
    Manages your spiritual profile - tracking your journey, interests, and growth.
    """
    
    def __init__(self, profile_path: str = None):
        """
        Initialize the profile manager.
        
        Args:
            profile_path: Path to store profile data. Defaults to ai_twin/profile.json
        """
        if profile_path is None:
            base_dir = os.path.dirname(__file__)
            profile_path = os.path.join(base_dir, 'profile.json')
        
        self.profile_path = profile_path
        self.profile = self._load_or_create_profile()
    
    def _load_or_create_profile(self) -> UserProfile:
        """Load existing profile or create a new one"""
        if os.path.exists(self.profile_path):
            try:
                with open(self.profile_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Convert nested dicts back to dataclasses
                profile = UserProfile(
                    created=data.get('created', datetime.now().isoformat()),
                    last_active=datetime.now().isoformat()
                )
                
                # Load interests
                for topic, interest_data in data.get('interests', {}).items():
                    profile.interests[topic] = SpiritualInterest(**interest_data)
                
                # Load struggles
                for topic, struggle_data in data.get('struggles', {}).items():
                    profile.struggles[topic] = Struggle(**struggle_data)
                
                # Load other fields
                profile.verses_read = data.get('verses_read', [])
                profile.chapters_completed = data.get('chapters_completed', [])
                profile.books_explored = data.get('books_explored', [])
                profile.favorite_themes = data.get('favorite_themes', [])
                profile.reading_patterns = data.get('reading_patterns', {})
                profile.milestones = data.get('milestones', [])
                profile.preferred_version = data.get('preferred_version', 'asv')
                profile.daily_reading_time = data.get('daily_reading_time', 'morning')
                profile.reading_depth = data.get('reading_depth', 'deep')
                
                return profile
                
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error loading profile, creating new: {e}")
        
        # Create new profile
        return UserProfile(
            created=datetime.now().isoformat(),
            last_active=datetime.now().isoformat()
        )
    
    def save(self):
        """Save the profile to disk"""
        self.profile.last_active = datetime.now().isoformat()
        
        # Convert to serializable dict
        data = {
            'created': self.profile.created,
            'last_active': self.profile.last_active,
            'interests': {k: asdict(v) for k, v in self.profile.interests.items()},
            'struggles': {k: asdict(v) for k, v in self.profile.struggles.items()},
            'verses_read': self.profile.verses_read,
            'chapters_completed': self.profile.chapters_completed,
            'books_explored': self.profile.books_explored,
            'favorite_themes': self.profile.favorite_themes,
            'reading_patterns': self.profile.reading_patterns,
            'milestones': self.profile.milestones,
            'preferred_version': self.profile.preferred_version,
            'daily_reading_time': self.profile.daily_reading_time,
            'reading_depth': self.profile.reading_depth
        }
        
        os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
        with open(self.profile_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    def add_interest(self, topic: str, related_verse: str = None):
        """Record interest in a topic"""
        topic_key = topic.lower()
        
        if topic_key in self.profile.interests:
            interest = self.profile.interests[topic_key]
            interest.times_explored += 1
            interest.last_explored = datetime.now().isoformat()
            if related_verse and related_verse not in interest.related_verses:
                interest.related_verses.append(related_verse)
        else:
            self.profile.interests[topic_key] = SpiritualInterest(
                topic=topic,
                first_encountered=datetime.now().isoformat(),
                last_explored=datetime.now().isoformat(),
                related_verses=[related_verse] if related_verse else []
            )
        
        self.save()
    
    def add_struggle(self, topic: str, question: str = None):
        """Record a topic you're struggling to understand"""
        topic_key = topic.lower()
        
        if topic_key in self.profile.struggles:
            struggle = self.profile.struggles[topic_key]
            struggle.attempts_to_understand += 1
            if question and question not in struggle.questions_asked:
                struggle.questions_asked.append(question)
        else:
            self.profile.struggles[topic_key] = Struggle(
                topic=topic,
                first_encountered=datetime.now().isoformat(),
                questions_asked=[question] if question else []
            )
        
        self.save()
    
    def mark_breakthrough(self, topic: str, notes: str = ""):
        """Mark that you've had a breakthrough in understanding"""
        topic_key = topic.lower()
        
        if topic_key in self.profile.struggles:
            struggle = self.profile.struggles[topic_key]
            struggle.breakthrough = True
            struggle.breakthrough_notes = notes
            
            # Add milestone
            self.add_milestone(
                f"Breakthrough in understanding: {topic}",
                category="understanding"
            )
            
            self.save()
    
    def record_verse_read(self, reference: str):
        """Record that you've read a verse"""
        if reference not in self.profile.verses_read:
            self.profile.verses_read.append(reference)
        
        # Extract chapter and book
        parts = reference.rsplit(':', 1)
        if parts:
            chapter = parts[0]  # e.g., "John 3"
            if chapter not in self.profile.chapters_completed:
                self.profile.chapters_completed.append(chapter)
            
            # Extract book
            book_parts = chapter.rsplit(' ', 1)
            if book_parts:
                book = book_parts[0]  # e.g., "John"
                if book not in self.profile.books_explored:
                    self.profile.books_explored.append(book)
        
        self.save()
    
    def add_milestone(self, description: str, category: str = "general"):
        """Add a milestone to your journey"""
        milestone = {
            'date': datetime.now().isoformat(),
            'description': description,
            'category': category
        }
        self.profile.milestones.append(milestone)
        self.save()
    
    def get_top_interests(self, limit: int = 5) -> List[Dict]:
        """Get your most explored topics"""
        sorted_interests = sorted(
            self.profile.interests.values(),
            key=lambda x: x.times_explored,
            reverse=True
        )
        return [asdict(i) for i in sorted_interests[:limit]]
    
    def get_active_struggles(self) -> List[Dict]:
        """Get topics you're still working to understand"""
        active = [s for s in self.profile.struggles.values() if not s.breakthrough]
        return [asdict(s) for s in active]
    
    def get_journey_summary(self) -> Dict:
        """Get a summary of your spiritual journey"""
        days_active = 1
        if self.profile.created:
            created_date = datetime.fromisoformat(self.profile.created)
            days_active = max(1, (datetime.now() - created_date).days)
        
        return {
            'days_on_journey': days_active,
            'verses_read': len(self.profile.verses_read),
            'chapters_completed': len(self.profile.chapters_completed),
            'books_explored': len(self.profile.books_explored),
            'topics_explored': len(self.profile.interests),
            'breakthroughs': sum(1 for s in self.profile.struggles.values() if s.breakthrough),
            'active_struggles': sum(1 for s in self.profile.struggles.values() if not s.breakthrough),
            'milestones': len(self.profile.milestones),
            'top_interests': self.get_top_interests(3),
            'recent_milestones': self.profile.milestones[-3:] if self.profile.milestones else []
        }
    
    def suggest_revisit_topics(self) -> List[Dict]:
        """Suggest topics that might benefit from revisiting"""
        suggestions = []
        
        # Topics struggled with multiple times
        for topic, struggle in self.profile.struggles.items():
            if not struggle.breakthrough and struggle.attempts_to_understand >= 2:
                suggestions.append({
                    'topic': struggle.topic,
                    'reason': f"You've asked about this {struggle.attempts_to_understand} times",
                    'questions': struggle.questions_asked[-3:],
                    'type': 'struggle'
                })
        
        # Topics not revisited recently
        for topic, interest in self.profile.interests.items():
            if interest.last_explored:
                last = datetime.fromisoformat(interest.last_explored)
                days_since = (datetime.now() - last).days
                if days_since > 30 and interest.times_explored >= 3:
                    suggestions.append({
                        'topic': interest.topic,
                        'reason': f"You were interested in this ({interest.times_explored} times) but haven't explored it in {days_since} days",
                        'related_verses': interest.related_verses[-3:],
                        'type': 'interest'
                    })
        
        return suggestions
