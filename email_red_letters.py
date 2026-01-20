"""
Quick script to help email the Red Letters book
Opens your default email client with the EPUB file ready to attach
"""
import os
import subprocess
import sys

def email_red_letters():
    """Help user email the Red Letters book"""
    
    epub_file = "red_letters_book_formats/red_letters_book.epub"
    html_file = "red_letters_book_formats/red_letters_book.html"
    
    print("=" * 80)
    print("EMAIL RED LETTERS BOOK")
    print("=" * 80)
    print()
    
    # Check if files exist
    if not os.path.exists(epub_file):
        print(f"Error: EPUB file not found: {epub_file}")
        return
    
    print(f"Found EPUB file: {epub_file}")
    print(f"File size: {os.path.getsize(epub_file) // 1024} KB")
    print()
    
    # Get full path
    full_path = os.path.abspath(epub_file)
    
    print("To email the book:")
    print()
    print("METHOD 1: Manual (Easiest)")
    print("-" * 80)
    print("1. Open your email (Gmail, Outlook, etc.)")
    print("2. Click 'Compose' or 'New Email'")
    print("3. Click 'Attach' (paperclip icon)")
    print(f"4. Navigate to: {os.path.dirname(full_path)}")
    print("5. Select: red_letters_book.epub")
    print("6. Enter your email address")
    print("7. Send!")
    print()
    print("METHOD 2: Right-Click (Windows)")
    print("-" * 80)
    print(f"1. Open File Explorer")
    print(f"2. Navigate to: {os.path.dirname(full_path)}")
    print("3. Right-click on: red_letters_book.epub")
    print("4. Choose 'Send to' -> 'Mail recipient'")
    print("5. Your email client opens with file attached")
    print()
    print("METHOD 3: Drag and Drop")
    print("-" * 80)
    print("1. Open your email in browser/app")
    print("2. Open File Explorer")
    print(f"3. Navigate to: {os.path.dirname(full_path)}")
    print("4. Drag red_letters_book.epub into email")
    print("5. Send!")
    print()
    print("=" * 80)
    print("FILE LOCATION:")
    print("=" * 80)
    print(full_path)
    print()
    print("On iPad:")
    print("1. Open email")
    print("2. Tap the EPUB attachment")
    print("3. Choose 'Open in Books'")
    print("4. Book appears in your library!")
    print()
    
    # Try to open file location
    try:
        if sys.platform == "win32":
            # Windows: Open folder in Explorer
            subprocess.run(["explorer", "/select,", full_path])
            print("Opened file location in Windows Explorer")
        elif sys.platform == "darwin":
            # Mac: Open folder in Finder
            subprocess.run(["open", "-R", full_path])
            print("Opened file location in Finder")
        else:
            # Linux: Open folder
            subprocess.run(["xdg-open", os.path.dirname(full_path)])
            print("Opened file location")
    except Exception as e:
        print(f"Could not open file location automatically: {e}")
        print("Please navigate manually to the path above")


if __name__ == "__main__":
    email_red_letters()