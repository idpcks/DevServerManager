@echo off
REM DevServerManager Windows Launcher
REM This script provides better error handling and user feedback

title DevServerManager v2.1.1
echo Starting DevServerManager...
echo.
if not exist "DevServerManager.exe" (
    echo ERROR: DevServerManager.exe not found in current directory
    echo Please make sure you're running this from the correct folder
    pause
    exit /b 1
)

REM Start the application
start "" "DevServerManager.exe"

REM Optional: Keep window open for troubleshooting
REM echo Application started successfully!
REM echo You can close this window now.
REM pause
