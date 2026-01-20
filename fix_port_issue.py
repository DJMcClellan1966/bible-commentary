"""
Fix Port 8000 Issue
Helps resolve port conflicts when starting the Bible app
"""
import socket
import subprocess
import sys
import os


def find_port_process(port=8000):
    """Find what process is using the port"""
    try:
        if sys.platform == "win32":
            result = subprocess.run(
                ["netstat", "-ano"], 
                capture_output=True, 
                text=True
            )
            for line in result.stdout.split('\n'):
                if f':{port}' in line and 'LISTENING' in line:
                    parts = line.split()
                    if len(parts) > 4:
                        pid = parts[-1]
                        return pid
        return None
    except:
        return None


def kill_process(pid):
    """Kill a process by PID"""
    try:
        if sys.platform == "win32":
            subprocess.run(["taskkill", "/F", "/PID", str(pid)], check=True)
            return True
        return False
    except:
        return False


def find_free_port(start_port=8000, max_attempts=10):
    """Find a free port"""
    for port in range(start_port, start_port + max_attempts):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('localhost', port))
            sock.close()
            return port
        except:
            continue
    return None


def main():
    print("=" * 80)
    print("FIXING PORT 8000 ISSUE")
    print("=" * 80)
    print()
    
    port = 8000
    
    # Check if port is in use
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('localhost', port))
        sock.close()
        print(f"Port {port} is available!")
        return
    except:
        print(f"Port {port} is already in use.")
        print()
    
    # Find the process
    pid = find_port_process(port)
    
    if pid:
        print(f"Process using port {port}: PID {pid}")
        print()
        print("Options:")
        print("1. Kill the process (free port 8000)")
        print("2. Use a different port")
        print()
        
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == "1":
            print(f"\nKilling process {pid}...")
            if kill_process(pid):
                print(f"[OK] Process killed. Port {port} is now free.")
                print("\nYou can now start the server:")
                print("  python start_bible_app.py")
            else:
                print("[ERROR] Could not kill process. Try running as administrator.")
        else:
            # Find free port
            free_port = find_free_port(8001, 10)
            if free_port:
                print(f"\n[OK] Found free port: {free_port}")
                print(f"\nTo use this port, modify start_bible_app.py:")
                print(f"  Change: uvicorn.run(app, host='0.0.0.0', port=8000)")
                print(f"  To:     uvicorn.run(app, host='0.0.0.0', port={free_port})")
                print(f"\nOr start with:")
                print(f"  uvicorn bible_api:app --host 0.0.0.0 --port {free_port}")
            else:
                print("[ERROR] Could not find free port")
    else:
        print("Could not identify the process.")
        print("\nTry:")
        print("1. Close any other applications using port 8000")
        print("2. Restart your computer")
        print("3. Use a different port (see option 2 above)")


if __name__ == "__main__":
    main()