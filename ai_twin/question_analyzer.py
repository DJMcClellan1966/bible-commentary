"""
Question Analyzer - Extracts topics, patterns, and insights from your questions
"""
import re
from typing import List, Dict, Tuple
from datetime import datetime
from collections import defaultdict
import json
import os


class QuestionAnalyzer:
    """
    Analyzes your questions to understand what you're really seeking.
    
    - Extracts topics and themes
    - Identifies patterns in your questioning
    - Detects struggles and breakthroughs
    - Learns your spiritual interests
    """
    
    def __init__(self):
        # Spiritual/theological topics to detect
        self.topic_patterns = {
            # Core doctrines
            'trinity': ['trinity', 'three persons', 'godhead', 'father son spirit'],
            'salvation': ['salvation', 'saved', 'born again', 'eternal life', 'redemption'],
            'grace': ['grace', 'unmerited', 'favor', 'gift of god'],
            'faith': ['faith', 'believe', 'trust', 'confidence in'],
            'sin': ['sin', 'transgression', 'fall', 'original sin', 'wickedness'],
            'forgiveness': ['forgiveness', 'forgive', 'pardon', 'absolution'],
            'resurrection': ['resurrection', 'rise again', 'raised from dead'],
            'incarnation': ['incarnation', 'became flesh', 'word made flesh'],
            'atonement': ['atonement', 'sacrifice', 'propitiation', 'expiation'],
            'justification': ['justification', 'justified', 'made righteous'],
            'sanctification': ['sanctification', 'holy', 'set apart', 'purification'],
            
            # Practices
            'prayer': ['prayer', 'pray', 'petition', 'intercession'],
            'worship': ['worship', 'praise', 'adoration', 'liturgy'],
            'eucharist': ['eucharist', 'communion', 'lord\'s supper', 'bread and wine'],
            'baptism': ['baptism', 'baptize', 'baptised', 'immersion'],
            'confession': ['confession', 'confess', 'reconciliation'],
            
            # Bible study
            'interpretation': ['interpret', 'meaning', 'understand', 'what does it mean'],
            'typology': ['type', 'antitype', 'prefigure', 'foreshadow', 'symbol'],
            'prophecy': ['prophecy', 'prophet', 'foretold', 'prediction'],
            'covenant': ['covenant', 'promise', 'oath', 'testament'],
            
            # Life topics
            'suffering': ['suffering', 'pain', 'hardship', 'trial', 'why does god allow'],
            'purpose': ['purpose', 'calling', 'vocation', 'why am i here'],
            'relationships': ['marriage', 'family', 'friendship', 'love others'],
            'work': ['work', 'job', 'career', 'vocation'],
            'money': ['money', 'wealth', 'possessions', 'materialism', 'giving'],
            'death': ['death', 'dying', 'afterlife', 'heaven', 'hell'],
            'evil': ['evil', 'devil', 'satan', 'demons', 'spiritual warfare'],
            'anxiety': ['anxiety', 'worry', 'fear', 'stress', 'peace'],
            'doubt': ['doubt', 'uncertain', 'struggle to believe', 'hard to accept'],
            
            # Historical
            'church_fathers': ['church fathers', 'patristic', 'early church', 'augustine', 'aquinas'],
            'church_history': ['church history', 'councils', 'reformation', 'tradition'],
            
            # Figures
            'jesus': ['jesus', 'christ', 'messiah', 'lord', 'savior'],
            'moses': ['moses', 'law of moses', 'exodus', 'ten commandments'],
            'paul': ['paul', 'apostle paul', 'pauline'],
            'mary': ['mary', 'mother of god', 'virgin mary', 'blessed mother'],
            'david': ['david', 'king david', 'house of david'],
            'abraham': ['abraham', 'father abraham', 'abrahamic']
        }
        
        # Question type patterns
        self.question_types = {
            'what': r'\bwhat\b',
            'why': r'\bwhy\b',
            'how': r'\bhow\b',
            'who': r'\bwho\b',
            'when': r'\bwhen\b',
            'where': r'\bwhere\b',
            'meaning': r'\b(mean|meaning|significance)\b',
            'connection': r'\b(connect|relate|link|between)\b',
            'application': r'\b(apply|practical|life|today)\b',
            'comparison': r'\b(difference|compare|versus|vs)\b',
            'explanation': r'\b(explain|understand|clarify)\b'
        }
        
        # Struggle indicators
        self.struggle_indicators = [
            'don\'t understand',
            'confused about',
            'hard to believe',
            'struggling with',
            'can\'t grasp',
            'makes no sense',
            'how can',
            'why would',
            'doesn\'t seem',
            'trouble with',
            'difficult to',
            'always wondered',
            'never understood'
        ]
        
        # Breakthrough indicators
        self.breakthrough_indicators = [
            'finally understand',
            'now i see',
            'makes sense now',
            'clicked for me',
            'realized that',
            'breakthrough',
            'eye-opening',
            'now i get it'
        ]
    
    def analyze_question(self, question: str) -> Dict:
        """
        Analyze a single question.
        
        Returns:
            Dict with topics, question_type, is_struggle, insights
        """
        question_lower = question.lower()
        
        # Extract topics
        topics = []
        for topic, patterns in self.topic_patterns.items():
            if any(pattern in question_lower for pattern in patterns):
                topics.append(topic)
        
        # Determine question type
        question_type = 'general'
        for q_type, pattern in self.question_types.items():
            if re.search(pattern, question_lower):
                question_type = q_type
                break
        
        # Check for struggle indicators
        is_struggle = any(indicator in question_lower for indicator in self.struggle_indicators)
        
        # Check for breakthrough indicators
        is_breakthrough = any(indicator in question_lower for indicator in self.breakthrough_indicators)
        
        # Extract verse references
        verse_refs = self._extract_verse_references(question)
        
        return {
            'question': question,
            'topics': topics if topics else ['general'],
            'question_type': question_type,
            'is_struggle': is_struggle,
            'is_breakthrough': is_breakthrough,
            'verse_references': verse_refs,
            'timestamp': datetime.now().isoformat()
        }
    
    def _extract_verse_references(self, text: str) -> List[str]:
        """Extract Bible verse references from text"""
        # Pattern for book chapter:verse (e.g., John 3:16, 1 Corinthians 13:4-7)
        pattern = r'\b(\d?\s*[A-Za-z]+)\s+(\d+):(\d+)(?:-\d+)?\b'
        matches = re.findall(pattern, text)
        
        refs = []
        for match in matches:
            book = match[0].strip()
            chapter = match[1]
            verse = match[2]
            refs.append(f"{book} {chapter}:{verse}")
        
        return refs
    
    def analyze_question_history(self, questions: List[str]) -> Dict:
        """
        Analyze a history of questions to find patterns.
        
        Returns:
            Dict with topic_frequencies, recurring_themes, struggles, growth_areas
        """
        topic_counts = defaultdict(int)
        question_types = defaultdict(int)
        struggles = []
        breakthroughs = []
        all_analyses = []
        
        for question in questions:
            analysis = self.analyze_question(question)
            all_analyses.append(analysis)
            
            for topic in analysis['topics']:
                topic_counts[topic] += 1
            
            question_types[analysis['question_type']] += 1
            
            if analysis['is_struggle']:
                struggles.append({
                    'question': question,
                    'topics': analysis['topics']
                })
            
            if analysis['is_breakthrough']:
                breakthroughs.append({
                    'question': question,
                    'topics': analysis['topics']
                })
        
        # Find recurring themes (topics mentioned 3+ times)
        recurring_themes = [
            topic for topic, count in topic_counts.items()
            if count >= 3
        ]
        
        # Identify struggle areas
        struggle_topics = defaultdict(int)
        for s in struggles:
            for topic in s['topics']:
                struggle_topics[topic] += 1
        
        persistent_struggles = [
            topic for topic, count in struggle_topics.items()
            if count >= 2
        ]
        
        return {
            'total_questions': len(questions),
            'topic_frequencies': dict(topic_counts),
            'question_type_distribution': dict(question_types),
            'recurring_themes': recurring_themes,
            'struggles': struggles,
            'persistent_struggle_areas': persistent_struggles,
            'breakthroughs': breakthroughs,
            'top_interests': sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        }
    
    def get_personalized_insights(self, analysis: Dict) -> List[str]:
        """
        Generate personalized insights based on question analysis.
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Comment on top interests
        if analysis.get('top_interests'):
            top_topic = analysis['top_interests'][0][0]
            count = analysis['top_interests'][0][1]
            insights.append(
                f"You've shown deep interest in '{top_topic}' - you've explored this {count} times. "
                f"This seems to be a core area of your spiritual journey."
            )
        
        # Comment on question types
        q_types = analysis.get('question_type_distribution', {})
        if q_types.get('why', 0) > q_types.get('what', 0):
            insights.append(
                "You tend to ask 'why' questions more than 'what' questions. "
                "This suggests you're seeking deeper understanding, not just information."
            )
        if q_types.get('application', 0) > 2:
            insights.append(
                "You often ask about practical application. "
                "You want Scripture to transform your daily life, not just your knowledge."
            )
        
        # Comment on struggles
        if analysis.get('persistent_struggle_areas'):
            struggle = analysis['persistent_struggle_areas'][0]
            insights.append(
                f"You've wrestled with '{struggle}' multiple times. "
                f"This is a sign of genuine seeking - don't give up. "
                f"Consider exploring what the Church Fathers said about this."
            )
        
        # Comment on breakthroughs
        if analysis.get('breakthroughs'):
            insights.append(
                f"You've had {len(analysis['breakthroughs'])} breakthrough moments! "
                f"These are milestones in your journey. "
                f"Consider journaling about what led to these realizations."
            )
        
        # Suggest connections
        if analysis.get('recurring_themes'):
            themes = analysis['recurring_themes'][:3]
            if len(themes) >= 2:
                insights.append(
                    f"Your interests in {', '.join(themes)} are actually deeply connected in Scripture. "
                    f"Consider exploring how these themes weave together."
                )
        
        return insights
    
    def suggest_next_study(self, analysis: Dict) -> Dict:
        """
        Suggest what to study next based on patterns.
        
        Returns:
            Dict with suggested_topic, reason, starting_verses
        """
        suggestions = []
        
        # Suggest based on struggles
        if analysis.get('persistent_struggle_areas'):
            topic = analysis['persistent_struggle_areas'][0]
            suggestions.append({
                'topic': topic,
                'reason': f"You've been wrestling with {topic}. Deeper study here could bring breakthrough.",
                'approach': 'Try reading what Augustine or Chrysostom wrote about this topic.',
                'priority': 'high'
            })
        
        # Suggest based on interests
        if analysis.get('top_interests'):
            for topic, count in analysis['top_interests'][:2]:
                if topic not in [s['topic'] for s in suggestions]:
                    suggestions.append({
                        'topic': topic,
                        'reason': f"This clearly resonates with you ({count} explorations). Go deeper!",
                        'approach': 'Trace this theme from Genesis through Revelation.',
                        'priority': 'medium'
                    })
        
        # Suggest something new if they've been focused
        focused_topics = [t for t, c in analysis.get('topic_frequencies', {}).items() if c >= 3]
        if len(focused_topics) <= 2:
            unexplored = set(self.topic_patterns.keys()) - set(analysis.get('topic_frequencies', {}).keys())
            if unexplored:
                new_topic = list(unexplored)[0]
                suggestions.append({
                    'topic': new_topic,
                    'reason': "Broadening your study brings new perspectives.",
                    'approach': 'Start with a key passage and see how it connects to your existing interests.',
                    'priority': 'low'
                })
        
        return suggestions[:3]  # Top 3 suggestions
