"""
Start Deep Bible Study App

Simple launcher for your personal Bible study application.
"""

import subprocess
import sys
import os
import webbrowser
import time


def check_dependencies():
    """Check if required packages are installed"""
    required = ['fastapi', 'uvicorn']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)


def main():
    print("=" * 60)
    print("DEEP BIBLE STUDY")
    print("Personal Bible Study with Deep Interconnections")
    print("=" * 60)
    print()
    
    # Check dependencies
    check_dependencies()
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start the server
    port = 8080
    print(f"Starting server on http://localhost:{port}")
    print()
    print("Features:")
    print("  - Daily reading with deep interconnections")
    print("  - Backward/Forward Scripture links")
    print("  - Typological connections (OT to Christ)")
    print("  - Church Fathers wisdom")
    print("  - AI Twin that learns your journey")
    print("  - 365-day chronological reading plan")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Open browser after short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open(f'http://localhost:{port}')
    
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Run uvicorn
    import uvicorn
    uvicorn.run(
        "deep_bible_api:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()
