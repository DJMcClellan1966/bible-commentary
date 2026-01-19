# Running Bible Commentary Agent on iPad

## Method 1: Access via Web Interface (Easiest)

### Step 1: Find Your Computer's IP Address

**On Windows:**
```powershell
ipconfig
```
Look for "IPv4 Address" under your active network adapter (usually starts with 192.168.x.x or 10.x.x.x)

**On Mac:**
```bash
ifconfig | grep "inet "
```

**On Linux:**
```bash
ip addr show
```

### Step 2: Start the API Server on Your Computer

Make sure the server is accessible on your network (not just localhost):

```bash
# On Windows PowerShell
$env:UVICORN_HOST="0.0.0.0"
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Or on Mac/Linux
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Serve the Web Interface

**Option A: Using Python's built-in server**
```bash
# In the project directory
python -m http.server 8080
```

**Option B: Using the API server (serve static files)**
Add this to your `api.py`:
```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory=".", html=True), name="static")
```

### Step 4: Access from iPad

1. Make sure your iPad is on the **same Wi-Fi network** as your computer
2. Open Safari on your iPad
3. Navigate to: `http://YOUR_COMPUTER_IP:8080/web_interface.html`
   - Replace `YOUR_COMPUTER_IP` with the IP address from Step 1
   - Example: `http://192.168.1.100:8080/web_interface.html`
4. In the web interface, update the "API Server URL" field to: `http://YOUR_COMPUTER_IP:8000`

## Method 2: Direct API Access from iPad

You can use any REST client app on iPad to access the API directly:

1. **Install a REST client app** (e.g., "REST Client", "Postman", or "Insomnia")
2. Make sure the API server is running with `--host 0.0.0.0`
3. Use your computer's IP address: `http://YOUR_COMPUTER_IP:8000`

## Method 3: Deploy to Cloud (Advanced)

### Deploy to Heroku, Railway, or Render

1. Create a `Procfile`:
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

2. Deploy using your preferred platform
3. Access from anywhere using the provided URL

## Quick Setup Script

Create a file `start_for_ipad.py`:

```python
import subprocess
import socket
import webbrowser

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"\n{'='*60}")
    print(f"Bible Commentary Agent - iPad Access")
    print(f"{'='*60}")
    print(f"\nYour computer's IP: {local_ip}")
    print(f"\nAPI Server: http://{local_ip}:8000")
    print(f"Web Interface: http://{local_ip}:8080/web_interface.html")
    print(f"\nOn your iPad, open Safari and go to:")
    print(f"http://{local_ip}:8080/web_interface.html")
    print(f"\n{'='*60}\n")
    
    # Start API server
    print("Starting API server...")
    subprocess.run(["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"])
```

Run it:
```bash
python start_for_ipad.py
```

## Troubleshooting

### Can't connect from iPad

1. **Check firewall**: Make sure Windows Firewall allows connections on ports 8000 and 8080
   ```powershell
   # Allow ports in Windows Firewall
   New-NetFirewallRule -DisplayName "Bible Commentary API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
   New-NetFirewallRule -DisplayName "Bible Commentary Web" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
   ```

2. **Check network**: Ensure iPad and computer are on the same Wi-Fi network

3. **Test connection**: From iPad, try accessing `http://YOUR_IP:8000/health` first

### Server not accessible

- Make sure you're using `--host 0.0.0.0` (not just `localhost`)
- Check that no other application is using ports 8000 or 8080
- Try a different port if needed

### Web interface not loading

- Make sure `web_interface.html` is in the project directory
- Check that the HTTP server is running on port 8080
- Verify the API URL in the web interface matches your computer's IP

## Security Note

⚠️ **Important**: When running on `0.0.0.0`, your API is accessible to anyone on your local network. For production use, consider:
- Adding authentication
- Using HTTPS
- Restricting access to specific IPs
- Deploying to a secure cloud service
