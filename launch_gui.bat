@echo off
echo Starting Laravel Server Manager GUI...
echo.
echo Make sure Python is installed on your system.
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.6+ and try again.
    pause
    exit /b 1
)

REM Check if the GUI script exists
if not exist "server_manager_gui.py" (
    echo ERROR: server_manager_gui.py not found!
    echo Please make sure you're running this from the correct directory.
    pause
    exit /b 1
)

REM Launch the GUI application
echo Launching Server Manager GUI...
python server_manager_gui.py

REM If we get here, the GUI was closed
echo.
echo Server Manager GUI closed.
pause