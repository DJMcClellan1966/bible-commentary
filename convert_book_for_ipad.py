"""
Convert Bible Mysteries Book for iPad Reading
Converts markdown book to EPUB (for iBooks) and PDF formats
"""
import os
import sys
from pathlib import Path

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    from ebooklib import epub
    EPUB_AVAILABLE = True
except ImportError:
    EPUB_AVAILABLE = False

try:
    from markdown2 import markdown as markdown2
    MARKDOWN2_AVAILABLE = True
except ImportError:
    MARKDOWN2_AVAILABLE = False


def convert_to_epub(book_path: str, output_path: str):
    """Convert markdown book to EPUB format for iPad"""
    if not EPUB_AVAILABLE:
        print("Error: ebooklib not installed. Install with: pip install ebooklib")
        return False
    
    print(f"Reading book from: {book_path}")
    
    # Read the book
    with open(book_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create EPUB book
    book = epub.EpubBook()
    
    # Set metadata
    book.set_identifier('bible_mysteries_book')
    book.set_title('The Mysteries of the Bible: How Divine Mysteries Reveal God\'s Grand Design')
    book.set_language('en')
    book.add_author('AI-Powered Biblical Analysis')
    
    # Split into chapters
    chapters = content.split('# Chapter')
    
    # Add introduction
    intro_content = chapters[0] if chapters else content
    intro_chapter = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='en')
    intro_chapter.content = f'<h1>Introduction</h1>{_markdown_to_html(intro_content)}'
    book.add_item(intro_chapter)
    
    # Add chapters
    spine = ['nav', intro_chapter]
    toc = []
    
    for i, chapter_text in enumerate(chapters[1:], 1):
        # Extract chapter title
        lines = chapter_text.split('\n')
        title = lines[0].strip() if lines else f"Chapter {i}"
        
        # Create chapter
        chapter_file = f'chapter_{i:02d}.xhtml'
        chapter = epub.EpubHtml(title=title, file_name=chapter_file, lang='en')
        chapter.content = f'<h1>{title}</h1>{_markdown_to_html(chapter_text)}'
        
        book.add_item(chapter)
        spine.append(chapter)
        toc.append(chapter)
    
    # Add table of contents
    book.toc = toc
    
    # Add default NCX and Nav file
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    
    # Define CSS style
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        font-family: Georgia, serif;
        line-height: 1.6;
        margin: 2em;
    }
    h1 {
        color: #667eea;
        margin-top: 1em;
        margin-bottom: 0.5em;
    }
    h2 {
        color: #764ba2;
        margin-top: 0.8em;
        margin-bottom: 0.4em;
    }
    p {
        margin-bottom: 1em;
        text-align: justify;
    }
    '''
    
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    
    # Set spine
    book.spine = spine
    
    # Write EPUB file
    epub.write_epub(output_path, book)
    print(f"[OK] EPUB created: {output_path}")
    return True


def _markdown_to_html(markdown_text: str) -> str:
    """Convert markdown to HTML"""
    if MARKDOWN2_AVAILABLE:
        return markdown2(markdown_text, extras=['fenced-code-blocks', 'tables'])
    elif MARKDOWN_AVAILABLE:
        return markdown.markdown(markdown_text, extensions=['fenced_code', 'tables'])
    else:
        # Simple conversion
        html = markdown_text.replace('\n\n', '</p><p>')
        html = html.replace('\n', '<br>')
        html = html.replace('# ', '<h1>').replace('## ', '<h2>').replace('### ', '<h3>')
        return f'<p>{html}</p>'


def convert_to_pdf(book_path: str, output_path: str):
    """Convert markdown book to PDF"""
    try:
        import pdfkit
        PDFKIT_AVAILABLE = True
    except ImportError:
        print("Error: pdfkit not installed. Install with: pip install pdfkit")
        print("Also need: wkhtmltopdf (https://wkhtmltopdf.org/downloads.html)")
        return False
    
    print(f"Converting to PDF: {output_path}")
    
    # Read and convert markdown to HTML
    with open(book_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    html_content = _markdown_to_html(content)
    
    # Add CSS styling
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Georgia, serif;
                line-height: 1.8;
                max-width: 800px;
                margin: 0 auto;
                padding: 2em;
            }}
            h1 {{
                color: #667eea;
                margin-top: 2em;
                margin-bottom: 1em;
            }}
            h2 {{
                color: #764ba2;
                margin-top: 1.5em;
                margin-bottom: 0.8em;
            }}
            p {{
                margin-bottom: 1em;
                text-align: justify;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    try:
        pdfkit.from_string(full_html, output_path, options={'page-size': 'A4', 'margin-top': '0.75in', 'margin-bottom': '0.75in', 'margin-left': '0.75in', 'margin-right': '0.75in'})
        print(f"[OK] PDF created: {output_path}")
        return True
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return False


def create_simple_html(book_path: str, output_path: str):
    """Create a simple HTML version for web reading"""
    print(f"Creating HTML version: {output_path}")
    
    with open(book_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    html_content = _markdown_to_html(content)
    
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Mysteries of the Bible</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
        }}
        h1 {{
            color: #667eea;
            margin-top: 2em;
            margin-bottom: 1em;
            font-size: 2em;
        }}
        h2 {{
            color: #764ba2;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
            font-size: 1.5em;
        }}
        h3 {{
            color: #555;
            margin-top: 1.2em;
            margin-bottom: 0.6em;
        }}
        p {{
            margin-bottom: 1em;
            text-align: justify;
        }}
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            .container {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"[OK] HTML created: {output_path}")
    return True


def main():
    """Main conversion function"""
    book_dir = "bible_mysteries_book"
    book_file = os.path.join(book_dir, "bible_mysteries_book.md")
    
    if not os.path.exists(book_file):
        print(f"Error: Book file not found: {book_file}")
        print("\nPlease generate the book first:")
        print("  python generate_bible_mysteries_book.py")
        return
    
    print("=" * 80)
    print("CONVERTING BOOK FOR IPAD READING")
    print("=" * 80)
    print()
    
    # Create output directory
    output_dir = "bible_mysteries_book_formats"
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert to EPUB (best for iPad/iBooks)
    epub_path = os.path.join(output_dir, "bible_mysteries_book.epub")
    if convert_to_epub(book_file, epub_path):
        print(f"\nFor iPad: Transfer '{epub_path}' to your iPad")
        print("   - Email it to yourself and open on iPad")
        print("   - Use AirDrop to transfer")
        print("   - Use iCloud Drive")
        print("   - Open in iBooks/Apple Books app")
    
    # Convert to HTML (for web reading)
    html_path = os.path.join(output_dir, "bible_mysteries_book.html")
    create_simple_html(book_file, html_path)
    print(f"\nHTML version: Open '{html_path}' in any web browser")
    print("   - Works great on iPad Safari")
    print("   - Can be saved to Home Screen as web app")
    
    # Try PDF conversion
    pdf_path = os.path.join(output_dir, "bible_mysteries_book.pdf")
    print(f"\nAttempting PDF conversion...")
    convert_to_pdf(book_file, pdf_path)
    
    print("\n" + "=" * 80)
    print("CONVERSION COMPLETE!")
    print("=" * 80)
    print(f"\nAll formats saved to: {output_dir}/")
    print("\nBest for iPad:")
    print("   1. EPUB file - Open in iBooks/Apple Books")
    print("   2. HTML file - Open in Safari, add to Home Screen")
    print("   3. PDF file - Open in Files app or any PDF reader")


if __name__ == "__main__":
    main()