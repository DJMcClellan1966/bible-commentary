"""
Script to create a standalone executable using PyInstaller
Run this to build the app: python create_standalone_app.py
"""
import PyInstaller.__main__
import os
import sys

def build_app():
    """Build standalone executable"""
    print("Building standalone Bible Commentary App...")
    print("This may take a few minutes...\n")
    
    # PyInstaller arguments
    args = [
        'app_launcher.py',
        '--name=BibleCommentaryApp',
        '--onefile',
        '--windowed',  # No console window on Windows
        '--icon=NONE',  # Add icon file path if you have one
        '--add-data=web_interface.html;.',
        '--add-data=improved_web_interface.html;.',
        '--add-data=bible_study.html;.',
        '--add-data=bible_ai_interface.html;.',
        '--add-data=bible_llm_interface.html;.',
        '--add-data=quantum_study_interface.html;.',
        '--add-data=bible_characters_interface.html;.',
        '--add-data=quantum_ai_interface.html;.',
        '--hidden-import=uvicorn',
        '--hidden-import=fastapi',
        '--hidden-import=sqlalchemy',
        '--hidden-import=bs4',
        '--hidden-import=langchain',
        '--collect-all=uvicorn',
        '--collect-all=fastapi',
    ]
    
    try:
        PyInstaller.__main__.run(args)
        print("\n" + "=" * 60)
        print("Build complete!")
        print("=" * 60)
        print("\nExecutable created in: dist/BibleCommentaryApp.exe")
        print("You can now distribute this file to run the app anywhere!")
        print("\nNote: The first run may take a moment to extract files.")
    except Exception as e:
        print(f"\nError building app: {e}")
        print("\nMake sure PyInstaller is installed:")
        print("  pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_app()
