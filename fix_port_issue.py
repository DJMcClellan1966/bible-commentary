"""
Helper script to fix port 8000 issue
"""
import subprocess
import sys
import os

def kill_process_on_port(port=8000):
    """Kill process using port 8000"""
    try:
        # Find process using port
        result = subprocess.run(
            ['netstat', '-ano'],
            capture_output=True,
            text=True
        )
        
        for line in result.stdout.split('\n'):
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    print(f"Found process {pid} using port {port}")
                    
                    # Kill the process
                    try:
                        subprocess.run(['taskkill', '/F', '/PID', pid], check=True)
                        print(f"Successfully killed process {pid}")
                        return True
                    except subprocess.CalledProcessError:
                        print(f"Could not kill process {pid} - may need admin rights")
                        return False
        
        print(f"No process found using port {port}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Attempting to free port 8000...")
    if kill_process_on_port(8000):
        print("\nPort 8000 is now free! You can run:")
        print("  uvicorn api:app --reload")
    else:
        print("\nCould not free port 8000. Try:")
        print("  1. Run as administrator")
        print("  2. Or use a different port:")
        print("     uvicorn api:app --reload --port 8001")
