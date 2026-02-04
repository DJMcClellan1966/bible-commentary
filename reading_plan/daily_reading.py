"""
Daily Reading - Generates the complete daily reading experience

Brings together:
- The day's passage from the chronological plan
- Monthly theme connection
- Deep interconnections (backward, forward, typological)
- Church Fathers wisdom
- Reflection questions
"""

import sys
import os
from datetime import date
from typing import Dict, Optional
from dataclasses import dataclass

# Add parent for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from .chronological_plan import ChronologicalPlan, ReadingDay, get_reading_plan
from .themes import get_theme_for_date, MonthlyTheme


@dataclass
class DailyReading:
    """Complete daily reading with all enrichments"""
    # Basic info
    date: date
    day_number: int
    
    # Reading
    passages: list
    title: str
    passage_text: str  # Actual verse text
    
    # Context
    salvation_history_context: str
    monthly_theme: MonthlyTheme
    
    # Interconnections
    backward_links: list  # Earlier Scripture this echoes
    forward_links: list   # Later Scripture this points to
    typological: list     # Type/antitype connections
    connection_to_christ: str
    
    # Wisdom
    church_fathers: list
    key_verse: str
    
    # Daily reflection in the style of the Church Fathers
    patristic_summary: str  # Themes, echoes past/future, impact on Christ
    
    # Reflection
    reflection_questions: list
    
    # Progress
    progress_percentage: float
    current_period: str


class DailyReadingGenerator:
    """
    Generates the complete daily reading experience.
    """
    
    def __init__(self, bible_data: Dict = None, interconnection_engine=None):
        """
        Initialize the generator.
        
        Args:
            bible_data: Dictionary of {reference: text} for verse lookup
            interconnection_engine: Optional InterconnectionEngine instance
        """
        self.bible_data = bible_data or {}
        self.plan = get_reading_plan()
        
        # Try to import interconnection engine
        self.interconnection_engine = interconnection_engine
        if interconnection_engine is None:
            try:
                from interconnection_engine import InterconnectionEngine
                self.interconnection_engine = InterconnectionEngine(bible_data)
            except ImportError:
                self.interconnection_engine = None
    
    def get_todays_reading(self) -> Optional[DailyReading]:
        """Get today's complete reading"""
        return self.get_reading_for_date(date.today())
    
    def get_reading_for_date(self, d: date) -> Optional[DailyReading]:
        """Get complete reading for a specific date"""
        reading = self.plan.get_reading_for_date(d)
        if not reading:
            return None
        
        return self._build_daily_reading(reading, d)
    
    def get_reading_for_day(self, day_number: int) -> Optional[DailyReading]:
        """Get complete reading for a specific day number"""
        reading = self.plan.get_reading_for_day(day_number)
        if not reading:
            return None
        
        return self._build_daily_reading(reading, reading.date)
    
    def _build_daily_reading(self, reading: ReadingDay, d: date) -> DailyReading:
        """Build the complete daily reading from a ReadingDay"""
        
        # Get monthly theme
        theme = get_theme_for_date(d)
        
        # Get passage text
        passage_text = self._get_passage_text(reading.passages)
        
        # Get interconnections
        backward_links = []
        forward_links = []
        typological = []
        church_fathers = []
        rich_christ_connection = ""
        themes = []
        
        if self.interconnection_engine and passage_text:
            try:
                interconnected = self.interconnection_engine.get_interconnections(
                    reading.passages[0] if reading.passages else "",
                    passage_text
                )
                backward_links = [
                    {'reference': c.reference, 'text': c.text, 'explanation': c.explanation, 'church_fathers': getattr(c, 'church_fathers', None) or []}
                    for c in (interconnected.backward_links or [])
                ]
                forward_links = [
                    {'reference': c.reference, 'text': c.text, 'explanation': c.explanation, 'church_fathers': getattr(c, 'church_fathers', None) or []}
                    for c in (interconnected.forward_links or [])
                ]
                typological = interconnected.typological or []
                church_fathers = interconnected.church_fathers or []
                rich_christ_connection = interconnected.christ_connection or ""
                themes = getattr(interconnected, 'themes', None) or []
            except Exception:
                pass  # Gracefully handle if interconnection fails
        
        # Use rich Christ connection if available, otherwise use reading's
        christ_connection = rich_christ_connection if rich_christ_connection else reading.connection_to_christ
        
        # Daily summary in the style of the Church Fathers: themes, echoes past/future, impact on Christ
        patristic_summary = self._generate_patristic_summary(
            title=reading.title,
            passage_ref=reading.passages[0] if reading.passages else "",
            salvation_history_context=reading.salvation_history_context,
            connection_to_christ=christ_connection,
            backward_links=backward_links,
            forward_links=forward_links,
            typological=typological,
            themes=themes,
            key_verse=reading.key_verse,
        )
        
        # Generate reflection questions based on passage and theme
        reflection_questions = self._generate_reflection_questions(
            reading, theme, passage_text
        )
        
        # Get progress
        progress = self.plan.get_progress(d)
        
        return DailyReading(
            date=d,
            day_number=reading.day_number,
            passages=reading.passages,
            title=reading.title,
            passage_text=passage_text,
            salvation_history_context=reading.salvation_history_context,
            monthly_theme=theme,
            backward_links=backward_links,
            forward_links=forward_links,
            typological=typological,
            connection_to_christ=christ_connection,
            church_fathers=church_fathers,
            key_verse=reading.key_verse,
            patristic_summary=patristic_summary,
            reflection_questions=reflection_questions,
            progress_percentage=progress['percentage'],
            current_period=progress['current_period']['name'] if progress['current_period'] else ""
        )
    
    def _get_passage_text(self, passages: list) -> str:
        """Get the text for passages"""
        if not passages or not self.bible_data:
            return ""
        
        texts = []
        for passage in passages:
            # Try exact match first
            if passage in self.bible_data:
                texts.append(self.bible_data[passage])
            else:
                # Try to find verses that match the chapter
                # e.g., "Genesis 1:1-31" should find Genesis 1:1, Genesis 1:2, etc.
                matching = [
                    text for ref, text in self.bible_data.items()
                    if ref.startswith(passage.split(':')[0])
                ]
                if matching:
                    texts.extend(matching[:10])  # Limit to avoid huge text
        
        return '\n'.join(texts) if texts else ""
    
    def _generate_reflection_questions(
        self, 
        reading: ReadingDay, 
        theme: MonthlyTheme,
        passage_text: str
    ) -> list:
        """Generate reflection questions for the day"""
        questions = []
        
        # Theme-based question
        if theme.reflection_questions:
            questions.append(theme.reflection_questions[0])
        
        # Passage-specific questions based on keywords
        passage_lower = passage_text.lower() if passage_text else ""
        
        if 'promise' in passage_lower or 'covenant' in passage_lower:
            questions.append("What promises is God making here, and how do they apply to you?")
        
        if 'faith' in passage_lower or 'believe' in passage_lower:
            questions.append("What does this passage teach about faith? Where do you need more faith?")
        
        if 'love' in passage_lower:
            questions.append("How does this passage reveal God's love? How can you show this love to others?")
        
        if 'sin' in passage_lower or 'transgression' in passage_lower:
            questions.append("What does this passage show about sin and its consequences?")
        
        if 'prayer' in passage_lower or 'prayed' in passage_lower:
            questions.append("What does this teach about prayer? How can you apply it today?")
        
        # Connection to Christ question
        if reading.connection_to_christ:
            questions.append("How does this passage point to or reveal Christ?")
        
        # Default question
        if len(questions) < 3:
            questions.append("What is God saying to you through this passage today?")
            questions.append("How will you respond to what you've read?")
        
        return questions[:4]  # Max 4 questions
    
    def _generate_patristic_summary(
        self,
        title: str,
        passage_ref: str,
        salvation_history_context: str,
        connection_to_christ: str,
        backward_links: list,
        forward_links: list,
        typological: list,
        themes: list,
        key_verse: str,
    ) -> str:
        """
        Generate a daily summary in the style of the Church Fathers: theological,
        tying themes to the whole of Scripture, echoing past and future, and
        showing impact on Christ's life and ministry.
        """
        parts = []
        
        # Opening: what this passage is in the divine economy
        if salvation_history_context:
            parts.append(
                f"This portion of Holy Scripture—{title}—finds its place in the divine economy as {salvation_history_context.lower().rstrip('.')}."
            )
        else:
            parts.append(
                f"The Fathers saw in {title} a word that speaks to the whole of redemption."
            )
        
        # Themes, if we have them
        if themes:
            theme_str = ", ".join(themes[:4])
            parts.append(
                f"Here the great themes of {theme_str} are woven together, echoing what went before and prefiguring what was to come."
            )
        
        # Echoes of the past (backward links)
        if backward_links:
            refs = [link.get("reference", "") for link in backward_links[:2] if link.get("reference")]
            if refs:
                ref_str = " and ".join(refs) if len(refs) == 2 else refs[0]
                parts.append(
                    f"What was revealed in {ref_str} is recalled and deepened here, for God does not speak in fragments but in one unfolding mystery."
                )
        
        # Pointing forward and typology
        if forward_links or typological:
            if typological:
                t = typological[0]
                type_name = t.get("type_name", "the type")
                antitype_name = t.get("antitype_name", "the fulfillment")
                parts.append(
                    f"As {type_name} finds its fulfillment in {antitype_name}, so this passage looks toward the fullness of time."
                )
            elif forward_links:
                refs = [link.get("reference", "") for link in forward_links[:2] if link.get("reference")]
                if refs:
                    ref_str = " and ".join(refs) if len(refs) == 2 else refs[0]
                    parts.append(
                        f"It points forward to {ref_str}, for the same Spirit who spoke then was at work in the apostles and in the Church."
                    )
        
        # Connection to Christ's life and ministry
        if connection_to_christ:
            # Slightly rephrase so it reads as the conclusion of the reflection
            christ = connection_to_christ.strip()
            if not christ.endswith("."):
                christ += "."
            parts.append(
                f"Above all, the Fathers teach that this word touches the life and ministry of our Lord: {christ}"
            )
        else:
            parts.append(
                "In the incarnation, passion, and resurrection of the Word, these shadows find their substance and this promise its Yes."
            )
        
        return " ".join(parts)
    
    def format_for_display(self, reading: DailyReading) -> str:
        """Format the daily reading for text display"""
        lines = []
        
        # Header
        lines.append("=" * 70)
        lines.append(f"DAY {reading.day_number} | {reading.date.strftime('%B %d, %Y')}")
        lines.append(f"Theme: {reading.monthly_theme.name}")
        lines.append(f"Period: {reading.current_period}")
        lines.append("=" * 70)
        lines.append("")
        
        # Passage
        lines.append(f"TODAY'S READING: {', '.join(reading.passages)}")
        lines.append(f"\"{reading.title}\"")
        lines.append("")
        
        if reading.passage_text:
            lines.append(reading.passage_text[:500] + "..." if len(reading.passage_text) > 500 else reading.passage_text)
            lines.append("")
        
        # Patristic summary
        if getattr(reading, "patristic_summary", None):
            lines.append("-" * 70)
            lines.append("DAILY REFLECTION (in the spirit of the Fathers)")
            lines.append("-" * 70)
            lines.append(reading.patristic_summary)
            lines.append("")
        
        # Context
        lines.append("-" * 70)
        lines.append("WHERE THIS FITS")
        lines.append("-" * 70)
        lines.append(reading.salvation_history_context)
        lines.append("")
        
        # Key verse
        if reading.key_verse:
            lines.append(f"KEY VERSE: {reading.key_verse}")
            lines.append("")
        
        # Interconnections
        lines.append("-" * 70)
        lines.append("INTERCONNECTIONS")
        lines.append("-" * 70)
        
        if reading.backward_links:
            lines.append("\nLOOKING BACK (Earlier Scripture this echoes):")
            for link in reading.backward_links[:3]:
                lines.append(f"  -> {link['reference']}")
                lines.append(f"     {link['explanation']}")
        
        if reading.forward_links:
            lines.append("\nLOOKING FORWARD (Later Scripture this points to):")
            for link in reading.forward_links[:3]:
                lines.append(f"  -> {link['reference']}")
                lines.append(f"     {link['explanation']}")
        
        if reading.typological:
            lines.append("\nTYPOLOGY:")
            for typ in reading.typological[:2]:
                lines.append(f"  {typ.get('type_name', '')} -> {typ.get('antitype_name', '')}")
                lines.append(f"  {typ.get('connection_explanation', '')[:100]}...")
        
        if reading.connection_to_christ:
            lines.append(f"\nCONNECTION TO CHRIST:")
            lines.append(f"  {reading.connection_to_christ}")
        
        # Church Fathers
        if reading.church_fathers:
            lines.append("")
            lines.append("-" * 70)
            lines.append("CHURCH FATHERS")
            lines.append("-" * 70)
            for quote in reading.church_fathers[:2]:
                lines.append(f"\"{quote.get('quote', '')}\"")
                lines.append(f"  - {quote.get('author', '')}")
                lines.append("")
        
        # Reflection
        lines.append("-" * 70)
        lines.append("REFLECTION")
        lines.append("-" * 70)
        for i, q in enumerate(reading.reflection_questions, 1):
            lines.append(f"{i}. {q}")
        lines.append("")
        
        # Progress
        lines.append("-" * 70)
        lines.append(f"PROGRESS: {reading.progress_percentage}% through the year")
        lines.append("=" * 70)
        
        return '\n'.join(lines)


def get_todays_reading(bible_data: Dict = None) -> Optional[DailyReading]:
    """Convenience function to get today's reading"""
    generator = DailyReadingGenerator(bible_data)
    return generator.get_todays_reading()


if __name__ == "__main__":
    # Test the daily reading
    generator = DailyReadingGenerator()
    
    # Get Day 1 reading
    reading = generator.get_reading_for_day(1)
    if reading:
        print(generator.format_for_display(reading))
    
    # Get today's reading
    print("\n" + "=" * 70)
    print("TODAY'S READING")
    print("=" * 70)
    
    today_reading = generator.get_todays_reading()
    if today_reading:
        print(generator.format_for_display(today_reading))
    else:
        print("No reading found for today.")
