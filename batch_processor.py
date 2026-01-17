"""
Batch processing utility for building commentaries for entire books or ranges
"""
import argparse
import json
import time
from typing import List, Tuple
from agent import BibleCommentaryAgent
from models import init_db, SessionLocal, Commentary
from config import BIBLE_BOOKS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chapter and verse counts for each book (approximate - you may want to use a Bible API)
BIBLE_STRUCTURE = {
    "Genesis": (50, [31, 25, 24, 26, 32, 22, 24, 22, 29, 32, 32, 20, 18, 24, 21, 16, 27, 33, 38, 18, 34, 24, 20, 67, 34, 35, 46, 22, 35, 43, 55, 32, 20, 31, 29, 43, 36, 30, 23, 23, 57, 38, 34, 34, 28, 34, 31, 22, 33, 26]),
    # Add more books as needed - this is a simplified structure
    # In production, use a proper Bible API or database
}


class BatchProcessor:
    """Process multiple verses in batch"""

    def __init__(self):
        self.agent = BibleCommentaryAgent()
        init_db()

    def get_verse_count(self, book: str, chapter: int) -> int:
        """Get verse count for a chapter (simplified - use Bible API in production)"""
        if book in BIBLE_STRUCTURE:
            chapters, verses = BIBLE_STRUCTURE[book]
            if 1 <= chapter <= len(verses):
                return verses[chapter - 1]
        # Default fallback - you should use a proper Bible API
        return 30  # Average verse count

    def process_verse(self, book: str, chapter: int, verse: int, 
                     source_types: List[str] = None, delay: float = 1.0) -> dict:
        """Process a single verse with rate limiting"""
        logger.info(f"Processing {book} {chapter}:{verse}")
        
        try:
            result = self.agent.build_commentary(
                book=book,
                chapter=chapter,
                verse=verse,
                source_types=source_types,
                synthesize=True
            )
            
            time.sleep(delay)  # Rate limiting
            return {"success": True, "result": result}
        except Exception as e:
            logger.error(f"Error processing {book} {chapter}:{verse}: {e}")
            return {"success": False, "error": str(e)}

    def process_chapter(self, book: str, chapter: int, 
                       source_types: List[str] = None,
                       delay: float = 1.0) -> dict:
        """Process all verses in a chapter"""
        verse_count = self.get_verse_count(book, chapter)
        results = []
        
        logger.info(f"Processing {book} chapter {chapter} ({verse_count} verses)")
        
        for verse in range(1, verse_count + 1):
            result = self.process_verse(book, chapter, verse, source_types, delay)
            results.append(result)
        
        success_count = sum(1 for r in results if r["success"])
        return {
            "book": book,
            "chapter": chapter,
            "total_verses": verse_count,
            "successful": success_count,
            "failed": verse_count - success_count,
            "results": results
        }

    def process_book(self, book: str, start_chapter: int = 1, end_chapter: int = None,
                    source_types: List[str] = None, delay: float = 1.0) -> dict:
        """Process all chapters in a book"""
        if book not in BIBLE_STRUCTURE:
            logger.warning(f"Book {book} not in structure. Using default chapter count.")
            end_chapter = end_chapter or 50  # Default
        
        if end_chapter is None:
            chapters, _ = BIBLE_STRUCTURE.get(book, (50, []))
            end_chapter = chapters
        
        logger.info(f"Processing {book} chapters {start_chapter}-{end_chapter}")
        
        all_results = []
        for chapter in range(start_chapter, end_chapter + 1):
            chapter_result = self.process_chapter(book, chapter, source_types, delay)
            all_results.append(chapter_result)
        
        total_verses = sum(r["total_verses"] for r in all_results)
        total_successful = sum(r["successful"] for r in all_results)
        
        return {
            "book": book,
            "chapters_processed": end_chapter - start_chapter + 1,
            "total_verses": total_verses,
            "successful": total_successful,
            "failed": total_verses - total_successful,
            "results": all_results
        }

    def process_range(self, start_book: str, end_book: str = None,
                     source_types: List[str] = None, delay: float = 1.0) -> dict:
        """Process a range of books"""
        start_idx = BIBLE_BOOKS.index(start_book) if start_book in BIBLE_BOOKS else 0
        end_idx = BIBLE_BOOKS.index(end_book) + 1 if end_book and end_book in BIBLE_BOOKS else len(BIBLE_BOOKS)
        
        logger.info(f"Processing books from {BIBLE_BOOKS[start_idx]} to {BIBLE_BOOKS[end_idx-1]}")
        
        all_results = []
        for book in BIBLE_BOOKS[start_idx:end_idx]:
            book_result = self.process_book(book, source_types=source_types, delay=delay)
            all_results.append(book_result)
        
        total_verses = sum(r["total_verses"] for r in all_results)
        total_successful = sum(r["successful"] for r in all_results)
        
        return {
            "books_processed": end_idx - start_idx,
            "total_verses": total_verses,
            "successful": total_successful,
            "failed": total_verses - total_successful,
            "results": all_results
        }


def main():
    parser = argparse.ArgumentParser(description="Batch process Bible commentaries")
    parser.add_argument("--book", type=str, required=True, help="Bible book name")
    parser.add_argument("--chapter", type=int, help="Specific chapter to process")
    parser.add_argument("--start-chapter", type=int, default=1, help="Start chapter")
    parser.add_argument("--end-chapter", type=int, help="End chapter")
    parser.add_argument("--start-book", type=str, help="Start book for range processing")
    parser.add_argument("--end-book", type=str, help="End book for range processing")
    parser.add_argument("--source-types", nargs="+",
                       choices=["church_fathers", "middle_ages", "modern", "jewish", "popes"],
                       help="Source types to include")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    parser.add_argument("--output", type=str, help="Output file path (JSON)")
    
    args = parser.parse_args()
    
    processor = BatchProcessor()
    
    if args.start_book:
        # Process range of books
        result = processor.process_range(
            start_book=args.start_book,
            end_book=args.end_book,
            source_types=args.source_types,
            delay=args.delay
        )
    elif args.chapter:
        # Process single chapter
        result = processor.process_chapter(
            book=args.book,
            chapter=args.chapter,
            source_types=args.source_types,
            delay=args.delay
        )
    else:
        # Process entire book
        result = processor.process_book(
            book=args.book,
            start_chapter=args.start_chapter,
            end_chapter=args.end_chapter,
            source_types=args.source_types,
            delay=args.delay
        )
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        logger.info(f"Results saved to {args.output}")
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
