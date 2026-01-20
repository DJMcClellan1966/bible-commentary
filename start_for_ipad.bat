@echo off
echo ================================================================================
echo BIBLE APP - STARTING FOR IPAD ACCESS
echo ================================================================================
echo.
echo This will start the server so you can access it from your iPad.
echo.
echo IMPORTANT: Make sure your iPad is on the same Wi-Fi network as this computer.
echo.
echo After starting, you'll see:
echo   - The IP address to use
echo   - The port number
echo.
echo Then on your iPad, open Safari and go to:
echo   http://YOUR_IP:PORT
echo.
echo Example: http://192.168.1.100:8000
echo.
echo Press any key to start the server...
pause >nul
echo.
echo Starting server...
echo.

python start_bible_app.py

pause