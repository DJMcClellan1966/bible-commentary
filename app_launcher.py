"""
Standalone Bible Commentary App Launcher
This script starts the server and opens the app in the default browser
"""
import os
import sys
import webbrowser
import threading
import time
import subprocess
from pathlib import Path

def find_free_port(start_port=8000):
    """Find a free port starting from start_port"""
    import socket
    port = start_port
    while port < start_port + 100:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            port += 1
    return None

def start_server(port=8000):
    """Start the FastAPI server"""
    try:
        import uvicorn
        from api import app
        
        # Start server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=port,
            log_level="info",
            access_log=False
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def open_browser(port=8000, delay=2):
    """Open browser after server starts"""
    time.sleep(delay)
    url = f"http://127.0.0.1:{port}"
    print(f"Opening browser at {url}")
    webbrowser.open(url)

def main():
    """Main launcher function"""
    print("=" * 60)
    print("Quantum AI Framework")
    print("=" * 60)
    print("\nStarting server...")
    
    # Find free port
    port = find_free_port()
    if not port:
        print("Error: Could not find a free port")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"Server will start on port {port}")
    print(f"App will open at http://127.0.0.1:{port}")
    print("\nTo close the app, close this window or press Ctrl+C\n")
    
    # Start browser in background thread
    browser_thread = threading.Thread(target=open_browser, args=(port,), daemon=True)
    browser_thread.start()
    
    # Start server (this blocks)
    try:
        start_server(port)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        sys.exit(0)

if __name__ == "__main__":
    main()
