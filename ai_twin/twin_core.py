"""
AI Twin Core - Your Personal Bible Study Companion

This is the heart of your AI Twin - it learns you:
- Tracks your questions and what you're really seeking
- Identifies patterns in your spiritual interests
- Remembers your struggles and helps you revisit them
- Grows with you on your journey
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from .question_analyzer import QuestionAnalyzer
from .profile_manager import ProfileManager
from .answer_engine import AnswerEngine


class AITwin:
    """
    Your AI Twin - a companion that learns your spiritual journey.
    
    Unlike generic chatbots, this companion:
    - Remembers every question you've asked
    - Identifies patterns in what interests you
    - Notices what you struggle to understand
    - Suggests when to revisit topics
    - Grows its understanding of you over time
    """
    
    def __init__(self, data_dir: str = None):
        """
        Initialize your AI Twin.
        
        Args:
            data_dir: Directory to store your data. Defaults to ai_twin/
        """
        if data_dir is None:
            data_dir = os.path.dirname(__file__)
        
        self.data_dir = data_dir
        
        # Initialize components
        self.analyzer = QuestionAnalyzer()
        self.profile = ProfileManager(
            os.path.join(data_dir, 'profile.json')
        )
        
        # Initialize answer engine for generating actual answers
        self.answer_engine = AnswerEngine()
        
        # Load question history
        self.questions_file = os.path.join(data_dir, 'questions_log.json')
        self.questions = self._load_questions()
        
        # Load insights
        self.insights_file = os.path.join(data_dir, 'insights.json')
        self.insights = self._load_insights()
    
    def _load_questions(self) -> List[Dict]:
        """Load question history"""
        if os.path.exists(self.questions_file):
            try:
                with open(self.questions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return []
    
    def _save_questions(self):
        """Save question history"""
        os.makedirs(os.path.dirname(self.questions_file), exist_ok=True)
        with open(self.questions_file, 'w', encoding='utf-8') as f:
            json.dump(self.questions, f, indent=2, default=str)
    
    def _load_insights(self) -> Dict:
        """Load discovered insights"""
        if os.path.exists(self.insights_file):
            try:
                with open(self.insights_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {'patterns': [], 'last_analysis': None}
    
    def _save_insights(self):
        """Save insights"""
        os.makedirs(os.path.dirname(self.insights_file), exist_ok=True)
        with open(self.insights_file, 'w', encoding='utf-8') as f:
            json.dump(self.insights, f, indent=2, default=str)
    
    def ask(self, question: str, context: Dict = None) -> Dict:
        """
        Process a question, learn from it, and provide an actual answer.
        
        Args:
            question: The question being asked
            context: Optional context (current verse, reading, etc.)
        
        Returns:
            Dict with analysis, actual answer, verses, and church fathers
        """
        # Analyze the question
        analysis = self.analyzer.analyze_question(question)
        
        # Add context
        if context:
            analysis['context'] = context
        
        # Store the question
        self.questions.append(analysis)
        self._save_questions()
        
        # Update profile based on topics
        for topic in analysis['topics']:
            if analysis['is_struggle']:
                self.profile.add_struggle(topic, question)
            else:
                self.profile.add_interest(topic)
        
        # Check for breakthrough
        if analysis['is_breakthrough']:
            for topic in analysis['topics']:
                self.profile.mark_breakthrough(topic)
        
        # Generate personal observation (meta-response about your journey)
        personal_observation = self._generate_personal_response(analysis)
        
        # Generate actual answer with Scripture and Church Fathers
        answer_data = self.answer_engine.answer_question(question, analysis['topics'])
        
        # Combine personal observation with the actual answer
        full_response = self._combine_response(personal_observation, answer_data)
        
        return {
            'analysis': analysis,
            'personal_response': full_response,
            'answer': answer_data['answer'],
            'key_verses': answer_data.get('key_verses', []),
            'church_fathers': answer_data.get('church_fathers', []),
            'typology': answer_data.get('typology'),
            'confidence': answer_data.get('confidence', 'medium'),
            'related_interests': self._get_related_interests(analysis['topics']),
            'suggested_connections': self._suggest_connections(analysis)
        }
    
    def _combine_response(self, personal_observation: str, answer_data: Dict) -> str:
        """Combine personal observation with actual answer"""
        parts = []
        
        # Add personal observation if meaningful
        if personal_observation and 'Good question' not in personal_observation:
            parts.append(personal_observation)
            parts.append("")  # Blank line
        
        # Add the actual answer
        if answer_data.get('answer'):
            parts.append(answer_data['answer'])
        
        # Add key verses summary
        if answer_data.get('key_verses'):
            parts.append("")
            parts.append("Key passages to study:")
            for verse in answer_data['key_verses'][:3]:
                parts.append(f"  - {verse['reference']}")
        
        # Add Church Father quote if available
        if answer_data.get('church_fathers'):
            father = answer_data['church_fathers'][0]
            parts.append("")
            parts.append(f'As {father.get("author", "the Church Fathers")} wrote: "{father.get("quote", "")[:150]}..."')
        
        return '\n'.join(parts)
    
    def _generate_personal_response(self, analysis: Dict) -> str:
        """Generate a personalized response based on the question and your history"""
        responses = []
        
        topics = analysis['topics']
        is_struggle = analysis['is_struggle']
        
        # Check if this is a recurring topic
        for topic in topics:
            if topic in self.profile.profile.interests:
                interest = self.profile.profile.interests[topic]
                if interest.times_explored >= 3:
                    responses.append(
                        f"I notice '{topic}' keeps drawing your attention - "
                        f"you've explored this {interest.times_explored} times. "
                        f"This seems to be an important part of your spiritual journey."
                    )
            
            if topic in self.profile.profile.struggles:
                struggle = self.profile.profile.struggles[topic]
                if not struggle.breakthrough:
                    responses.append(
                        f"You've wrestled with '{topic}' before. "
                        f"Let's approach it from a different angle this time."
                    )
        
        # Check for struggle
        if is_struggle:
            responses.append(
                "I can sense this is something you're wrestling with. "
                "That's a sign of genuine seeking - the deepest understanding "
                "often comes through struggle."
            )
        
        # Default response
        if not responses:
            if analysis['question_type'] == 'why':
                responses.append(
                    "You're asking 'why' - the deepest kind of question. "
                    "Let's explore this together."
                )
            else:
                responses.append(
                    "Good question. Let me help you explore this."
                )
        
        return ' '.join(responses)
    
    def _get_related_interests(self, topics: List[str]) -> List[Dict]:
        """Find your related interests"""
        related = []
        
        for topic in topics:
            # Find interests that share themes
            for interest_topic, interest in self.profile.profile.interests.items():
                if interest_topic != topic.lower():
                    # Simple relatedness check
                    if any(word in interest_topic for word in topic.lower().split()):
                        related.append({
                            'topic': interest.topic,
                            'times_explored': interest.times_explored,
                            'related_verses': interest.related_verses[:3]
                        })
        
        return related[:5]
    
    def _suggest_connections(self, analysis: Dict) -> List[str]:
        """Suggest connections based on the question"""
        suggestions = []
        
        topics = analysis['topics']
        
        # Suggest connections between current question and past interests
        top_interests = self.profile.get_top_interests(5)
        
        for interest in top_interests:
            interest_topic = interest['topic'].lower()
            if interest_topic not in [t.lower() for t in topics]:
                suggestions.append(
                    f"Consider how this connects to '{interest['topic']}' - "
                    f"another area you've been exploring."
                )
        
        return suggestions[:2]
    
    def get_daily_greeting(self) -> str:
        """Get a personalized daily greeting"""
        summary = self.profile.get_journey_summary()
        
        greetings = []
        
        # Time-based greeting
        hour = datetime.now().hour
        if hour < 12:
            greetings.append("Good morning!")
        elif hour < 17:
            greetings.append("Good afternoon!")
        else:
            greetings.append("Good evening!")
        
        # Journey progress
        greetings.append(
            f"You've been on this journey for {summary['days_on_journey']} days, "
            f"exploring {summary['verses_read']} verses."
        )
        
        # Suggest revisit
        revisit = self.profile.suggest_revisit_topics()
        if revisit:
            topic = revisit[0]
            greetings.append(
                f"You might want to revisit '{topic['topic']}' - {topic['reason']}."
            )
        
        # Recent milestone
        if summary['recent_milestones']:
            milestone = summary['recent_milestones'][-1]
            greetings.append(
                f"Recent milestone: {milestone['description']}."
            )
        
        return ' '.join(greetings)
    
    def get_weekly_reflection(self) -> Dict:
        """Generate a weekly reflection on your journey"""
        # Analyze recent questions
        recent_questions = [q['question'] for q in self.questions[-20:]]
        
        if recent_questions:
            analysis = self.analyzer.analyze_question_history(recent_questions)
            insights = self.analyzer.get_personalized_insights(analysis)
            suggestions = self.analyzer.suggest_next_study(analysis)
        else:
            analysis = {}
            insights = ["You haven't asked many questions yet. Start exploring!"]
            suggestions = []
        
        journey = self.profile.get_journey_summary()
        
        return {
            'journey_summary': journey,
            'recent_analysis': analysis,
            'personalized_insights': insights,
            'suggested_studies': suggestions,
            'active_struggles': self.profile.get_active_struggles(),
            'topics_to_revisit': self.profile.suggest_revisit_topics()
        }
    
    def record_reading(self, reference: str, notes: str = None):
        """Record that you've read a passage"""
        self.profile.record_verse_read(reference)
        
        if notes:
            # Analyze notes for insights
            analysis = self.analyzer.analyze_question(notes)
            for topic in analysis['topics']:
                self.profile.add_interest(topic, reference)
    
    def mark_understanding(self, topic: str, notes: str = ""):
        """Mark that you've gained understanding in an area"""
        self.profile.mark_breakthrough(topic, notes)
    
    def get_journey_stats(self) -> Dict:
        """Get your complete journey statistics"""
        return {
            'profile_summary': self.profile.get_journey_summary(),
            'questions_asked': len(self.questions),
            'topics_explored': len(self.profile.profile.interests),
            'struggles_faced': len(self.profile.profile.struggles),
            'breakthroughs': sum(
                1 for s in self.profile.profile.struggles.values() 
                if s.breakthrough
            ),
            'top_interests': self.profile.get_top_interests(5),
            'active_struggles': self.profile.get_active_struggles()
        }


# Global instance
_twin_instance: Optional[AITwin] = None


def get_twin(data_dir: str = None) -> AITwin:
    """Get or create the global AI Twin instance"""
    global _twin_instance
    if _twin_instance is None:
        _twin_instance = AITwin(data_dir)
    return _twin_instance


if __name__ == "__main__":
    # Test the AI Twin
    twin = get_twin()
    
    print("=" * 60)
    print("AI TWIN TEST")
    print("=" * 60)
    
    # Test daily greeting
    print("\nDAILY GREETING:")
    print(twin.get_daily_greeting())
    
    # Test asking questions
    print("\nASKING QUESTIONS:")
    
    questions = [
        "What does it mean to be born again?",
        "Why does God allow suffering?",
        "I don't understand the Trinity - how can God be three persons?",
        "How does Jesus fulfill the Passover?",
        "What did Augustine say about grace?"
    ]
    
    for q in questions:
        print(f"\nQ: {q}")
        result = twin.ask(q)
        print(f"Response: {result['personal_response']}")
    
    # Test weekly reflection
    print("\n" + "=" * 60)
    print("WEEKLY REFLECTION:")
    reflection = twin.get_weekly_reflection()
    
    print(f"\nJourney Summary: {reflection['journey_summary']}")
    print(f"\nInsights: {reflection['personalized_insights']}")
    print(f"\nSuggested Studies: {reflection['suggested_studies']}")
    
    # Test journey stats
    print("\n" + "=" * 60)
    print("JOURNEY STATS:")
    stats = twin.get_journey_stats()
    print(json.dumps(stats, indent=2, default=str))
