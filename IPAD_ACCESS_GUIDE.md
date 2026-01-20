# How to Run the Bible App on Your iPad

## Overview

The Bible app is a web-based application that runs on your computer and can be accessed from your iPad through your local network.

---

## Method 1: Same Wi-Fi Network (Recommended)

### Step 1: Start the Server on Your Computer

1. **Open a terminal/command prompt** on your computer
2. **Navigate to the project folder:**
   ```bash
   cd C:\Users\DJMcC\OneDrive\Desktop\qai\bible-commentary
   ```

3. **Start the server:**
   ```bash
   python start_bible_app.py
   ```

   The server will automatically find a free port (usually 8000 or 8001) and display:
   ```
   Server will be available at:
     - Main app: http://localhost:8000/
     - Bible app: http://localhost:8000/bible
     - Journey: http://localhost:8000/journey
     - Understanding: http://localhost:8000/understanding
   ```

4. **Note the IP address and port** shown in the output

### Step 2: Find Your Computer's IP Address

**On Windows:**
1. Open Command Prompt
2. Type: `ipconfig`
3. Look for "IPv4 Address" under your active network adapter
   - Example: `192.168.1.100`

**On Mac:**
1. Open System Preferences → Network
2. Select your Wi-Fi connection
3. Note the IP address shown

**On Linux:**
```bash
hostname -I
```

### Step 3: Access from Your iPad

1. **Make sure your iPad is on the same Wi-Fi network** as your computer

2. **Open Safari on your iPad**

3. **Enter the address:**
   ```
   http://YOUR_COMPUTER_IP:PORT
   ```
   
   Example:
   ```
   http://192.168.1.100:8000
   ```

4. **Access specific apps:**
   - Main Bible App: `http://192.168.1.100:8000/bible`
   - Understanding Bible: `http://192.168.1.100:8000/understanding`
   - Relationship Journey: `http://192.168.1.100:8000/journey`
   - API Docs: `http://192.168.1.100:8000/docs`

### Step 4: Add to Home Screen (Optional)

1. In Safari, tap the **Share button** (square with arrow)
2. Tap **"Add to Home Screen"**
3. Give it a name (e.g., "Bible App")
4. Tap **"Add"**

Now you have an app icon on your iPad home screen!

---

## Method 2: Using ngrok (Access from Anywhere)

If you want to access the app from anywhere (not just your local network):

### Step 1: Install ngrok

1. Download from: https://ngrok.com/download
2. Extract and add to your PATH

### Step 2: Start Your Server

```bash
python start_bible_app.py
```

Note the port (e.g., 8000)

### Step 3: Start ngrok

In a new terminal:
```bash
ngrok http 8000
```

This will give you a public URL like:
```
https://abc123.ngrok.io
```

### Step 4: Access from iPad

1. Open Safari on your iPad
2. Enter the ngrok URL
3. Access your app from anywhere!

**Note:** Free ngrok URLs change each time you restart. For permanent URLs, upgrade to a paid plan.

---

## Method 3: Deploy to a Server (Permanent Solution)

For a permanent solution, deploy to:
- **Heroku** (free tier available)
- **DigitalOcean** ($5/month)
- **AWS** (pay as you go)
- **PythonAnywhere** (free tier available)

---

## Troubleshooting

### Can't Connect from iPad

1. **Check firewall:** Make sure Windows Firewall allows connections on the port
   - Windows: Control Panel → Windows Defender Firewall → Allow an app
   - Allow Python through firewall

2. **Check network:** Make sure both devices are on the same Wi-Fi network

3. **Check IP address:** Your computer's IP might have changed
   - Run `ipconfig` again to get current IP

4. **Check port:** Make sure the server is actually running
   - Look for "Application startup complete" in the terminal

### Server Won't Start

1. **Port in use:** The auto-port finder should handle this, but if it doesn't:
   ```bash
   python fix_port_issue.py
   ```

2. **Missing dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```

### Slow Performance

- The first load might be slow as it loads Bible data
- Subsequent loads should be faster
- Consider using the optimized version if available

---

## Quick Start Script

Create a file `start_for_ipad.bat` (Windows) or `start_for_ipad.sh` (Mac/Linux):

**Windows (`start_for_ipad.bat`):**
```batch
@echo off
echo Starting Bible App for iPad Access...
echo.
python start_bible_app.py
pause
```

**Mac/Linux (`start_for_ipad.sh`):**
```bash
#!/bin/bash
echo "Starting Bible App for iPad Access..."
echo ""
python start_bible_app.py
```

Then just double-click to start!

---

## Recommended Setup

1. **Start server** on your computer
2. **Note the IP and port** from the output
3. **Open Safari on iPad** and enter the address
4. **Add to Home Screen** for easy access
5. **Keep server running** while using the app

---

## Features Available on iPad

All features work on iPad:
- ✅ Bible reading with hyperlinks
- ✅ AI commentary
- ✅ Semantic search
- ✅ Understanding Bible (theological insights)
- ✅ Relationship Journey
- ✅ Book Library
- ✅ Cross-references

The app is fully responsive and works great on iPad!

---

## Tips

1. **Keep your computer on** while using the app
2. **Bookmark the address** in Safari for quick access
3. **Add to Home Screen** to make it feel like a native app
4. **Use landscape mode** for better reading experience
5. **Keep server terminal open** to see any errors

Enjoy your Bible app on iPad! 📱📖