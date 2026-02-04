"""
Answer Engine - Generates actual answers to theological questions

Uses:
- Interconnection engine to find relevant Scripture
- Church Fathers quotes database
- Typology connections
- Optional LLM for natural language generation
"""

import os
import sys
import json
from typing import Dict, List, Optional

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Try to import the interconnection engine
try:
    from interconnection_engine import InterconnectionEngine
    INTERCONNECTION_AVAILABLE = True
except ImportError:
    INTERCONNECTION_AVAILABLE = False

# Try to import LLM capabilities
try:
    import config
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False


class AnswerEngine:
    """
    Generates grounded answers to theological questions.
    
    Answers are built from:
    1. Relevant Scripture passages
    2. Church Fathers wisdom
    3. Typological connections
    4. Historical perspective
    """
    
    def __init__(self, bible_data: Dict = None):
        """
        Initialize the answer engine.
        
        Args:
            bible_data: Dictionary of {reference: text} for verse lookup
        """
        self.bible_data = bible_data or {}
        
        # Load Church Fathers quotes
        self.church_fathers = self._load_church_fathers()
        
        # Load typology database
        self.typology = self._load_typology()
        
        # Initialize interconnection engine if available
        self.interconnection_engine = None
        if INTERCONNECTION_AVAILABLE:
            try:
                self.interconnection_engine = InterconnectionEngine(bible_data)
            except Exception:
                pass
        
        # Theological knowledge base for common questions
        self.knowledge_base = self._build_knowledge_base()
    
    def _load_church_fathers(self) -> Dict:
        """Load Church Fathers quotes"""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'church_fathers_quotes.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'quotes_by_verse': {}, 'quotes_by_theme': {}, 'authors': {}}
    
    def _load_typology(self) -> Dict:
        """Load typology database"""
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'typology.json')
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {'types': [], 'thematic_connections': {}}
    
    def _build_knowledge_base(self) -> Dict:
        """Build knowledge base for common theological questions"""
        return {
            'born again': {
                'key_verses': ['John 3:3-7', 'John 1:12-13', '1 Peter 1:23', '2 Corinthians 5:17', 'Titus 3:5'],
                'explanation': (
                    "To be 'born again' (Greek: gennao anothen) means to be spiritually reborn from above. "
                    "Jesus told Nicodemus that no one can see the kingdom of God without this new birth. "
                    "It is not physical rebirth, but a spiritual regeneration by the Holy Spirit. "
                    "Through faith in Christ, we become new creations - the old passes away, and the new comes."
                ),
                'church_fathers_topic': 'salvation',
                'typology_connection': 'creation_new_creation'
            },
            'trinity': {
                'key_verses': ['Matthew 28:19', 'John 1:1-3', '2 Corinthians 13:14', 'Genesis 1:26', 'John 14:16-17'],
                'explanation': (
                    "The Trinity is the Christian doctrine that God is one Being in three Persons: "
                    "Father, Son, and Holy Spirit. Each Person is fully God, yet there is one God, not three. "
                    "This mystery is revealed throughout Scripture: the Father sends the Son, "
                    "the Son reveals the Father, and the Spirit proceeds from both to dwell in believers. "
                    "The early Church councils (Nicaea, Constantinople) articulated this against heresies."
                ),
                'church_fathers_topic': 'trinity',
                'typology_connection': None
            },
            'salvation': {
                'key_verses': ['Ephesians 2:8-9', 'Romans 3:23-24', 'John 14:6', 'Acts 4:12', 'Romans 10:9-10'],
                'explanation': (
                    "Salvation is deliverance from sin and its consequences through Jesus Christ. "
                    "Scripture teaches that all have sinned and fall short of God's glory, "
                    "but we are justified freely by His grace through the redemption in Christ Jesus. "
                    "Salvation is by grace through faith - not by works, lest anyone boast. "
                    "Christ is the only way to the Father; there is no other name by which we must be saved."
                ),
                'church_fathers_topic': 'salvation',
                'typology_connection': 'exodus_salvation'
            },
            'suffering': {
                'key_verses': ['Romans 8:28', 'James 1:2-4', '2 Corinthians 1:3-4', '1 Peter 4:12-13', 'Romans 5:3-5'],
                'explanation': (
                    "Scripture does not promise freedom from suffering, but purpose within it. "
                    "God works all things for good for those who love Him. Trials produce perseverance, "
                    "character, and hope. Christ Himself suffered, and we are called to share in His sufferings "
                    "that we may also share in His glory. The God of all comfort comforts us in our afflictions "
                    "so that we can comfort others."
                ),
                'church_fathers_topic': 'suffering',
                'typology_connection': None
            },
            'grace': {
                'key_verses': ['Ephesians 2:8-9', 'Romans 5:20-21', 'Titus 2:11', '2 Corinthians 12:9', 'John 1:16-17'],
                'explanation': (
                    "Grace (Greek: charis) is God's unmerited favor - a gift we cannot earn. "
                    "Where sin increased, grace abounded all the more. The grace of God has appeared, "
                    "bringing salvation to all people. Paul learned that God's grace is sufficient, "
                    "for His power is made perfect in weakness. From Christ's fullness we have all received "
                    "grace upon grace."
                ),
                'church_fathers_topic': 'salvation',
                'typology_connection': None
            },
            'faith': {
                'key_verses': ['Hebrews 11:1', 'Romans 10:17', 'James 2:17', 'Ephesians 2:8', 'Galatians 2:20'],
                'explanation': (
                    "Faith is the substance of things hoped for, the evidence of things not seen. "
                    "It comes by hearing, and hearing by the word of God. True faith is not merely intellectual assent "
                    "but trust that transforms - faith without works is dead. We are saved by grace through faith. "
                    "As Paul said, the life we now live, we live by faith in the Son of God who loved us."
                ),
                'church_fathers_topic': 'faith',
                'typology_connection': None
            },
            'eucharist': {
                'key_verses': ['John 6:53-56', 'Matthew 26:26-28', '1 Corinthians 11:23-26', 'Luke 22:19-20'],
                'explanation': (
                    "The Eucharist (Lord's Supper, Communion) was instituted by Christ at the Last Supper. "
                    "Jesus said 'This is my body' and 'This is my blood of the covenant.' "
                    "In John 6, Jesus taught that unless we eat His flesh and drink His blood, "
                    "we have no life in us. The early Church understood this as a real participation "
                    "in Christ's body and blood, not mere symbolism."
                ),
                'church_fathers_topic': 'eucharist',
                'typology_connection': 'manna_eucharist'
            },
            'baptism': {
                'key_verses': ['Matthew 28:19', 'Romans 6:3-4', '1 Peter 3:21', 'Acts 2:38', 'Galatians 3:27'],
                'explanation': (
                    "Baptism is the sacrament of initiation commanded by Christ. We are baptized into Christ's death "
                    "and raised to walk in newness of life. Peter says baptism now saves us - not the removal of dirt "
                    "but the pledge of a good conscience toward God through the resurrection of Christ. "
                    "In baptism we are clothed with Christ."
                ),
                'church_fathers_topic': 'baptism',
                'typology_connection': 'exodus_salvation'
            },
            'prayer': {
                'key_verses': ['Matthew 6:9-13', 'Philippians 4:6-7', '1 Thessalonians 5:17', 'James 5:16', 'Romans 8:26'],
                'explanation': (
                    "Prayer is conversation with God - both speaking and listening. Jesus taught us to pray "
                    "to our Father in heaven. We are to pray without ceasing, with thanksgiving, making our requests "
                    "known to God. The prayer of a righteous person has great power. When we don't know how to pray, "
                    "the Spirit intercedes for us with groanings too deep for words."
                ),
                'church_fathers_topic': 'prayer',
                'typology_connection': None
            },
            'resurrection': {
                'key_verses': ['1 Corinthians 15:3-8', 'Romans 6:5', 'John 11:25-26', '1 Corinthians 15:20-22', 'Philippians 3:10-11'],
                'explanation': (
                    "The resurrection of Christ is the foundation of Christian faith. If Christ has not been raised, "
                    "our faith is in vain. But Christ has been raised as the firstfruits of those who have fallen asleep. "
                    "As in Adam all die, so in Christ all will be made alive. Jesus said, 'I am the resurrection and the life; "
                    "whoever believes in me, though he die, yet shall he live.'"
                ),
                'church_fathers_topic': 'resurrection',
                'typology_connection': 'jonah_resurrection'
            },
            'mary': {
                'key_verses': ['Luke 1:28-38', 'Luke 1:46-55', 'John 2:1-11', 'John 19:26-27', 'Revelation 12:1'],
                'explanation': (
                    "Mary is the mother of Jesus, honored as the Theotokos (God-bearer) by the early Church. "
                    "The angel Gabriel greeted her as 'full of grace' and 'blessed among women.' "
                    "Her response - 'Let it be to me according to your word' - is the model of faith. "
                    "At Cana, she told the servants, 'Do whatever he tells you.' At the cross, "
                    "Jesus entrusted her to the beloved disciple."
                ),
                'church_fathers_topic': 'mary',
                'typology_connection': None
            }
        }
    
    def answer_question(self, question: str, topics: List[str] = None) -> Dict:
        """
        Generate a comprehensive answer to a theological question.
        
        Args:
            question: The question to answer
            topics: List of detected topics (from QuestionAnalyzer)
        
        Returns:
            Dict with answer, verses, church_fathers, and typology
        """
        question_lower = question.lower()
        
        # Find matching knowledge base entry
        matched_topic = None
        for topic, data in self.knowledge_base.items():
            if topic in question_lower:
                matched_topic = topic
                break
        
        # Also check topics parameter
        if not matched_topic and topics:
            for topic in topics:
                topic_lower = topic.lower()
                if topic_lower in self.knowledge_base:
                    matched_topic = topic_lower
                    break
        
        # Build the answer
        if matched_topic:
            return self._build_answer_from_knowledge_base(matched_topic, question)
        else:
            return self._build_general_answer(question, topics)
    
    def _build_answer_from_knowledge_base(self, topic: str, question: str) -> Dict:
        """Build answer from knowledge base"""
        data = self.knowledge_base[topic]
        
        # Get key verses with text if available
        verses = []
        for ref in data['key_verses']:
            text = self.bible_data.get(ref, "")
            verses.append({
                'reference': ref,
                'text': text if text else f"[{ref}]"
            })
        
        # Get Church Fathers quotes
        fathers_quotes = []
        fathers_topic = data.get('church_fathers_topic')
        if fathers_topic and fathers_topic in self.church_fathers.get('quotes_by_theme', {}):
            fathers_quotes = self.church_fathers['quotes_by_theme'][fathers_topic][:3]
        
        # Get typology connection
        typology_info = None
        typology_id = data.get('typology_connection')
        if typology_id:
            for t in self.typology.get('types', []):
                if t.get('id') == typology_id:
                    typology_info = {
                        'type': t['type']['name'],
                        'antitype': t['antitype']['name'],
                        'connection': t['connection']
                    }
                    break
        
        return {
            'answer': data['explanation'],
            'key_verses': verses,
            'church_fathers': fathers_quotes,
            'typology': typology_info,
            'topic': topic,
            'confidence': 'high'
        }
    
    def _build_general_answer(self, question: str, topics: List[str] = None) -> Dict:
        """Build answer for questions not in knowledge base"""
        answer_parts = []
        verses = []
        fathers_quotes = []
        
        # Try to find relevant content using interconnection engine
        if self.interconnection_engine and topics:
            for topic in topics[:2]:  # Check first 2 topics
                # Search Church Fathers by theme
                topic_lower = topic.lower()
                if topic_lower in self.church_fathers.get('quotes_by_theme', {}):
                    fathers_quotes.extend(self.church_fathers['quotes_by_theme'][topic_lower][:2])
        
        # Build a general response
        if topics:
            topic_str = ', '.join(topics[:3])
            answer_parts.append(
                f"Your question touches on {topic_str}. "
                f"Let me share what Scripture and the Church Fathers teach about this."
            )
        else:
            answer_parts.append(
                "This is a thoughtful question. Let me help you explore what Scripture teaches."
            )
        
        # Add suggestion to explore specific verses
        if not verses:
            answer_parts.append(
                "\n\nI'd encourage you to explore this topic further in Scripture. "
                "Consider searching for related passages in the Explore view, "
                "or ask about a specific verse for deeper interconnections."
            )
        
        return {
            'answer': ' '.join(answer_parts),
            'key_verses': verses,
            'church_fathers': fathers_quotes[:3] if fathers_quotes else [],
            'typology': None,
            'topic': topics[0] if topics else 'general',
            'confidence': 'medium' if topics else 'low'
        }
    
    def get_verse_explanation(self, reference: str) -> Dict:
        """Get explanation for a specific verse"""
        verse_text = self.bible_data.get(reference, "")
        
        # Get Church Fathers quotes for this verse
        fathers_quotes = self.church_fathers.get('quotes_by_verse', {}).get(reference, [])
        
        # Get interconnections if available
        interconnections = None
        if self.interconnection_engine:
            try:
                result = self.interconnection_engine.get_interconnections(reference, verse_text)
                interconnections = {
                    'backward_links': [
                        {'reference': c.reference, 'explanation': c.explanation}
                        for c in (result.backward_links or [])[:3]
                    ],
                    'forward_links': [
                        {'reference': c.reference, 'explanation': c.explanation}
                        for c in (result.forward_links or [])[:3]
                    ],
                    'typological': result.typological[:2] if result.typological else [],
                    'themes': result.themes
                }
            except Exception:
                pass
        
        return {
            'reference': reference,
            'text': verse_text,
            'church_fathers': fathers_quotes[:3],
            'interconnections': interconnections
        }
