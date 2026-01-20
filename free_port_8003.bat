@echo off
echo Freeing port 8003...
netstat -ano | findstr :8003
echo.
echo Killing process on port 8003...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8003 ^| findstr LISTENING') do taskkill /F /PID %%a
echo Done.
pause