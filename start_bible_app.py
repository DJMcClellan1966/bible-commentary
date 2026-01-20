"""
Start Bible App Server
Launches the FastAPI server for the Bible Study App
Automatically finds a free port if 8000 is in use
"""
import uvicorn
import os
import sys
import socket

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def find_free_port(start_port=8000, max_attempts=20):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

if __name__ == "__main__":
    print("=" * 80)
    print("BIBLE STUDY APP - Starting Server")
    print("=" * 80)
    
    # Try port 8000 first
    port = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        print(f"\nUsing port {port}")
    except OSError:
        print(f"\nPort {port} is in use. Finding free port...")
        port = find_free_port(8001, 20)
        if not port:
            print("ERROR: Could not find a free port")
            sys.exit(1)
        print(f"Using port {port} instead")
    
    print("\nServer will be available at:")
    print(f"  - Main app: http://localhost:{port}/")
    print(f"  - Bible app: http://localhost:{port}/bible")
    print(f"  - Journey: http://localhost:{port}/journey")
    print(f"  - Understanding: http://localhost:{port}/understanding")
    print(f"  - API docs: http://localhost:{port}/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80)
    print()
    
    try:
        # Import and run Bible API
        from bible_api import app
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    except ImportError as e:
        print(f"Error: Could not import Bible API: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install fastapi uvicorn")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\nError starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)