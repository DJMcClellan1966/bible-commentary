"""
Start Bible App - Auto-find Free Port
Automatically finds a free port if 8000 is in use
"""
import socket
import uvicorn
import sys
import os

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

def main():
    print("=" * 80)
    print("STARTING BIBLE APP")
    print("=" * 80)
    print()
    
    # Try port 8000 first
    port = 8000
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        print(f"Using port {port}")
    except OSError:
        print(f"Port {port} is in use. Finding free port...")
        port = find_free_port(8001, 20)
        if not port:
            print("ERROR: Could not find a free port")
            sys.exit(1)
        print(f"Using port {port} instead")
    
    print()
    print("Server will be available at:")
    print(f"  - Main app: http://localhost:{port}/")
    print(f"  - Journey: http://localhost:{port}/journey")
    print(f"  - Understanding: http://localhost:{port}/understanding")
    print(f"  - API docs: http://localhost:{port}/docs")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 80)
    print()
    
    try:
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

if __name__ == "__main__":
    main()