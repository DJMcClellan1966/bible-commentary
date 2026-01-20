"""
Kill process using a specific port
Helps free up ports when they're stuck
"""
import subprocess
import sys
import socket


def find_port_process(port):
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python kill_port_process.py <port>")
        print("Example: python kill_port_process.py 8000")
        sys.exit(1)
    
    port = int(sys.argv[1])
    
    print(f"Finding process using port {port}...")
    pid = find_port_process(port)
    
    if pid:
        print(f"Found process: PID {pid}")
        response = input(f"Kill process {pid}? (y/n): ").strip().lower()
        
        if response == 'y':
            if kill_process(pid):
                print(f"[OK] Process {pid} killed. Port {port} is now free.")
            else:
                print(f"[ERROR] Could not kill process. Try running as administrator.")
        else:
            print("Cancelled.")
    else:
        print(f"No process found using port {port}")


if __name__ == "__main__":
    main()