"""
Start script for iPad access - makes the server accessible on local network
"""
import subprocess
import socket
import sys
import os

def get_local_ip():
    """Get the local IP address of this computer"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to a remote address (doesn't actually send data)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def print_banner(local_ip):
    """Print connection information"""
    print("\n" + "="*70)
    print(" " * 15 + "Bible Commentary Agent - iPad Access")
    print("="*70)
    print(f"\n✓ Server starting on all network interfaces")
    print(f"\n📱 On your iPad (same Wi-Fi network):")
    print(f"   Open Safari and go to:")
    print(f"   http://{local_ip}:8000")
    print(f"\n💻 On this computer:")
    print(f"   http://localhost:8000")
    print(f"\n📚 API Documentation:")
    print(f"   http://{local_ip}:8000/docs")
    print(f"\n" + "="*70)
    print("\nPress Ctrl+C to stop the server\n")

if __name__ == "__main__":
    local_ip = get_local_ip()
    print_banner(local_ip)
    
    # Check if web interface exists
    if not os.path.exists("web_interface.html"):
        print("⚠️  Warning: web_interface.html not found. Web interface may not work.")
        print("   The API will still be accessible at /docs\n")
    
    try:
        # Start the server on all interfaces (0.0.0.0)
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "api:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nMake sure you have installed all dependencies:")
        print("  pip install -r requirements.txt")
