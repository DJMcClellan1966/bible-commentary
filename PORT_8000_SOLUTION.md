# Port 8000 Already in Use - Solutions

## Quick Fixes

### Option 1: Use Auto-Port Script (Easiest) ⭐

**Use the new script that automatically finds a free port:**

```bash
python start_bible_app_auto_port.py
```

This will:
- Try port 8000 first
- If busy, automatically use 8001, 8002, etc.
- Tell you which port it's using

**No manual configuration needed!**

---

### Option 2: Kill Process Using Port 8000

**Windows PowerShell (as Administrator):**
```powershell
# Find process
netstat -ano | findstr :8000

# Kill process (replace PID with actual process ID)
taskkill /F /PID <PID>
```

**Or use the fix script:**
```bash
python fix_port_issue.py
```

---

### Option 3: Use Different Port Manually

**Modify `start_bible_app.py`:**
```python
# Change this line:
uvicorn.run(app, host="0.0.0.0", port=8000)

# To:
uvicorn.run(app, host="0.0.0.0", port=8001)  # or any free port
```

**Or start directly:**
```bash
uvicorn bible_api:app --host 0.0.0.0 --port 8001
```

---

## Recommended Solution

**Use `start_bible_app_auto_port.py`** - it handles everything automatically!

```bash
python start_bible_app_auto_port.py
```

It will find a free port and tell you which one to use. 🚀