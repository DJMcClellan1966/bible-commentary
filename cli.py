"""
Command-line interface for Bible Commentary Agent
"""
import argparse
import json
from agent import BibleCommentaryAgent
from models import init_db

def main():
    parser = argparse.ArgumentParser(description="Bible Commentary Agent CLI")
    parser.add_argument("command", choices=["build", "search", "get", "suggest", "batch"],
                       help="Command to execute")
    parser.add_argument("--book", type=str, help="Bible book name")
    parser.add_argument("--chapter", type=int, help="Chapter number")
    parser.add_argument("--verse", type=int, help="Verse number")
    parser.add_argument("--query", type=str, help="Search query")
    parser.add_argument("--category", type=str, 
                       choices=["church_fathers", "middle_ages", "modern", "jewish", "popes"],
                       help="Commentary category")
    parser.add_argument("--source-types", nargs="+",
                       choices=["church_fathers", "middle_ages", "modern", "jewish", "popes"],
                       help="Source types to include")
    parser.add_argument("--synthesize", action="store_true", default=True,
                       help="Synthesize commentaries with AI")
    parser.add_argument("--no-synthesize", dest="synthesize", action="store_false",
                       help="Don't synthesize commentaries")
    parser.add_argument("--output", type=str, help="Output file path (JSON)")
    parser.add_argument("--start-book", type=str, help="Start book for batch processing")
    parser.add_argument("--end-book", type=str, help="End book for batch processing")
    
    args = parser.parse_args()
    
    # Initialize database
    init_db()
    
    # Initialize agent
    agent = BibleCommentaryAgent()
    
    if args.command == "build":
        if not all([args.book, args.chapter, args.verse]):
            print("Error: --book, --chapter, and --verse are required for 'build' command")
            return
        
        print(f"Building commentary for {args.book} {args.chapter}:{args.verse}...")
        result = agent.build_commentary(
            book=args.book,
            chapter=args.chapter,
            verse=args.verse,
            source_types=args.source_types,
            synthesize=args.synthesize
        )
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "search":
        if not args.query:
            print("Error: --query is required for 'search' command")
            return
        
        print(f"Searching for: {args.query}...")
        results = agent.search_commentaries(
            query=args.query,
            book=args.book,
            chapter=args.chapter,
            verse=args.verse,
            source_types=args.source_types
        )
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump({"results": results, "count": len(results)}, f, indent=2, ensure_ascii=False)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps({"results": results, "count": len(results)}, indent=2, ensure_ascii=False))
    
    elif args.command == "get":
        if not all([args.book, args.chapter, args.verse, args.category]):
            print("Error: --book, --chapter, --verse, and --category are required for 'get' command")
            return
        
        print(f"Getting {args.category} commentary for {args.book} {args.chapter}:{args.verse}...")
        result = agent.get_commentary_by_category(
            book=args.book,
            chapter=args.chapter,
            verse=args.verse,
            category=args.category
        )
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.command == "suggest":
        if not all([args.book, args.chapter, args.verse]):
            print("Error: --book, --chapter, and --verse are required for 'suggest' command")
            return
        
        print(f"Getting suggestions for {args.book} {args.chapter}:{args.verse}...")
        suggestions = agent.suggest_improvements(
            book=args.book,
            chapter=args.chapter,
            verse=args.verse
        )
        
        print("\nSuggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
    
    elif args.command == "batch":
        from config import BIBLE_BOOKS
        
        start_idx = BIBLE_BOOKS.index(args.start_book) if args.start_book else 0
        end_idx = BIBLE_BOOKS.index(args.end_book) + 1 if args.end_book else len(BIBLE_BOOKS)
        
        print(f"Batch processing from {BIBLE_BOOKS[start_idx]} to {BIBLE_BOOKS[end_idx-1]}...")
        print("Note: This will process all chapters and verses. Use with caution!")
        
        # This is a template - you'd need to implement chapter/verse ranges
        # For now, just show the structure
        print("\nBatch processing structure:")
        print("- For each book in range")
        print("- For each chapter (1 to N)")
        print("- For each verse (1 to M)")
        print("- Build commentary")
        print("\nThis would take a very long time. Consider processing specific books/chapters.")

if __name__ == "__main__":
    main()
