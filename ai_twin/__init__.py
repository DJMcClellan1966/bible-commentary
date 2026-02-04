"""
AI Twin - Your Personal Bible Study Companion

This module creates a personalized AI that:
- Learns your recurring questions and spiritual interests
- Tracks topics you struggle to understand
- Identifies patterns in what draws your attention
- Actually ANSWERS your theological questions with Scripture and Church Fathers
- Grows with you on your spiritual journey
"""

from .twin_core import AITwin, get_twin
from .question_analyzer import QuestionAnalyzer
from .profile_manager import ProfileManager
from .answer_engine import AnswerEngine

__all__ = ['AITwin', 'get_twin', 'QuestionAnalyzer', 'ProfileManager', 'AnswerEngine']
