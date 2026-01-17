"""
AI Agent for building and managing Bible commentaries
"""
from typing import List, Dict, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import logging
from config import OPENAI_API_KEY, AGENT_TEMPERATURE, MAX_TOKENS, ENABLE_LEARNING
from scraper import CommentaryScraper
from models import Commentary, SourceType, SessionLocal
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BibleCommentaryAgent:
    """AI Agent for building comprehensive Bible commentaries"""

    def __init__(self):
        self.scraper = CommentaryScraper()
        self.llm = None
        
        if OPENAI_API_KEY:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    temperature=AGENT_TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                    model="gpt-4"  # or "gpt-3.5-turbo" for faster/cheaper
                )
            except Exception as e:
                logger.warning(f"Could not initialize LLM: {e}")
                self.llm = None
        else:
            logger.warning("No OpenAI API key found. Some features will be limited.")
            self.llm = None

    def _categorize_source(self, source_name: str, source_url: str = "") -> SourceType:
        """Categorize a source into appropriate type"""
        source_lower = (source_name + source_url).lower()
        
        if any(term in source_lower for term in ["father", "patristic", "augustine", "chrysostom", "jerome"]):
            return SourceType.CHURCH_FATHERS
        elif any(term in source_lower for term in ["aquinas", "medieval", "scholastic", "middle age"]):
            return SourceType.MIDDLE_AGES
        elif any(term in source_lower for term in ["jewish", "rabbi", "talmud", "sefaria", "chabad"]):
            return SourceType.JEWISH
        elif any(term in source_lower for term in ["pope", "vatican", "encyclical", "papal"]):
            return SourceType.POPES
        else:
            return SourceType.MODERN

    def _synthesize_commentaries(self, commentaries: List[Dict], book: str, chapter: int, verse: int) -> str:
        """Use AI to synthesize multiple commentaries into a comprehensive reading"""
        if not self.llm or not commentaries:
            # Fallback: just combine all commentaries
            return "\n\n---\n\n".join([c["text"] for c in commentaries])
        
        try:
            # Prepare context
            commentary_texts = "\n\n".join([
                f"[Source: {c.get('author', 'Unknown')} - {c.get('source', 'Unknown')}]\n{c['text']}"
                for c in commentaries
            ])
            
            prompt = PromptTemplate(
                input_variables=["book", "chapter", "verse", "commentaries"],
                template="""
You are an expert Bible scholar synthesizing commentaries on {book} {chapter}:{verse}.

Below are multiple commentaries from different sources (Church Fathers, Medieval scholars, Modern scholars, Jewish sources, etc.):

{commentaries}

Please synthesize these commentaries into a comprehensive, coherent commentary that:
1. Brings out the underlying messages and themes
2. Enhances understanding of the biblical text
3. Integrates insights from different traditions and time periods
4. Highlights key theological, historical, and literary points
5. Maintains accuracy and respect for all source traditions

Provide a well-structured, insightful commentary that helps readers understand the deeper meaning of this verse.
"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            result = chain.run(
                book=book,
                chapter=chapter,
                verse=verse,
                commentaries=commentary_texts
            )
            
            return result
        except Exception as e:
            logger.error(f"Error synthesizing commentaries: {e}")
            # Fallback to simple combination
            return "\n\n---\n\n".join([c["text"] for c in commentaries])

    def build_commentary(self, book: str, chapter: int, verse: int, 
                        source_types: List[str] = None, synthesize: bool = True) -> Dict:
        """Build a comprehensive commentary for a specific verse"""
        logger.info(f"Building commentary for {book} {chapter}:{verse}")
        
        # Check database first
        db = SessionLocal()
        try:
            existing = db.query(Commentary).filter(
                Commentary.book == book,
                Commentary.chapter == chapter,
                Commentary.verse == verse
            ).all()
            
            if existing and not synthesize:
                # Return existing without re-scraping
                return {
                    "book": book,
                    "chapter": chapter,
                    "verse": verse,
                    "commentaries": [
                        {
                            "text": c.commentary_text,
                            "source_type": c.source_type.value,
                            "author": c.author,
                            "source": c.source_name
                        }
                        for c in existing
                    ]
                }
        finally:
            db.close()
        
        # Scrape new commentaries
        scraped_commentaries = self.scraper.scrape_verse(book, chapter, verse, source_types)
        
        # Save to database
        db = SessionLocal()
        try:
            saved_commentaries = []
            for comm in scraped_commentaries:
                source_type = self._categorize_source(comm.get("author", ""), comm.get("url", ""))
                
                commentary = Commentary(
                    book=book,
                    chapter=chapter,
                    verse=verse,
                    commentary_text=comm["text"],
                    source_type=source_type,
                    source_name=comm.get("source", "Unknown"),
                    source_url=comm.get("url"),
                    author=comm.get("author", "Unknown")
                )
                db.add(commentary)
                saved_commentaries.append(commentary)
            
            db.commit()
            
            # Synthesize if requested
            if synthesize and saved_commentaries:
                synthesized_text = self._synthesize_commentaries(
                    [{"text": c.commentary_text, "author": c.author, "source": c.source_name} 
                     for c in saved_commentaries],
                    book, chapter, verse
                )
            else:
                synthesized_text = None
            
            return {
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "commentaries": [
                    {
                        "text": c.commentary_text,
                        "source_type": c.source_type.value,
                        "author": c.author,
                        "source": c.source_name,
                        "url": c.source_url
                    }
                    for c in saved_commentaries
                ],
                "synthesized": synthesized_text
            }
        finally:
            db.close()

    def search_commentaries(self, query: str, book: str = None, 
                           chapter: int = None, verse: int = None,
                           source_types: List[str] = None) -> List[Dict]:
        """Search for commentaries using natural language query"""
        db = SessionLocal()
        try:
            query_obj = db.query(Commentary)
            
            if book:
                query_obj = query_obj.filter(Commentary.book == book)
            if chapter:
                query_obj = query_obj.filter(Commentary.chapter == chapter)
            if verse:
                query_obj = query_obj.filter(Commentary.verse == verse)
            if source_types:
                source_enums = [SourceType(st) for st in source_types]
                query_obj = query_obj.filter(Commentary.source_type.in_(source_enums))
            
            # Simple text search (can be enhanced with full-text search)
            if query:
                query_obj = query_obj.filter(Commentary.commentary_text.contains(query))
            
            results = query_obj.all()
            
            return [
                {
                    "book": r.book,
                    "chapter": r.chapter,
                    "verse": r.verse,
                    "text": r.commentary_text,
                    "source_type": r.source_type.value,
                    "author": r.author,
                    "source": r.source_name,
                    "url": r.source_url
                }
                for r in results
            ]
        finally:
            db.close()

    def get_commentary_by_category(self, book: str, chapter: int, verse: int,
                                   category: str) -> Dict:
        """Get commentary filtered by category (church_fathers, middle_ages, modern, etc.)"""
        db = SessionLocal()
        try:
            source_type = SourceType(category)
            commentaries = db.query(Commentary).filter(
                Commentary.book == book,
                Commentary.chapter == chapter,
                Commentary.verse == verse,
                Commentary.source_type == source_type
            ).all()
            
            return {
                "book": book,
                "chapter": chapter,
                "verse": verse,
                "category": category,
                "commentaries": [
                    {
                        "text": c.commentary_text,
                        "author": c.author,
                        "source": c.source_name,
                        "url": c.source_url
                    }
                    for c in commentaries
                ]
            }
        finally:
            db.close()

    def suggest_improvements(self, book: str, chapter: int, verse: int) -> List[str]:
        """Use AI to suggest improvements and better methods for commentary collection"""
        if not self.llm:
            return ["Enable AI features by setting OPENAI_API_KEY for improvement suggestions"]
        
        try:
            db = SessionLocal()
            existing = db.query(Commentary).filter(
                Commentary.book == book,
                Commentary.chapter == chapter,
                Commentary.verse == verse
            ).all()
            db.close()
            
            prompt = PromptTemplate(
                input_variables=["book", "chapter", "verse", "count"],
                template="""
You are an expert Bible commentary researcher. For {book} {chapter}:{verse}, 
we currently have {count} commentary sources.

Suggest:
1. Additional sources we should consider (specific authors, websites, databases)
2. Better methods for finding commentaries
3. Specific search terms or approaches
4. Any gaps in our current coverage (e.g., missing perspectives from certain traditions)

Provide practical, actionable suggestions.
"""
            )
            
            chain = LLMChain(llm=self.llm, prompt=prompt)
            suggestions = chain.run(
                book=book,
                chapter=chapter,
                verse=verse,
                count=len(existing)
            )
            
            return suggestions.split("\n") if isinstance(suggestions, str) else [suggestions]
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return [f"Error generating suggestions: {e}"]
