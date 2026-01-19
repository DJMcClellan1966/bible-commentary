# Building a Standalone Desktop App

## Option 1: Simple Executable (Recommended)

### Step 1: Install PyInstaller
```bash
pip install pyinstaller
```

### Step 2: Build the App
```bash
python create_standalone_app.py
```

This will create `dist/BibleCommentaryApp.exe` that you can:
- Double-click to run
- Distribute to others
- Run without Python installed (first run extracts files)

### Step 3: Run the App
Just double-click `BibleCommentaryApp.exe` - it will:
1. Start the server automatically
2. Open your browser to the app
3. Work completely offline (after first run)

---

## Option 2: Desktop App with Embedded Browser

### Step 1: Install Dependencies
```bash
pip install pywebview
```

### Step 2: Run the Desktop App
```bash
python desktop_app.py
```

This creates a native desktop window with embedded browser - no separate browser needed!

---

## Option 3: Simple Launcher (Current)

### Run the Launcher
```bash
python app_launcher.py
```

This will:
- Start the server
- Open browser automatically
- Show status in console

---

## Creating Distribution Package

### For Windows (.exe):
1. Run `python create_standalone_app.py`
2. Find `dist/BibleCommentaryApp.exe`
3. Test it works
4. Share the .exe file

### For Mac (.app):
```bash
pyinstaller --name=BibleCommentaryApp --windowed --onefile app_launcher.py
```

### For Linux:
```bash
pyinstaller --name=BibleCommentaryApp --onefile app_launcher.py
```

---

## Features of Standalone App

✅ **No Installation Required** - Just double-click and run
✅ **Offline Capable** - Works without internet (after first run)
✅ **Portable** - Can run from USB drive
✅ **Auto-Launch** - Opens browser automatically
✅ **Self-Contained** - Includes all dependencies

---

## Troubleshooting

### "Port already in use"
- Close other instances of the app
- Or modify port in `app_launcher.py`

### "Missing modules"
- Make sure all dependencies are in `requirements.txt`
- Rebuild with PyInstaller

### "App won't start"
- Check console for error messages
- Make sure database file exists
- Try running `python app_launcher.py` first to test

---

## Advanced: Add Icon

1. Create or download an `.ico` file (Windows) or `.icns` (Mac)
2. Update `create_standalone_app.py`:
   ```python
   '--icon=icon.ico',  # Replace with your icon path
   ```

---

## Distribution

To share the app:
1. Build the executable
2. Test it on a clean machine
3. Create a zip file with:
   - `BibleCommentaryApp.exe`
   - `README.txt` (instructions)
4. Share the zip file

Users just need to:
1. Extract the zip
2. Double-click `BibleCommentaryApp.exe`
3. Use the app!
