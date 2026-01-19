"""
Desktop Application with Embedded Browser
Uses Tkinter with embedded webview for a native desktop experience
"""
import tkinter as tk
from tkinter import ttk
import threading
import webbrowser
import time
import sys
import os

try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("Note: pywebview not installed. Using system browser instead.")
    print("For better experience, install: pip install pywebview")

def start_server(port=8000):
    """Start the FastAPI server in a separate thread"""
    try:
        import uvicorn
        from api import app
        
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=port,
            log_level="warning",
            access_log=False
        )
    except Exception as e:
        print(f"Error starting server: {e}")
        return False
    return True

def open_webview(port=8000):
    """Open embedded webview window"""
    url = f"http://127.0.0.1:{port}"
    
    if WEBVIEW_AVAILABLE:
        # Wait for server to start
        time.sleep(2)
        webview.create_window(
            'Bible Commentary & Study App',
            url,
            width=1400,
            height=900,
            min_size=(800, 600),
            resizable=True
        )
        webview.start(debug=False)
    else:
        # Fallback to system browser
        webbrowser.open(url)
        print(f"App opened in browser at {url}")
        print("Close this window to stop the server")

def create_tkinter_app(port=8000):
    """Create Tkinter launcher window"""
    root = tk.Tk()
    root.title("Bible Commentary & Study App")
    root.geometry("500x300")
    root.resizable(False, False)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (500 // 2)
    y = (root.winfo_screenheight() // 2) - (300 // 2)
    root.geometry(f"500x300+{x}+{y}")
    
    # Styling
    style = ttk.Style()
    style.theme_use('clam')
    
    # Header
    header_frame = tk.Frame(root, bg="#4a90e2", height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text="📖 Bible Commentary & Study",
        font=("Arial", 18, "bold"),
        bg="#4a90e2",
        fg="white"
    )
    title_label.pack(pady=20)
    
    # Content
    content_frame = tk.Frame(root, bg="white")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    status_label = tk.Label(
        content_frame,
        text="Starting server...",
        font=("Arial", 12),
        bg="white",
        fg="#333"
    )
    status_label.pack(pady=20)
    
    progress = ttk.Progressbar(
        content_frame,
        mode='indeterminate',
        length=300
    )
    progress.pack(pady=10)
    progress.start()
    
    url_label = tk.Label(
        content_frame,
        text=f"http://127.0.0.1:{port}",
        font=("Arial", 10),
        bg="white",
        fg="#4a90e2",
        cursor="hand2"
    )
    url_label.pack(pady=10)
    
    def open_browser():
        webbrowser.open(f"http://127.0.0.1:{port}")
    
    url_label.bind("<Button-1>", lambda e: open_browser())
    
    info_label = tk.Label(
        content_frame,
        text="The app will open in your browser.\nClose this window to stop the server.",
        font=("Arial", 9),
        bg="white",
        fg="#666",
        justify=tk.CENTER
    )
    info_label.pack(pady=10)
    
    # Start server in background
    def start_app():
        server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
        server_thread.start()
        
        # Update status
        time.sleep(1)
        status_label.config(text="Server started!")
        progress.stop()
        progress.config(mode='determinate', value=100)
        
        # Open browser
        time.sleep(1)
        open_browser()
    
    # Start after window is shown
    root.after(100, start_app)
    
    # Handle window close
    def on_closing():
        root.destroy()
        sys.exit(0)
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

def main():
    """Main entry point"""
    port = 8000
    
    # Check if port is available
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
    except OSError:
        print(f"Port {port} is already in use. Trying another port...")
        port = 8001
    
    if WEBVIEW_AVAILABLE:
        # Use embedded webview
        server_thread = threading.Thread(target=start_server, args=(port,), daemon=True)
        server_thread.start()
        open_webview(port)
    else:
        # Use Tkinter launcher with system browser
        create_tkinter_app(port)

if __name__ == "__main__":
    main()
